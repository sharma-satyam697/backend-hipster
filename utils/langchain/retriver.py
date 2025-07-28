import json
import os
from json import JSONDecodeError
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from icecream import ic
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

from utils.logger import Logger


load_dotenv()

async def documents_chunking(path:str):
# Load all .md and .txt files
    try:
        loader = DirectoryLoader(f"{path}/", glob="**/[!.]*" , loader_cls=TextLoader)
        docs = loader.load()

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        return chunks
    except Exception as e:
        await Logger.error_log(__name__,'documents_chunking',e)
        return None



async def chatbot_prompt(company_name: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         f"""You are an intelligent and helpful chatbot assistant for {company_name}, assisting users on the company’s official website.

You will be given:
- Context: relevant information about the company’s services, products, and other details
- Metadata: may contain URLs, references, or additional resources
- Query: a message or question from a user about the company

Response formatting guidelines:

1. If the user is just greeting or not asking anything specific:
   - Respond warmly and politely.
   - Do not provide company information unless the user explicitly asks for it.

2. If the query is about the company’s services, products, offerings, or any related information:
   - Base your answer only on the provided context and metadata.
   - Use "- " (dash + space) for bullet points.
   - Keep each bullet point on a separate line.
   - Add blank lines between sections for better readability.
   - Include URLs or links wherever relevant and available in metadata or context.
   - Keep your tone concise, friendly, and professional.

3. Do not provide extra, assumed, or unrelated information.

4. If context does not contain the answer to any part of the query, politely mention that you do not have that specific information at the moment.

Always return a valid JSON response in the following format:
{{{{ "response": "<your formatted answer>" }}}}
"""),
        ("human",
         """Context:
{context}

Metadata:
{metadata}

Query:
{query}""")
    ])
    return prompt.partial(company_name=company_name)




# Step 4: Call the chain in your async route or function
async def gpt_response(context: List[dict], company_name: str, query: str):
    try:
        # Step 1: Aggregate context and metadata
        context_str = ""
        metadata_urls = []

        for item in context:
            context_text = item.get("context", "")
            metadata_url = item.get("metadata", {}).get("url", "")
            context_str += context_text.strip() + "\n\n"
            if metadata_url:
                metadata_urls.append(metadata_url)

        metadata_str = "\n".join(f"- {url}" for url in metadata_urls)

        # Step 2: Initialize LLM
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4.1-nano",
            temperature=0.4,
            max_tokens=700,
            max_retries=2,
        )

        # Step 3: Prepare prompt
        prompt = await chatbot_prompt(company_name)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        # Step 4: Call the chain
        result = await chain.ainvoke({
            "context": context_str,
            "metadata": metadata_str,
            "query": query
        })

        # Step 5: Parse JSON response from the model
        try:
            response = json.loads(result)
        except JSONDecodeError as je:
            await Logger.error_log(__name__, 'gpt_response', je)
            return {'response': 'Sorry! Can you please try again later'}
        except Exception as e:
            await Logger.error_log(__name__, 'gpt_response', e)
            return {'response': 'Sorry! Can you please try again later'}

        return response

    except Exception as e:
        await Logger.error_log(__name__, 'calling_gpt4o_instruct', e)
        return {'response': 'Something went wrong. Please try again later.'}

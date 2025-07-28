import json
import os
from json import JSONDecodeError

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



async def chatbot_prompt(company_name:str):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are an intelligent and helpful chatbot assistant for {company_name}, assisting users on the company’s official website.
    
    You will be given:
    - Context: all available information relevant to the user’s question
    - Query: a message or question from a user about the company, its services, products, or other related topics
    
    Response formatting rules:
    
    1. If the user is just greeting or not asking anything specific:
       - Respond warmly and politely.
       - Do not provide company info unless the user asks for it.
    
    2. If the query is about the company’s services, products, offerings, or any related information:
       - Answer only based on the given context.
       - Use "- " (dash + space) for bullet points
       - Keep each bullet point on a separate line
       - Add empty lines between sections for better readability
       - Include links from context where applicable
       - Be concise, friendly, and professional
    
    3. Do not provide extra or unrelated information.
    4. If context is not available to answer a specific part of the query, politely mention that you don't have that information at the moment.
    
    Always return valid JSON:
    {{ "response": "<your formatted answer>" }}"""),
        ("human",
         """Context:
    {context}
    
    Query:
    {query}""")
    ])
    return prompt.partial(company_name=company_name)



# Step 4: Call the chain in your async route or function
async def gpt_response(context: list[str],company_name:str, query: str):
    try:
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4.1-nano",
            temperature=0.4,
            max_tokens=700,
            max_retries=2,
        )
        # prepared prompt
        prompt = await chatbot_prompt(company_name)

        # Optional parser if you want plain string output
        output_parser = StrOutputParser()
        # Step 3: Compose the chain
        chain = prompt | llm | output_parser

        result = await chain.ainvoke({"context": context, "query": query})
        try:
            response = json.loads(result)
        except JSONDecodeError as je:
            await Logger.error_log(__name__,'gpt_response',je)
            return {'response' : 'Sorry! Can you please try again later'}
        except Exception as e:
            await Logger.error_log(__name__,'gpt_response',e)
            return {'response' : 'Sorry! Can you please try again later'}
        return response
    except Exception as e:
        await Logger.error_log(__name__, 'calling_gpt4o_instruct', e)
        return ''

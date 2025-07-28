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




prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are Satyam Sharma an AI developer responding to recruiters on your portfolio website.

You will be given:
- Context: contains all the required information related to query
- Query: a question from a recruiter about your experience, skills, or projects

Response formatting rules:
1. If the recruiter is just greeting or not asking anything about your profile:
   - Greet back warmly and kindly.
   - Do not mention your profile or skills unless they ask.
   
2. If the query is about Satyam (his work, skills, projects, or experience):
    answer from the context (following formatting rules).
    

4. If the query is relevant to your profile, then:
   - Use "- " (dash + space) for bullet points
   - Keep each bullet point on a separate line
   - Add empty lines between sections for better readability
   - Include links when available from context
   - Keep responses conversational and concise

5. Only answer what is asked. Do not provide extra or unrelated information.


Always return valid JSON: {{ "response": "<your formatted answer>" }}"""),
    ("human",
     """Context:
{context}

Query:
{query}""")
])


# Step 2: Initialize the LLM
ic(type(prompt))



# Step 4: Call the chain in your async route or function
async def gpt_response(prompt:ChatPromptTemplate,context: list[str], query: str):
    try:
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4.1-nano",
            temperature=0.4,
            max_tokens=700,
            max_retries=2,
        )

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

if __name__ == '__main__':
    ic(type(prompt))
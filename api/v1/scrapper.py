from icecream import ic
import uuid
from dotenv import load_dotenv
from fastapi import APIRouter,Request


from databases.chromaDB import ChromaDB
from schemas.schemas import WebsiteRequest

from utils.logger import Logger
from utils.utility import scrape_webpage, get_collection_name, docs_splitting

scrape_router = APIRouter()

load_dotenv()

@scrape_router.post('/scrape')
async def get_all_data(request:WebsiteRequest):
    try:
        website = request.website
        # get website links
        text,external_links = await scrape_webpage(website)
        ic(website)
        # load the text into vector_db
        collection_name= await get_collection_name(website)
        ic(collection_name)
        #1. convert text into docs using langchain
        all_chunks = await docs_splitting(text,external_links)
        if not all_chunks:
            await Logger.info_log('Error in creating the docs')
            raise ValueError
        #2. create collection into the cromadb
        await ChromaDB.create_collection(collection_name)

        # separate the docs, metadata and uuid
        documents = [chunk.page_content for chunk in all_chunks]
        metadatas = [chunk.metadata for chunk in all_chunks]

        ids = [str(uuid.uuid4()) for _ in all_chunks]  # Or your own ID strategy

        await ChromaDB.add_documents(collection_name=collection_name,
                                     ids=ids,
                                     documents=documents,
                                     metadatas=metadatas)
        data = {
            'collection_name' : collection_name
        }
        return {
            'data' : data,
            'status' : True
        }

    except Exception as e:
        await Logger.error_log(__name__,'get_all_data',e)
        return {
            'status' : False
        }







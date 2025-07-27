import os
from chromadb import AsyncHttpClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv

from utils.logger import Logger

load_dotenv()

class ChromaDB:
    _client = None
    _embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    @classmethod
    async def connect(cls):
        if cls._client is None:
            cls._client = await AsyncHttpClient(host=os.getenv("CHROMA_URI"))
            await Logger.info_log('Connection established')

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()

        return None

    @classmethod
    async def create_collection(cls, collection_name: str):

        collection = await cls._client.get_or_create_collection(
            name=collection_name,
            embedding_function=cls._embedding_function
        )
        await Logger.info_log(f"created collection - {collection_name}")
        return collection

    @staticmethod
    async def add_documents(collection_name: str, documents: list[str], ids: list[str], metadatas: list[dict] = None):
        collection = await ChromaDB._client.get_collection(name=collection_name)
        await collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    @staticmethod
    async def query_docs(collection_name: str, query_texts: list[str], n_results: int = 5,threshold_score:float=1.3) -> list:
        collection = await ChromaDB._client.get_collection(name=collection_name)
        results = await collection.query(
            query_texts=query_texts,
            n_results=n_results,

        )
        chunks = []
        if results.get('ids')[0]:
            for i,score in enumerate(results.get('distances')[0]):
                if score <= threshold_score:
                    chunks.append(results.get('documents')[0][i])


        return chunks

    @staticmethod
    async def get_all(collection_name: str,where_condition:dict):
        collection = await ChromaDB._client.get_collection(name=collection_name)
        return await collection.get(where= where_condition)

    @staticmethod
    async def delete_documents(collection_name: str, ids: list[str]):
        collection = await ChromaDB._client.get_collection(name=collection_name)
        await collection.delete(ids=ids)

    @staticmethod
    async def delete_collection(collection_name: str):
        await ChromaDB._client.delete_collection(name=collection_name)
        await Logger.info_log(f"Collection {collection_name} deleted successfully")

    @staticmethod
    async def list_collections():
        return await ChromaDB._client.list_collections()

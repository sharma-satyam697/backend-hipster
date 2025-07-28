import asyncio
import hashlib
import os

from databases.chromaDB import ChromaDB
from utils.logger import Logger


async def add_profile_data_croma(folder_path: str, collection_name: str):
    try:
        # Load all .txt or .md files from folder
        documents = []
        metadatas = []
        ids = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".txt", ".md")):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()

                    if not content:
                        continue

                    # Create a deterministic ID using hash (file path + content)
                    hash_id = hashlib.md5((file + content).encode('utf-8')).hexdigest()

                    # Avoid inserting if already exists
                    existing = await ChromaDB.get_all(collection_name, where_condition={"id": {"$eq": hash_id}})
                    if existing and existing.get("documents"):
                        continue  # Skip duplicate

                    documents.append(content)
                    metadatas.append({"source": full_path})
                    ids.append(hash_id)

        if documents:
            await ChromaDB.add_documents(
                collection_name=collection_name,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
    except Exception as e:
        await Logger.error_log(__name__,'add_profile_data_croma',e)


async def setup_chroma():
    await ChromaDB.connect()
    await ChromaDB.create_collection('profile')
    await add_profile_data_croma('knowledge_base/', 'profile')


if __name__ == '__main__':
    asyncio.run(setup_chroma())
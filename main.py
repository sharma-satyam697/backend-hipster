from contextlib import asynccontextmanager


# create collection first if does not exists named as 'profile'
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from add_all_documents import add_profile_data_croma
from api.v1.chat import chat_router
from api.v1.contact import contact_router
from databases.chromaDB import ChromaDB
from utils.logger import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await ChromaDB.connect()
        await ChromaDB.create_collection("profile")
        await add_profile_data_croma("knowledge_base/", "profile")

    except Exception as e:
        raise e

    yield  # FastAPI app runs...
    # On shutdown
    try:
        for collec in await ChromaDB.list_collections():
            await ChromaDB.delete_collection(collec.name)
    except Exception as e:
        await Logger.error_log(__name__,'lifespan',e)



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] if you're using React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router,prefix='/api/v1')
app.include_router(contact_router,prefix='/api/v1')


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
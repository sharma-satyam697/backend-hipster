from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from add_all_documents import add_profile_data_croma
from api.v1.chat import chat_router
from api.v1.scrapper import scrape_webpage, scrape_router
from databases.chromaDB import ChromaDB
from utils.logger import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await ChromaDB.connect()
    except Exception as e:
        print("Startup error:", e)  # ✅ Add this line for Docker logs
        raise e

    yield  # FastAPI app runs...
    # On shutdown
    try:
        for collec in await ChromaDB.list_collections():
            await ChromaDB.delete_collection(collec.name)
    except Exception as e:
        await Logger.error_log(__name__,'lifespan',e)
        print("Shutdown error:", e)  # ✅ Add this too



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] if you're using React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router,prefix='/api/v1')
app.include_router(scrape_router,prefix='/api/v1')


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
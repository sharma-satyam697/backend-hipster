import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from dotenv import load_dotenv
from fastapi import APIRouter,Request
from fastapi.exceptions import  HTTPException
from icecream import ic
from starlette.responses import JSONResponse

from knowledge_base.scrapper import get_internal_urls, get_external_urls, scrape_all
from schemas.schemas import ContactForm
from utils.logger import Logger

scrape_router = APIRouter()

load_dotenv()

@scrape_router.post('/scrape')
async def get_all_data(website:str):
    # get website links
    int_urls = get_internal_urls(website)
    ext_urls = get_external_urls(website)

    # scrape internal urls data
    text = scrape_all(int_urls)






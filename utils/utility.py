import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge_base.scrapper import get_internal_urls, get_external_urls, scrape_all
from utils.logger import Logger


async def scrape_webpage(url:str):
    try:
        int_urls  = get_internal_urls(url)
        ext_urls = get_external_urls(url)

        text = scrape_all(int_urls)
        return text,ext_urls
    except Exception as e:
        await Logger.error_log(__name__,'scrape_webpage',e)
        return '',[]


async def get_collection_name(website=None):
    try:
        match = re.search(r"https?://www\.([a-zA-Z0-9-]+)\.com", website)

        if match:
            collection_name = match.group(1)
        else:
            collection_name = 'website'
        return collection_name
    except Exception as e:
        await Logger.error_log(__name__,'get_collection_name',e)
        return 'website'



async def docs_splitting(web_data:list,ext_links:list,chunk_size=450,chunk_overlap=20):
    """
    Function to create the text chunking with a specific chunk size
    """
    try:
        all_chunks = []
        external_text = "If you'd like to explore more about this topic or learn further details about our company, you can visit the following links. They provide additional insights and trusted resources that may help answer your query more comprehensively."
        external_data = {
            'text' :external_text,
            'url' : "; ".join(ext_links)
        }
        web_data.append(external_data)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for web in web_data:
            text = web.get('text')
            metadata = {
                'url' : web.get('url')
            }
            chunks = text_splitter.create_documents([text], metadatas=[metadata])
            all_chunks.extend(chunks)
        # adding all external links of webpage
        return all_chunks
    except Exception as e:
        await Logger.error_log(__name__,'docs_splitting',e)
        return []



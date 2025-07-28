from pydantic import BaseModel, EmailStr


class QueryData(BaseModel):
    query : str
    company_name:str

class WebsiteRequest(BaseModel):
    website: str

from pydantic import BaseModel, EmailStr


class QueryData(BaseModel):
    query : str

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

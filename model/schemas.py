
from pydantic import BaseModel, EmailStr
from typing import Optional

class chatRequest(BaseModel):
    query : str
    history: list = []


class emailform(BaseModel):
    name : str
    email : EmailStr
    question : str
    message : Optional[str] = None




    
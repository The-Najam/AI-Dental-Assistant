
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class chatRequest(BaseModel):
    query : str
    history: list = []


class emailform(BaseModel):
    name : str
    email : EmailStr
    question : str
    message : Optional[str] = None


class Category(Enum):
    genuine_lead = "genuine_lead" 
    information_education = "information_education" 
    unrelated = "unrelated"



class Chat_Response(BaseModel):
    answer : str
    category : Category

    
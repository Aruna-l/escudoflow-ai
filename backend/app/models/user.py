from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    full_name: str
    organization: str
    email: EmailStr
    password: str
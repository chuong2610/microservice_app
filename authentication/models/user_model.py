from pydantic import BaseModel

class User(BaseModel):
    id: str 
    full_name: str
    password: str
    email: str
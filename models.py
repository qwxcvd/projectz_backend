from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    is_verified: bool = False

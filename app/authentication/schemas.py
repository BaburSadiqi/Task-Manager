from pydantic import BaseModel



class Token(BaseModel):
    """Schamse for response token"""
    token: str
    token_type: str

class TokenDate(BaseModel):
    username: str | None = None
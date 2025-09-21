from pydantic import BaseModel



class Token(BaseModel):
    """Schamse for response token"""
    access_token: str
    token_type: str

class TokenDate(BaseModel):
    username: str | None = None
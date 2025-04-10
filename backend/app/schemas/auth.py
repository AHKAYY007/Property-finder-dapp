from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class SignInMessage(BaseModel):
    message: str
    signature: str
    address: str
    nonce: str 
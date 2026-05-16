from pydantic import BaseModel

class UserPayload(BaseModel):
    email: str
    password: str

class CreateNotePayload(BaseModel):
    title: str
    content: str

class ShareNotePayload(BaseModel):
    email: str



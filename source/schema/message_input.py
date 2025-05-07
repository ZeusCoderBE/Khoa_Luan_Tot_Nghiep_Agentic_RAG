from pydantic import BaseModel
class MessageInput(BaseModel):
    session_id: int
    sender: str
    message: str
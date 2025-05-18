from pydantic import BaseModel
from typing import List, Optional

class MessageInput(BaseModel):
    session_id: int
    sender: str
    message: str
    references: Optional[List[str]] = None
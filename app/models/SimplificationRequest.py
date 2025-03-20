from pydantic import BaseModel


class SimplificationRequest(BaseModel):
    text: str

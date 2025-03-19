from pydantic import BaseModel, Field


class SimplificationRequest(BaseModel):
    text: str

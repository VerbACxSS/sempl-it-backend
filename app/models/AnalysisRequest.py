from pydantic import BaseModel


class TextAnalysisRequest(BaseModel):
    text: str


class ComparisonAnalysisRequest(BaseModel):
    text1: str
    text2: str

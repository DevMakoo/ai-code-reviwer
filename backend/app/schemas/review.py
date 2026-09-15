from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    language: str = Field(min_length=1)
    code: str = Field(min_length=1)


class Issue(BaseModel):
    severity: str
    category: str
    line: int
    message: str
    suggestion: str


class ReviewResponse(BaseModel):
    id: int
    language: str
    score: int
    summary: str
    issues: list[Issue]
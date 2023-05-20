import datetime

import pydantic


class QuizRequest(pydantic.BaseModel):
    """Quiz request arguments"""
    questions_num: int = pydantic.Field(ge=0)


class QuizResponse(pydantic.BaseModel):
    """Quiz response serializer"""
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

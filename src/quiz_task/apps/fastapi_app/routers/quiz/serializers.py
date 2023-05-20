import pydantic


class QuizRequest(pydantic.BaseModel):
    """Quiz request arguments"""
    questions_num: int = pydantic.Field(gt=0)

import pydantic
import datetime
import dateutil.parser


class JServiceQuiz(pydantic.BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

    @pydantic.validator('created_at', pre=True)
    def validate_datetime(cls, v):
        return dateutil.parser.isoparse(v)

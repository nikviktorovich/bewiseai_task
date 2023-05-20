import dataclasses
import datetime


@dataclasses.dataclass
class Quiz:
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

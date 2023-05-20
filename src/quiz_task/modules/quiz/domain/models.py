import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class Quiz:
    id: Any
    question: str
    answer: str
    created_at: datetime.datetime

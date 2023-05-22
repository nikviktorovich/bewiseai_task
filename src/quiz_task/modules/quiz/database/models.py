from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import TIMESTAMP

import quiz_task.database.base


class Quiz(quiz_task.database.base.Base):
    """Quiz table"""
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(type_=TIMESTAMP(timezone=True))

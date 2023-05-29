import datetime
from typing import List

import quiz_task.modules.quiz.domain.models
import quiz_task.modules.quiz.repositories
import quiz_task.services.unit_of_work
import quiz_task.services.quizzes
from . import common


data: List[quiz_task.modules.quiz.domain.models.Quiz] = [
    quiz_task.modules.quiz.domain.models.Quiz(
        id=1,
        question='Question 1',
        answer='Answer 1',
        created_at=datetime.datetime.utcnow(),
    ),
    quiz_task.modules.quiz.domain.models.Quiz(
        id=2,
        question='Question 2',
        answer='Answer 2',
        created_at=datetime.datetime.utcnow(),
    ),
    quiz_task.modules.quiz.domain.models.Quiz(
        id=3,
        question='Question 3',
        answer='Answer 3',
        created_at=datetime.datetime.utcnow(),
    ),
    quiz_task.modules.quiz.domain.models.Quiz(
        id=4,
        question='Question 4',
        answer='Answer 4',
        created_at=datetime.datetime.utcnow(),
    ),
    quiz_task.modules.quiz.domain.models.Quiz(
        id=5,
        question='Question 5',
        answer='Answer 5',
        created_at=datetime.datetime.utcnow(),
    ),
]


async def test_retrieve_unique_quizzes():
    fake_client = common.FakeClient(data)
    fake_repository = common.FakeQuizRepository([data[1], data[2]])
    fake_uow = common.FakeUnitOfWork(fake_repository)
    quizzes = await quiz_task.services.quizzes._retrieve_unique_quizzes(
        num_quizzes=2,
        uow=fake_uow,
        client=fake_client,
    )
    assert quizzes == [data[0], data[3]]

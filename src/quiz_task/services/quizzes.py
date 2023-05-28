from typing import List
from typing import Set

import quiz_task.modules.quiz.domain.models
import quiz_task.modules.quiz.unit_of_work
import quiz_task.services.jservice


# Max quizzes count per request
MAX_COUNT = 100


async def retrieve_unique_quizzes(
    num_quizzes: int,
    uow: quiz_task.modules.quiz.unit_of_work.QuizUnitOfWork,
) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
    """Retrieves specified amount of unique quizzes"""
    async with quiz_task.services.jservice.AsyncQuestionsAPIClient() as client:
        quizzes =  await _retrieve_unique_quizzes(num_quizzes, uow, client)
    
    quizzes = uow.quizzes.add_all(quizzes)
    return quizzes
        


async def _retrieve_unique_quizzes(
    num_quizzes: int,
    uow: quiz_task.modules.quiz.unit_of_work.QuizUnitOfWork,
    client: quiz_task.services.jservice.AbstractAsyncQuestionsAPIClient,
) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
    result_quizzes: List[quiz_task.modules.quiz.domain.models.Quiz] = []
    used_quizzes: Set[int] = set()

    while len(result_quizzes) < num_quizzes:
        count = min(num_quizzes - len(result_quizzes), MAX_COUNT)
        chunk = await client.random(count=count)

        # Filtering quizzes from already used ones during session
        unique_quizzes = [q for q in chunk if q.id not in used_quizzes]

        if not unique_quizzes:
            continue

        # Filtering quizzes from previously used ones (from DB)
        unique_quizzes = await _filter_quizzes(chunk, uow)

        result_quizzes.extend(unique_quizzes)
        used_quizzes.update(quiz.id for quiz in unique_quizzes)

    return result_quizzes


async def _filter_quizzes(
    quizzes: List[quiz_task.modules.quiz.domain.models.Quiz],
    uow: quiz_task.modules.quiz.unit_of_work.QuizUnitOfWork,
) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
    quiz_ids = [quiz.id for quiz in quizzes]
    non_unique_quizzes = await uow.quizzes.list_by_id_in(quiz_ids)
    non_unique_quizzes_set = set(quiz.id for quiz in non_unique_quizzes)
    return [quiz for quiz in quizzes if quiz.id not in non_unique_quizzes_set]

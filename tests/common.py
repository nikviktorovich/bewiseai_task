from typing import Dict
from typing import List

import quiz_task.common.errors
import quiz_task.modules.quiz.domain.models
import quiz_task.modules.quiz.repositories
import quiz_task.modules.quiz.unit_of_work
import quiz_task.services.jservice


class FakeClient(quiz_task.services.jservice.AbstractAsyncQuestionsAPIClient):
    data: List[quiz_task.modules.quiz.domain.models.Quiz]
    last_index: int = 0


    def __init__(
        self,
        data: List[quiz_task.modules.quiz.domain.models.Quiz],
    ) -> None:
        self.data = data


    async def random(
        self,
        count: int,
    ) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
        begin = self.last_index
        end = begin + count
        self.last_index += count
        return self.data[begin:end]


class FakeQuizRepository(quiz_task.modules.quiz.repositories.AbstractQuizRepository):
    quiz_set: Dict[int, quiz_task.modules.quiz.domain.models.Quiz]


    def __init__(
        self,
        data: List[quiz_task.modules.quiz.domain.models.Quiz],
    ) -> None:
        self.quiz_set = {quiz.id: quiz for quiz in data}
    

    def list(
        self,
        **filters,
    ) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
        return list(self.quiz_set.values())
    

    def get(
        self,
        quiz_id: int,
    ) -> quiz_task.modules.quiz.domain.models.Quiz:
        instance = self.quiz_set.get(quiz_id)

        if instance is None:
            raise quiz_task.common.errors.EntityNotFoundError(
                f'Unable to find a quiz with id={quiz_id}',
            )
        
        return instance
    

    def list_by_id_in(
        self,
        ids: List[int],
    ) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
        found = []
        for quiz_id in ids:
            if quiz_id in self.quiz_set:
                quiz = self.quiz_set[quiz_id]
                found.append(quiz)
        return found


    def add(
        self,
        instance: quiz_task.modules.quiz.domain.models.Quiz,
    ) -> quiz_task.modules.quiz.domain.models.Quiz:
        self.quiz_set[instance.id] = instance
        return instance
    

    def add_all(
        self,
        instances: List[quiz_task.modules.quiz.domain.models.Quiz],
    ) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
        for instance in instances:
            self.add(instance)
        return instances


class FakeUnitOfWork(quiz_task.modules.quiz.unit_of_work.AbstractQuizUnitOfWork):
    def __init__(self, repository: FakeQuizRepository) -> None:
        self.quizzes = repository


    def commit(self) -> None:
        pass


    def rollback(self) -> None:
        pass
    

    def __enter__(self) -> quiz_task.modules.quiz.unit_of_work.AbstractQuizUnitOfWork:
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        pass

from typing import List

import sqlalchemy.orm

import quiz_task.common.errors
import quiz_task.modules.quiz.database.models
from quiz_task.modules.quiz.domain import models


class AbstractQuizRepository:
    """Abstract quiz repository"""
    def list(self, **filters) -> List[models.Quiz]:
        """Returns list of all matching instances
        
        Args:
            filters: Keyword request filters
        """
        raise NotImplementedError()
    

    def get(self, quiz_id: int) -> models.Quiz:
        """Returns an instance with the specified id
        
        Raises:
            EntityNotFoundError: If unable to find the specified entity
        """
        raise NotImplementedError()
    

    def list_by_id_in(self, ids: List[int]) -> List[models.Quiz]:
        """Returns all instances which have their ids contained in the list"""
        raise NotImplementedError()


    def add(self, instance: models.Quiz) -> models.Quiz:
        """Adds an instance to repository"""
        raise NotImplementedError()
    

    def add_all(self, instances: List[models.Quiz]) -> List[models.Quiz]:
        """Adds many instances to repository"""
        raise NotImplementedError()


class SQLAlchemyQuizRepository(AbstractQuizRepository):
    """Quiz repository implementation bound to SQLAlchemy session"""
    session: sqlalchemy.orm.Session


    def __init__(self, session: sqlalchemy.orm.Session) -> None:
        self.session = session


    def _get_instance_set(self) -> sqlalchemy.orm.Query:
        return self.session.query(models.Quiz)


    def list(self, **filters) -> List[models.Quiz]:
        instances = self._get_instance_set().filter_by(**filters).all()
        return instances
    

    def get(self, quiz_id: int) -> models.Quiz:
        instance = self._get_instance_set().filter_by(id=quiz_id).first()
        
        if instance is None:
            raise quiz_task.common.errors.EntityNotFoundError(
                f'Unable to find a quiz with id={quiz_id}',
            )
        
        return instance
    

    def list_by_id_in(self, ids: List[int]) -> List[models.Quiz]:
        instances = self._get_instance_set().filter(
            quiz_task.modules.quiz.database.models.Quiz.id.in_(ids)
        )
        return instances.all()
    

    def add(self, instance: models.Quiz) -> models.Quiz:
        self.session.add(instance)
        return instance
    

    def add_all(self, instances: List[models.Quiz]) -> List[models.Quiz]:
        self.session.add_all(instances)
        return instances

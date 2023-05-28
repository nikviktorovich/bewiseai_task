from typing import List

import sqlalchemy.orm
import sqlalchemy.ext.asyncio
from sqlalchemy import select

import quiz_task.common.errors
import quiz_task.modules.quiz.database.models
from quiz_task.modules.quiz.domain import models


class QuizRepository:
    """Abstract quiz repository"""
    async def list(self, **filters) -> List[models.Quiz]:
        """Returns list of all matching instances
        
        Args:
            filters: Keyword request filters
        """
        raise NotImplementedError()
    

    async def get(self, quiz_id: int) -> models.Quiz:
        """Returns an instance with the specified id
        
        Raises:
            EntityNotFoundError: If unable to find the specified entity
        """
        raise NotImplementedError()
    

    async def list_by_id_in(self, ids: List[int]) -> List[models.Quiz]:
        """Returns all instances which have their ids contained in the list"""
        raise NotImplementedError()


    def add(self, instance: models.Quiz) -> models.Quiz:
        """Adds an instance to repository"""
        raise NotImplementedError()
    

    def add_all(self, instances: List[models.Quiz]) -> List[models.Quiz]:
        """Adds many instances to repository"""
        raise NotImplementedError()


class SQLAlchemyQuizRepository(QuizRepository):
    """Quiz repository implementation bound to SQLAlchemy session"""
    session: sqlalchemy.ext.asyncio.AsyncSession


    def __init__(self, session: sqlalchemy.ext.asyncio.AsyncSession) -> None:
        self.session = session


    async def list(self, **filters) -> List[models.Quiz]:
        q = select(models.Quiz).filter_by(**filters)
        scalars = await self.session.scalars(q)
        instances = scalars.all()
        return list(instances)
    

    async def get(self, quiz_id: int) -> models.Quiz:
        q = select(models.Quiz).filter_by(id=quiz_id).limit(1)
        scalars = await self.session.scalars(q)
        instance = scalars.first()
        
        if instance is None:
            raise quiz_task.common.errors.EntityNotFoundError(
                f'Unable to find a quiz with id={quiz_id}',
            )
        
        return instance
    

    async def list_by_id_in(self, ids: List[int]) -> List[models.Quiz]:
        q = select(models.Quiz).where(
            quiz_task.modules.quiz.database.models.Quiz.id.in_(ids)
        )
        scalars = await self.session.scalars(q)
        instances = scalars.all()
        return list(instances)
    

    def add(self, instance: models.Quiz) -> models.Quiz:
        self.session.add(instance)
        return instance
    

    def add_all(self, instances: List[models.Quiz]) -> List[models.Quiz]:
        self.session.add_all(instances)
        return instances

from typing import Optional

import sqlalchemy.ext.asyncio
import sqlalchemy.orm

import quiz_task.config
from quiz_task.modules.quiz import repositories


class AbstractQuizUnitOfWork:
    quizzes: repositories.AbstractQuizRepository


    async def commit(self) -> None:
        raise NotImplementedError()
    

    async def rollback(self) -> None:
        raise NotImplementedError()
    

    async def __aenter__(self) -> 'AbstractQuizUnitOfWork':
        raise NotImplementedError()
    

    async def __aexit__(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class SQLAlchemyQuizUnitOfWork(AbstractQuizUnitOfWork):
    session_factory: sqlalchemy.ext.asyncio.async_sessionmaker
    session: sqlalchemy.ext.asyncio.AsyncSession


    def __init__(
        self,
        engine: Optional[sqlalchemy.ext.asyncio.AsyncEngine] = None,
    ) -> None:
        if engine is None:
            engine = quiz_task.config.get_database_engine()
        
        self.session_factory = sqlalchemy.ext.asyncio.async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )
    

    async def commit(self) -> None:
        await self.session.commit()
    

    async def rollback(self) -> None:
        await self.session.rollback()
    

    async def __aenter__(self) -> 'AbstractQuizUnitOfWork':
        self.session: sqlalchemy.ext.asyncio.AsyncSession = self.session_factory()
        self.quizzes = repositories.SQLAlchemyQuizRepository(self.session)
        return self
    

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close()

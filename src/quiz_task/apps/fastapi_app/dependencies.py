import sqlalchemy.ext.asyncio
from fastapi import Depends

import quiz_task.config
import quiz_task.modules.quiz.unit_of_work


def get_database_engine() -> sqlalchemy.ext.asyncio.AsyncEngine:
    connection_url = quiz_task.config.get_postgres_connection_url()
    engine = sqlalchemy.ext.asyncio.create_async_engine(url=connection_url)
    return engine


async def get_uow(
    engine: sqlalchemy.ext.asyncio.AsyncEngine = Depends(get_database_engine),
):
    uow = quiz_task.modules.quiz.unit_of_work.SQLAlchemyQuizUnitOfWork(engine)
    async with uow:
        yield uow

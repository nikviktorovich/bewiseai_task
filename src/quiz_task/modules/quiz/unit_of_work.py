from typing import Optional

import sqlalchemy
import sqlalchemy.orm

import quiz_task.config
from quiz_task.modules.quiz import repositories


class AbstractQuizUnitOfWork:
    quizzes: repositories.AbstractQuizRepository


    def commit(self) -> None:
        raise NotImplementedError()
    

    def rollback(self) -> None:
        raise NotImplementedError()
    

    def __enter__(self) -> 'AbstractQuizUnitOfWork':
        raise NotImplementedError()
    

    def __exit__(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class SQLAlchemyQuizUnitOfWork(AbstractQuizUnitOfWork):
    session_factory: sqlalchemy.orm.sessionmaker
    session: sqlalchemy.orm.Session


    def __init__(
        self,
        engine: Optional[sqlalchemy.engine.Engine] = None,
    ) -> None:
        if engine is None:
            engine = quiz_task.config.get_database_engine()
        
        self.session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    

    def commit(self) -> None:
        self.session.commit()
    

    def rollback(self) -> None:
        self.session.rollback()
    

    def __enter__(self) -> 'AbstractQuizUnitOfWork':
        self.session = self.session_factory()
        self.quizzes = repositories.SQLAlchemyQuizRepository(self.session)
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()

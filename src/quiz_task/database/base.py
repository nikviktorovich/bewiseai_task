import sqlalchemy.orm

import quiz_task.config


Base = sqlalchemy.orm.declarative_base(
    bind=quiz_task.config.get_database_engine(),
)

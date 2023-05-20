import sqlalchemy.orm

import quiz_task.modules.quiz.database.models
import quiz_task.modules.quiz.domain.models


def start_mappers() -> None:
    """Starts orm to domain model mappers"""
    registry = sqlalchemy.orm.registry()

    registry.map_imperatively(
        quiz_task.modules.quiz.domain.models,
        quiz_task.modules.quiz.database.models,
    )

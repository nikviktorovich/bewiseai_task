import quiz_task.modules.quiz.unit_of_work


def get_uow():
    with quiz_task.modules.quiz.unit_of_work.SQLAlchemyQuizUnitOfWork() as uow:
        yield uow

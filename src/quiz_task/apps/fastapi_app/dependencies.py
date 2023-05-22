import quiz_task.modules.quiz.unit_of_work


async def get_uow():
    uow = quiz_task.modules.quiz.unit_of_work.SQLAlchemyQuizUnitOfWork()
    async with uow:
        yield uow

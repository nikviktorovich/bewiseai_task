import fastapi
from fastapi import Depends

import quiz_task.services.quizzes
from quiz_task.apps.fastapi_app import dependencies
from quiz_task.apps.fastapi_app.routers.quiz import serializers
from quiz_task.modules.quiz import unit_of_work


router = fastapi.routing.APIRouter()


@router.post('/quiz')
async def obtain_questions(
    quiz_request: serializers.QuizRequest,
    uow: unit_of_work.QuizUnitOfWork = Depends(dependencies.get_uow),
):
    quizzes = await quiz_task.services.quizzes.retrieve_unique_quizzes(
        num_quizzes=quiz_request.questions_num,
        uow=uow,
    )
    await uow.commit()

    return [serializers.QuizResponse.from_orm(quiz) for quiz in quizzes]

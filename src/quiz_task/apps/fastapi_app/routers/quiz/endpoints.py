import fastapi

from quiz_task.apps.fastapi_app.routers.quiz import serializers


router = fastapi.routing.APIRouter()


@router.post('/quiz')
def obtain_questions(quiz_request: serializers.QuizRequest):
    ...

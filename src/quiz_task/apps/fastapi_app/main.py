import fastapi
import fastapi.responses
from fastapi import status

import quiz_task.apps.fastapi_app.routers.quiz.endpoints
import quiz_task.common.errors
import quiz_task.database.mappers


def on_startup():
    quiz_task.database.mappers.start_mappers()


app = fastapi.FastAPI(on_startup=[on_startup])


@app.exception_handler(quiz_task.common.errors.EntityNotFoundError)
def handle_entity_not_found_error(request, exception):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=str(exception),
    )


# Routers
app.include_router(quiz_task.apps.fastapi_app.routers.quiz.endpoints.router)

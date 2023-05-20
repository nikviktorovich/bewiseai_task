import fastapi

import quiz_task.apps.fastapi_app.routers.quiz.endpoints
import quiz_task.database.mappers


def on_startup():
    quiz_task.database.mappers.start_mappers()


app = fastapi.FastAPI(on_startup=[on_startup])

# Routers
app.include_router(quiz_task.apps.fastapi_app.routers.quiz.endpoints.router)

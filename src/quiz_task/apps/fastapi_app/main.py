import fastapi

import quiz_task.apps.fastapi_app.routers.quiz.endpoints


app = fastapi.FastAPI()

# Routers
app.include_router(quiz_task.apps.fastapi_app.routers.quiz.endpoints.router)

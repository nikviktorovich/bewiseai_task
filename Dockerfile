FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/src
RUN pip install -e /code/src
CMD ["uvicorn", "quiz_task.apps.fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

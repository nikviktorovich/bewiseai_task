# Overview
This is a test task from _bewise.ai_ company

# Installation and deployment
To install and deploy this project you'll need Docker (`https://docs.docker.com/engine/install/`).

The first step is cloning the repository:
```bash
git clone https://github.com/nikviktorovich/bewiseai_task.git
cd bewiseai_task
```

The next step is running `docker compose`:
```bash
POSTGRES_DB=bewiseaidb \
POSTGRES_USER=testuser \
POSTGRES_PASSWORD=testuser \
docker compose up -d
```

Another options is to store the environment variables inside, for example, `.env` file. 
In this case, the command above will look like this:
```bash
docker compose --env-file .env up -d
```

...and `.env` file would look like this:
```
POSTGRES_DB=bewiseaidb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testuser
```

And this is pretty much it! After succesful deployment you can navigate to `http://127.0.0.1:8000/docs` in your browser and use the interactive documentation. As an alternative option, you might wanna use CLI tools:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/quiz' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"questions_num": 3}'
```

To stop and remove the containers use:
```bash
docker compose down
```

# Endpoints
## __`/quiz`__
### Overview
This endpoint returns specified number of unique quizzes, obtained from `jservice.io/api/random`

### Methods
- `POST`

JSON Schema:
```
{
    "questions_num": integer
}
```

Example JSON:
```json
{
    "questions_num": 3
}
```


# Database
## Tables
### `quizzes`
#### Overview
This table contains quizzes

#### Fields
- `id` - Integer, primary key
- `question` - Varchar (string)
- `answer` - Varchar (string)
- `created_at` - Timestamp (datetime)

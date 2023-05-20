from typing import Any
from typing import List
from typing import Optional

import aiohttp

import quiz_task.modules.quiz.domain.models
from quiz_task.services.jservice import serializers


API_ROOT = 'https://jservice.io/'


class AsyncQuestionsAPIClient:
    session: aiohttp.ClientSession


    async def __aenter__(
        self,
        api_root: Optional[str] = API_ROOT,
    ) -> 'AsyncQuestionsAPIClient':
        self.session = aiohttp.ClientSession(api_root)
        return self
    

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close()
    

    async def get(self, endpoint: str, **params) -> Any:
        """Makes a GET request to JService.io endpoint
        
        Raises:
            ValueError: If response status code != 200
        """
        async with self.session.get(endpoint, params=params) as resp:
            resp_json = await resp.json()
            if resp.status != 200:
                raise ValueError(resp_json.get('error', 'Error'))
        return resp_json


    async def random(
        self,
        count: int,
    ) -> List[quiz_task.modules.quiz.domain.models.Quiz]:
        """Retrieves a list of quizzes from JService.io"""
        resp_json: List[Any] = await self.get('/api/random', count=count)
        
        quizzes: List[quiz_task.modules.quiz.domain.models.Quiz] = []
        for quiz_json in resp_json:
            parsed_quiz = serializers.JServiceQuiz(**quiz_json)
            domain_quiz = quiz_task.modules.quiz.domain.models.Quiz(
                id=parsed_quiz.id,
                question=parsed_quiz.question,
                answer=parsed_quiz.answer,
                created_at=parsed_quiz.created_at,
            )
            quizzes.append(domain_quiz)
        
        return quizzes

import pytest

import quiz_task.services.jservice


@pytest.fixture(scope='function')
async def jservice_client():
    async with quiz_task.services.jservice.AsyncQuestionsAPIClient() as client:
        yield client

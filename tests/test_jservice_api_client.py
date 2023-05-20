import pytest

import quiz_task.services.jservice


@pytest.mark.usefixtures('jservice_client')
async def test_random_quizzes(
    jservice_client: quiz_task.services.jservice.AsyncQuestionsAPIClient,
):
    quizzes = await jservice_client.random(count=3)
    assert len(quizzes) == 3

    with pytest.raises(ValueError):
        await jservice_client.random(count=-1)

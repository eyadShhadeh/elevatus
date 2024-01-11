from unittest.mock import Mock
from src.models.generic import APIResponse
from src.models.user import User
from fastapi import status
from uuid import uuid4


def test_get_single_user(client: Mock, around: None) -> None:

    response = client.get(f"/user/{uuid4()}")

    api_response: APIResponse[User] = APIResponse.parse_obj(response.json())
    user_response = User.parse_obj(api_response.results)
    assert response.status_code == status.HTTP_200_OK
    assert type(user_response) is str

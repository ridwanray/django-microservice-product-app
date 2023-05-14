import pytest
from rest_framework.test import APIClient
from micro_shared_lib.authentication.auth import UserData
from pytest_factoryboy import register
from .factories import ProductFactory

register(ProductFactory)


@pytest.fixture
def api_client():
    return APIClient()


def api_client_with_credentials(api_client):
    """No need for actual token since Auth service is mocked"""
    return api_client.credentials(HTTP_AUTHORIZATION="Bearer " + "sth-random")


@pytest.fixture
def user_with_specific_permission(mocker):
    def _user(is_admin=False):
        mock_auth = mocker.patch("micro_shared_lib.authentication.auth.get_auth_user")
        mocked_user_data = {
            "id": "def93efb-18c5-4c5e-a8d3-9092675ee3e6",
            "username": "ray",
            "email": "ridwanray@ridwanray.com",
            "firstname": "Ridwan",
            "lastname": "Yusuf",
            "is_admin": is_admin,
        }
        mock_auth.return_value = UserData(mocked_user_data)
        return UserData(mocked_user_data)

    return _user

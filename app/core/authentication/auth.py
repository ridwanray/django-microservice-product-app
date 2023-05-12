import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework import serializers
from decouple import config


class UserData(object):
    is_authenticated = True

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def get_auth_user(token):
    # auth_service_url = config('AUTH_URL')
    auth_service_url = 'http://172.19.0.2:8000'
    auth_decode_url = f'{auth_service_url}/api/v1/auth/decode/'
    headers = {'Accept': 'application/json', 'Authorization': f'Bearer {str(token)}',
               'Content-Type': 'application/json'}
    data = {'token': str(token)}
    try:
        res = requests.request(method="POST", url=auth_decode_url, json=data, headers=headers)

    except requests.ConnectionError as err:
        raise serializers.ValidationError(f"Cannot establish connection: {err}") from err

    except requests.HTTPError as err:
        raise serializers.ValidationError(f"HTTP Error: {err}") from err
    except Exception as err:
        raise serializers.ValidationError(f"Error occurred: {err}") from err

    if 200 <= res.status_code < 300:
        return UserData(res.json())
    else:
        raise AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token):
        return raw_token.decode()

    def get_user(self, validated_token):
        return get_auth_user(validated_token)


class CustomJWTAuthenticationScheme(SimpleJWTScheme):
    target_class = CustomJWTAuthentication



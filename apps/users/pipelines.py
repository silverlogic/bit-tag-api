import re
from io import BytesIO

from django.core.files.images import ImageFile

import requests
from avatar.models import Avatar


class EmailAlreadyExistsError(Exception):
    pass


class EmailNotProvidedError(Exception):
    pass


def get_username(strategy, details, response, user=None, *args, **kwargs):
    storage = strategy.storage

    if not user:
        if details.get('email'):
            username = details['email']
        elif strategy.request.data.get('email'):
            username = strategy.request.data['email']
        else:
            raise EmailNotProvidedError()

        if storage.user.user_exists(username=username):
            raise EmailAlreadyExistsError()
    else:
        username = storage.user.get_username(user)
    return {'username': username}


def set_avatar(is_new, backend, user, response, *args, **kwargs):
    if not is_new:
        return

    image_url = None
    image_params = {}

    if backend.name == 'facebook':
        image_url = 'https://graph.facebook.com/v2.7/me/picture'
        image_params = {'type': 'large', 'access_token': response['access_token']}

    if image_url:
        response = requests.get(image_url, params=image_params)
        image = BytesIO(response.content)
        Avatar.objects.create(user=user, primary=True, avatar=ImageFile(image, name='pic.jpg'))


def set_is_new(is_new, user, *args, **kwargs):
    user.is_new = is_new

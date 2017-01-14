from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from requests import HTTPError
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_social_auth.views import SocialTokenOnlyAuthView, decorate_request
from social.exceptions import AuthException
from social.utils import user_is_authenticated

from .serializers import FacebookSerializer


class SocialAuthViewSet(SocialTokenOnlyAuthView, viewsets.GenericViewSet):
    serializer_class = FacebookSerializer

    def create(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    @method_decorator(never_cache)
    def do(self, request, *args, **kwargs):
        input_data = self.get_serializer_in_data()
        self.set_input_data(request, input_data)
        decorate_request(request, 'facebook')
        serializer = self.get_serializer(data=input_data)
        serializer.is_valid(raise_exception=True)
        try:
            user = self.get_object()
        except (AuthException, HTTPError) as e:
            return self.respond_error(e)
        if isinstance(user, HttpResponse):  # An error happened and pipeline returned HttpResponse instead of user
            return user
        self.get_serializer(instance=user)
        self.do_login(request.backend, user)
        return Response({'token': Token.objects.get_or_create(user=user)[0].key})

    def get_object(self):
        user = self.request.user
        is_authenticated = user_is_authenticated(user)
        user = is_authenticated and user or None

        # skip checking state by setting following params to False
        # it is responsibility of front-end to check state
        # TODO: maybe create an additional resource, where front-end will
        # store the state before making a call to oauth provider
        # so server can save it in session and consequently check it before
        # sending request to acquire access token.
        # In case of token authentication we need a way to store an anonymous
        # session to do it.
        self.request.backend.REDIRECT_STATE = False
        self.request.backend.STATE_PARAMETER = False

        access_token = self.request.auth_data.get('access_token')
        user = self.request.backend.do_auth(access_token)

        return user

    def respond_error(self, error):
        if isinstance(error, (AuthException, HTTPError)):
            raise serializers.ValidationError({'non_field_errors': 'invalid_credentials'})
        return Response(status=status.HTTP_400_BAD_REQUEST)

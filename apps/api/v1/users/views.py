from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters, mixins, permissions, response, serializers, viewsets
from rest_framework.decorators import detail_route, list_route

from apps.users.models import User

from .serializers import UserSerializer


class UpdateSelfPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH'):
            if not request.user.is_authenticated() or request.user != obj:
                return False
        return True


class UsersViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (UpdateSelfPermission,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name',)

    @list_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return response.Response(serializer.data)

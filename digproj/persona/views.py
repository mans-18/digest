from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Kollege, Event, Persona

from persona import serializers


class BasePersonaAttrViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    """Base viewset for user owned persona attr"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


# Gone use only list mixin. There are update, delete mixins ...
class KollegeViewSet(BasePersonaAttrViewSet):
    """Manage kollegen in the db"""
    # ListModeMixin requires a queryset set
    queryset = Kollege.objects.all()
    serializer_class = serializers.KollegeSerializer

    def get_queryset(self):
        """Return objects for current auth user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class EventViewSet(BasePersonaAttrViewSet):
    """Manage events in the db"""
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('title')


# Gonna implement more functionalities here not only list
class PersonaViewSet(viewsets.ModelViewSet):
    """Manage persona in the db"""
    serializer_class = serializers.PersonaSerializer
    queryset = Persona.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the personas for the auth user"""
        return self.queryset.filter(user=self.request.user).order_by('name')

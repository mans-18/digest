from rest_framework import serializers

from core.models import Kollege, Event, Persona


class KollegeSerializer(serializers.ModelSerializer):
    """Serializer for equipe objects"""

    class Meta:
        model = Kollege
        fields = ('id', 'name', 'crm')
        read_only_fields = ('id',)


class EventSerializer(serializers.ModelSerializer):
    """ Serializer for event objects"""

    class Meta:
        model = Event
        fields = ('id', 'title', 'start', 'color', 'insurance', 'comment')
        read_only_fields = ('id',)


class PersonaSerializer(serializers.ModelSerializer):
    """Serializer for persona obj"""
    events = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Event.objects.all()
    )
    kollegen = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Kollege.objects.all()
    )

    class Meta:
        model = Persona
        fields = ('id', 'name', 'mobile', 'whatsapp', 'telephone', 'email',
                  'street', 'complement', 'postalcode', 'dob', 'registerdate',
                  'comment', 'kollegen', 'events'
                  )
        read_only_fields = ('id',)

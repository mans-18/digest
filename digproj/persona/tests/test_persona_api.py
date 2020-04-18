from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Persona

from persona.serializers import PersonaSerializer


PERSONA_URL = reverse('persona:persona-list')


# ** means that any additional args other than user will be passed as a dict
# called params
def sample_persona(user, **params):
    """Create and return a sample persona"""
    defaults = {
        'name': 'Miguel',
        'mobile': '5585999568827'
    }
    defaults.update(params)

    return Persona.objects.create(user=user, **defaults)


class PublicPersonaApiTests(TestCase):
    """Test unauthenticated persona api access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required"""
        res = self.client.get(PERSONA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePersonaApiTests(TestCase):
    """Test auth persona api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@ufc.br',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_personas(self):
        """Test retrieving a list of personas"""
        # Error: Positional args follow kw args
        # sample_recipe(user=self.user, {
        #    'title': '',
        #    'time_minutes': 10,
        #    'price': 5.00
        # })
        # sample_recipe(user=self.user, {
        #    'title': '',
        #    'time_minutes': 20,
        #    'price': 10.00
        # })
        # ##### Accepted this one. Lets see!!! #######
        # sample_recipe({
        #    'title': 'Fried fish',
        #    'time_minutes': 10,
        #    'price': 5.00
        # TypeError: sample_recipe() got multiple values for argument 'user'
        # }, user=self.user)
        sample_persona(user=self.user)
        sample_persona(user=self.user)

        res = self.client.get(PERSONA_URL)

        # If don't order_by('-id'), no error: AssertionError: [OrderedDict
        # ([('id', 4), ('title', 'Sample recipe'), ('time_mi[221 chars]])])] !=
        # [OrderedDict([('id', 5), ('title', 'Sample recipe'), ('time_mi[221
        # chars]])])]
        # recipes = Recipe.objects.all().order_by('-id')
        personas = Persona.objects.all().order_by('name')
        serializer = PersonaSerializer(personas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_personas_limited_to_user(self):
        """Test retrieving personas for auth user only"""
        user2 = get_user_model().objects.create_user(
            'other@ufc.br',
            'pasrd'
        )
        sample_persona(user=user2)
        sample_persona(user=self.user)

        res = self.client.get(PERSONA_URL)

        personas = Persona.objects.filter(user=self.user)
        serializer = PersonaSerializer(personas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

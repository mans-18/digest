from django.urls import path, include
from rest_framework.routers import DefaultRouter

from persona import views


# The DefaultRouter auto generates the urls for a viewset.
# One viewset may have multiple urls.
router = DefaultRouter()
router.register('kollegen', views.KollegeViewSet)
router.register('events', views.EventViewSet)
router.register('persona', views.PersonaViewSet)
# So the reverse function may find
app_name = 'persona'

urlpatterns = [
    # router.urls NOT a str
    path('', include(router.urls)),
]

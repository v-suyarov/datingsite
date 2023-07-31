from django.urls import path, include
from .views import ParticipantCreateAPIView


urlpatterns = [
    path('clients/create/', ParticipantCreateAPIView.as_view()),
]

from django.urls import path, include
from .views import ParticipantCreateAPIView, ParticipantListView

urlpatterns = [
    path('clients/create/', ParticipantCreateAPIView.as_view()),
    path('list/', ParticipantListView.as_view(), name='participant-list'),
]

from django.urls import path, include
from .views import ParticipantCreateAPIView, ParticipantListView, ParticipantRateUpdateAPIView

urlpatterns = [
    path('clients/create/', ParticipantCreateAPIView.as_view()),
    path('list/', ParticipantListView.as_view(), name='participant-list'),
    path('clients/<int:pk>/rate/', ParticipantRateUpdateAPIView.as_view(), name='participant-rate'),
]

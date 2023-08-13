from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import ParticipantCreateAPIView, ParticipantListView, ParticipantMatchUpdateAPIView

urlpatterns = [
    path('v1/clients/create/', ParticipantCreateAPIView.as_view()),
    path('v1/list/', ParticipantListView.as_view(), name='participant-list'),
    path('v1/clients/<int:pk>/match/', ParticipantMatchUpdateAPIView.as_view(), name='participant-match'),
    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

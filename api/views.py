from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from clients.models import Participant
from clients.serializers import ParticipantSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from django.db.models import F, Func


class ParticipantCreateAPIView(CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        response.data = {"message": "Вы успешно создали профиль на Datingsite,"
                                    " пожалуйста запомните логин и пароль, которые вы указали при регистрации.",
                         "data": response.data}
        return response


class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.prefetch_related("likes")
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['gender', 'first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name', 'gender']
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        max_distance = self.request.query_params.get('distance', None)

        if max_distance:
            auth_participant = self.request.user.participant

            queryset = queryset.annotate(fact_distance=Distance(
                Point(float(auth_participant.longitude), float(auth_participant.latitude), srid=4326),
                Func(F('longitude'), F('latitude'), 4326, function='ST_Point', output_field=PointField()))
            ).filter(fact_distance__lt=float(max_distance))

        return queryset

from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from api.schemas import participant_create_schema, participant_match_schema, participant_list_schema
from clients.models import Participant
from clients.serializers import ParticipantSerializer, ParticipantMathSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F, Func


@participant_create_schema
class ParticipantCreateAPIView(CreateAPIView):
    """
    Создать нового пользователя
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        response.data = {"message": "Вы успешно создали профиль на Datingsite,"
                                    " пожалуйста запомните логин и пароль, которые вы указали при регистрации",
                         "data": response.data}
        return response


@participant_list_schema
class ParticipantListView(ListAPIView):
    """
    Получить список участников на основе фильтрации и сортировки по полу, имени и фамилии.
    Позволяет фильтровать список участников на основе расстояния до авторизованного пользователя
    """
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
            ).filter(fact_distance__lte=float(max_distance))

        return queryset


@participant_match_schema
class ParticipantMatchUpdateAPIView(UpdateAPIView):
    """
    Добавляет участника с ID в список понравившихся
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantMathSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Participant, pk=request.user.pk)
        serializer = self.get_serializer(instance, data=request.data, context=kwargs, partial=True)
        serializer.is_valid(raise_exception=True)
        evaluated = Participant.objects.get(pk=serializer.context.get('pk'))
        sympathy_before = serializer.instance.likes.contains(evaluated)
        self.perform_update(serializer)

        message = "вы успешно оценили выбранного участника"

        if sympathy_before:
            message = "вы уже оценивали выбранного участника"
        elif evaluated.likes.contains(serializer.instance):
            message = "у вас возникла взаимная симпатия, сообщеня с информацией были отправлены вам на почту"
        return Response({"message": message})

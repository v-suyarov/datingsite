from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from clients.models import Participant
from clients.serializers import ParticipantSerializer


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

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import inline_serializer, extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import status, serializers

from clients.models import GENDER_CHOICES
from clients.serializers import ParticipantSerializer

responseError = inline_serializer(
            name='ResponseError',
            fields={
                'details': serializers.DictField(
                    child=serializers.CharField()
                ),
                'code': serializers.IntegerField()
            })

participant_create_schema = extend_schema(
    summary="Создать нового пользователя",
    examples=[
        OpenApiExample(
            'Response valid example 1',
            summary='успешный ответ',
            value={
                'message': 'Вы успешно создали профиль на Datingsite, '
                           'пожалуйста запомните логин и пароль, которые вы указали при регистрации',
                'data': {
                    'first_name': 'string',
                    'last_name': 'string',
                    'gender': 'string',
                    'avatar': 'string',
                }
            },
            response_only=True,
            status_codes=[status.HTTP_201_CREATED]
        ),
        OpenApiExample(
            'Response error example 1',
            summary='ответ при ошибке',
            value={
                "details": {
                    "key_error_1": "string",
                    "key_error_2": "string",
                    "key_error_N": "string"
                },
                "code": 0
            },
            response_only=True,
            status_codes=["default"]
        )
    ],
    request={"multipart/form-data": ParticipantSerializer()},
    responses={
        status.HTTP_201_CREATED: ParticipantSerializer,
        'default': responseError,

    }
)

participant_list_schema = extend_schema(
    summary="Получить список участников",
    parameters=[
        OpenApiParameter(
            name='first_name',
            description='имя участника',
        ),
        OpenApiParameter(
            name='last_name',
            description='фамилия участника',
        ),
        OpenApiParameter(
            name='gender',
            enum=[gender for gender, _ in GENDER_CHOICES],
            description='пол участника',

        ),
        OpenApiParameter(
            name='distance',
            description='при заполнении этого поля будет получен список участников, '
                        'где расстояние в км между участником и авторизованным пользователем '
                        'не больше чем заданное значение',
        ),
        OpenApiParameter(
            name='ordering',
            description='поле по которому будет отсортирован список участников, например: '
                        'first_name или -first_name для обратной сортировки',
        ),

    ],
    responses={
        status.HTTP_200_OK: ParticipantSerializer,
        'default': responseError,

    }
)

participant_match_schema = extend_schema(
    summary="Добавить участика в понравившееся",
    parameters=[
        OpenApiParameter(
            name='id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID понравившегося участника',
        ),
    ],
    examples=[
        OpenApiExample(
            'Valid example 1',
            summary='односторонняя симпатия',
            value={
                'message': 'вы успешно оценили выбранного участника',
            },
        ),
        OpenApiExample(
            'Valid example 2',
            summary='взаимная симпатия',
            value={
                'message': 'у вас возникла взаимная симпатия, сообщеня с информацией были отправлены вам на почту',
            }
        ),
        OpenApiExample(
            'Valid example 3',
            summary='повторная симпатия',
            value={
                'message': 'вы уже оценивали выбранного участника',
            }
        )
    ],
    responses={
        status.HTTP_200_OK: inline_serializer(
            name='ParticipantMatch',
            fields={
                'message': serializers.CharField(),
            }
        )
        ,
        'default': responseError,

    }
)

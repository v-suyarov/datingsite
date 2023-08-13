from PIL import Image
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from clients.models import Participant

from clients.utils import apply_watermark


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)

    class Meta:
        model = Participant
        exclude = ["id", "user", 'likes']

    def create(self, validated_data):
        user_serializer = UserSerializer(data={"username": validated_data.pop("username"),
                                               "password": validated_data.pop("password")})
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        # добавление водяного знака на аватар пользователя
        avatar = Image.open(validated_data["avatar"])
        avatar = apply_watermark(avatar, path_to_watermark='static/img/watermark.png')
        validated_data["avatar"] = avatar
        participant = Participant.objects.create(user=user, **validated_data)

        return participant


class ParticipantMathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = []

    def update(self, instance, validated_data):
        evaluated = Participant.objects.get(pk=self.context.get('pk'))
        instance.likes.add(evaluated)
        instance.save()
        return instance

    def validate(self, data):
        evaluated_pk = self.context.get('pk', None)

        if not Participant.objects.filter(pk=evaluated_pk).exists():
            raise serializers.ValidationError({"pk": "Идентификатор оцениваемого участника недействителен"})

        if evaluated_pk == self.instance.pk:
            raise serializers.ValidationError({"pk": "Невозможно оценить самого себя"})
        return data

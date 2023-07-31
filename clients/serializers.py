from PIL import Image
from django.contrib.auth.models import User
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
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Participant
        exclude = ["id", "user"]

    def create(self, validated_data):
        user_serializer = UserSerializer(data={"username": validated_data.pop("username"),
                                               "password": validated_data.pop("password")})
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        # добавление водяного знака на аватар пользователя
        avatar = Image.open(validated_data["avatar"])
        avatar = apply_watermark(avatar)
        validated_data["avatar"] = avatar
        participant = Participant.objects.create(user=user, **validated_data)

        return participant

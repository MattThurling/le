from rest_framework import serializers
from website.models import TimeLog, Attainment, Level
from django.contrib.auth import get_user_model

class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = '__all__'
        read_only_fields = ('user',)

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('id', 'code', 'study', 'hierarchy')

class AttainmentSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)

    class Meta:
        model = Attainment
        fields = ('id', 'level', 'created_at')

class UserSerializer(serializers.ModelSerializer):
    attainments = serializers.SerializerMethodField()
    current_level = serializers.SerializerMethodField()
    next_level = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'attainments', 'current_level', 'next_level')

    def get_attainments(self, obj):
        attainments = obj.get_attainments()
        return AttainmentSerializer(attainments, many=True).data

    def get_current_level(self, obj):
        current_level, _ = obj.get_current_and_next_level()
        return LevelSerializer(current_level).data if current_level else None

    def get_next_level(self, obj):
        _, next_level = obj.get_current_and_next_level()
        return LevelSerializer(next_level).data if next_level else None


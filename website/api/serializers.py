from rest_framework import serializers
from website.models import TimeLog

class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = '__all__'
        read_only_fields = ('user',)

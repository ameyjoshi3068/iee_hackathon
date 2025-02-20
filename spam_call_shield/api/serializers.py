from rest_framework import serializers
from .models import CallRecording

class CallRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecording
        fields = '__all__'

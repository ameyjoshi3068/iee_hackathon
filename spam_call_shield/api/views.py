from django.shortcuts import render
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from api.app.huggingface_model import analyze_call
from .models import CallRecording
from .serializers import CallRecordingSerializer
from api.app.speech_processing import transcribe_audio
from api.app.ai_analysis import analyze_text

def setup_file_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs even debug messages
    fh = logging.FileHandler('spam_shield.log')
    fh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(fh)
    return logger

logger = setup_file_logger()

class UploadCallRecording(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = CallRecordingSerializer(data=request.data)
        if file_serializer.is_valid():
            call_recording = file_serializer.save()
            file_path = call_recording.audio_file.path
            logger.info(f"File Saved {file_path}")
            transcript = transcribe_audio(file_path)
            logger.info(f"Transcript created for {file_path}")
            call_recording.transcript = transcript

            is_suspicious, reason = analyze_call(transcript)
            logger.info(f"Text analyzed for {file_path} : is_suspicious - {is_suspicious}, reason - {reason}")
            call_recording.is_suspicious = is_suspicious
            call_recording.reason = reason
            call_recording.save()
            
            return Response(CallRecordingSerializer(call_recording).data, status=201)
        return Response(file_serializer.errors, status=400)

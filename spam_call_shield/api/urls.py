from django.urls import path
from .views import UploadCallRecording

urlpatterns = [
    path('upload/', UploadCallRecording.as_view(), name='upload-call'),
]

from django.db import models

class CallRecording(models.Model):
    audio_file = models.FileField(upload_to='recordings/')
    transcript = models.TextField(blank=True, null=True)
    is_suspicious = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

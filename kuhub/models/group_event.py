from django.db import models
import random
import string
import uuid

class GroupEvent(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    requests_id = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    def generate_request_id(self):
        if not self.requests_id:
            self.requests_id = uuid.uuid4()
            self.save()
        return str(self.requests_id)

    def __str__(self):
        return self.summary

from django.db import models
import random
import string

class GroupEvent(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255,null=True)
    requests_id = models.CharField(max_length=255, blank=True, null=True, default='')
    link = models.CharField(max_length=255, blank=True, default='')

    def generate_request_id(self):
        characters = string.ascii_letters + string.digits
        self.requests_id = ''.join(random.choice(characters) for _ in range(10))
        while GroupEvent.objects.filter(requests_id=self.requests_id).exists():
            self.requests_id = ''.join(random.choice(characters) for _ in range(10))
        print(self.requests_id)

    def __str__(self):
        return self.summary

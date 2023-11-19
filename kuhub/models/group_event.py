from django.db import models

class GroupEvent(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.summary

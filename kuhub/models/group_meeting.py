from django.db import models

class Group_meeting(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def get_attendies(self):
        return [member.email for member in self.group.group_member.all()]


    def __str__(self):
        return self.summary

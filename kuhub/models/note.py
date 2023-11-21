from django.db import models

class Note(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    note_text = models.CharField(max_length=255)



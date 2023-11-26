from django.db import models

class Task(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    event = models.ForeignKey('GroupEvent', on_delete=models.CASCADE, blank=True, null=True)
    task_text = models.CharField(max_length=255)
    assign_user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('todo', 'todo'),
        ('in progress', 'in progress'),
        ('done', 'done'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


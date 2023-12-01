from django.db import models

class Task(models.Model):
    """
        Model representing a task within a group or event.

        Attributes:
            group (Group): ForeignKey to the Group model, specifying the group associated with the task.
            event (GroupEvent, optional): ForeignKey to the GroupEvent model, specifying the event associated with the task (can be null).
            task_text (str): The text content or description of the task.
            assign_user (auth.User): ForeignKey to the User model, specifying the user assigned to the task.
            status (str): The status of the task, chosen from predefined choices (todo, in progress, done).

        """
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


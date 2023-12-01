from django.db import models
import random
import string
import uuid

class GroupEvent(models.Model):
    """
    Model representing a event crated by user. Show in the calendar.

    Attributes:
        group (Group): ForeignKey to the Group model, specifying the group associated with the event.
        start_time (str): The start time of the event as a string (e.g., "2023-12-01T08:00:00").
        end_time (str): The end time of the event as a string (e.g., "2023-12-01T10:00:00").
        show_time (str, optional): The time to display for the event, if different from start_time.
        summary (str): A concise summary or title for the event.
        location (str): The location where the event will take place.
        description (str): A brief description of the event.
        link (str, optional): A link related to the event, if applicable.
    """
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    show_time = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.summary

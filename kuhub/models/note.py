from django.db import models


class Note(models.Model):
    """
        A class representing a group's note.

        Attributes:
            group (ForeignKey): The group that the note belongs to.
            note_text (CharField): The content of the note.
    """
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    note_text = models.CharField(max_length=255)

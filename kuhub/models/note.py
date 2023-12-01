from django.db import models

class Note(models.Model):
    """
        Model representing a note associated with a group in Group Hub.

        Attributes:
            group (Group): ForeignKey to the Group model, specifying the group associated with the note.
            note_text (str): The text content of the note.

    """
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    note_text = models.CharField(max_length=255)



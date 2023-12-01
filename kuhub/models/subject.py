from django.db import models


class Subject(models.Model):
    """
        Model representing a subject or course.

        Attributes:
            course_code (str): The code identifying the course.
            type (str): The type or category of the subject.
            name_eng (str): The English name or title of the subject.
            name_th (str): The Thai name or title of the subject.
            unit (str): The unit or credit hours associated with the subject.
            hour (str): The number of hours the subject spans.
            faculty (str): The faculty or department offering the subject.

        """

    course_code = models.CharField(max_length=10)
    type = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=255)
    name_th = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    hour = models.CharField(max_length=10)
    faculty = models.CharField(max_length=255)

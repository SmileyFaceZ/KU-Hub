from django.db import models


class Subject(models.Model):
    course_code = models.CharField(max_length=10)
    type = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=255)
    name_th = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    hour = models.CharField(max_length=10)
    faculty = models.CharField(max_length=255)

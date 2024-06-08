
from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    class Meta:
        db_table = "grade"

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    class Meta:
        db_table = "student"
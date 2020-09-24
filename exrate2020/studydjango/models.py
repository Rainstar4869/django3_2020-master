from django.db import models


# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True)
    school = models.ForeignKey(to=School, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name

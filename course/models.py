from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from lab6.models import User

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=41, null=False, unique=True)
    description = models.CharField(max_length=150)
    duration = models.CharField(max_length=20)
    mini_image = models.ImageField(upload_to= 'images/', null=True)
    image = models.ImageField(upload_to= 'images/', null=True)
    discipline = models.CharField(max_length=41, null=False)
    prof = models.CharField(max_length=41, null=False)
    color = models.CharField(max_length=41, null=False)


class User_Course(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=2, null=False)


class Lession(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    num = models.IntegerField()
    title = models.CharField(max_length=41, null=False)
    file = models.FileField(upload_to= 'files/', null=True)


class User_Lession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lession = models.ForeignKey(Lession, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to= 'files/', null=True)
    complete = models.IntegerField()

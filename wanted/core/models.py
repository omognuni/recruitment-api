from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recruit(models.Model):
    title = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    reward = models.IntegerField()
    description = models.TextField(blank=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, blank=True, null=True)
    stack = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class User(AbstractUser):
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

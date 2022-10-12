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
        'Company',to_field='name', on_delete=models.SET_NULL, blank=True, null=True)
    stack = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Apply(models.Model):
    recruit = models.ForeignKey('Recruit', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recruit', 'user'],
                name='unique_apply',
            ),
        ]
    
    
class User(AbstractUser):

    def __str__(self):
        return self.username

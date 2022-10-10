from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255,unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recruit(models.Model):
    title = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    reward = models.IntegerField()
    description = models.TextField(blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    stack = models.CharField(max_length=255)

    def __str__(self):
        return self.title
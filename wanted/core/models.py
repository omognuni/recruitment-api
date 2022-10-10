from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255,unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name
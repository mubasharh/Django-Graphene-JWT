from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

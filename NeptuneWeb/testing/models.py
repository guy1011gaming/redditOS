from django.db import models

# Create your models here.
class User(models.Model):
    username = models.TextField(null=False)
    email = models.TextField(null=False)
    password_hash = models.TextField(null=False)
    name = models.TextField(null=False)
    surname = models.TextField(null=False)
    verified = models.BooleanField(null=False)
from django.db import models
from solid_backend.content.models import BaseProfile
# Create your models here.


class MyProfile(BaseProfile):
    name = models.CharField(max_length=200, default="")


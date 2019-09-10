from django.contrib.auth.models import User
from datetime import datetime
from links.models import Link, FileObject
from djongo import models

# Create your models here.

# account model
# 1. username - foreignkey to user
# 2. is_paid - boolean
# 3. linkset - set of id all links it creates 

class Account(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    linkset = models.ArrayModelField(model_container=Link)
    fileset = models.ArrayModelField(model_container=FileObject)

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

# link model
# 1. suffix - string - zuru.io/suffix
# 2. to - string - the url 
# 3. is_active - bool
# 4. redirects - 1 or infinity or custom
# 5. expiriy - date
# 6. owner - either akshay or some user

class Link(models.Model):
    suffix = models.CharField(max_length=32)
    to = models.CharField(max_length=9000)
    is_active = models.BooleanField(default=False)
    is_fileobject = models.BooleanField(default=False)
    redirects = models.IntegerField(default=9999)
    expiry = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.suffix

    def get_expiry_date(self):
        return self.expiry.strftime('%b %e %Y')
    
    def delete(self):
        print("Delete Called")
        Link.objects.filter(suffix=self.suffix).delete()

class FileObject(models.Model):
    link = models.CharField(max_length=9999)
    suffix = models.CharField(max_length=32, default='')
    name = models.CharField(max_length=9999, default='NameLess')
    fileObject = models.FileField(upload_to='f/')
    expiry = models.DateTimeField()
    redirects = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self):
        print("Object Delete Called")
        Link.objects.filter(suffix=self.suffix).delete()

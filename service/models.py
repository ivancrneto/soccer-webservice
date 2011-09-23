from django.db import models

# Create your models here.

class JsonEvent(models.Model):
    data = models.TextField()
    

class XmlEvent(models.Model):
    data = models.TextField()

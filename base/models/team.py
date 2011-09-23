from django.db import models

import os

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    
    class Meta:
        app_label = 'base'
        db_table = 'base_team'
        
    def __unicode__(self):
        return self.name
    
        

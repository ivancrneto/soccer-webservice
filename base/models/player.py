from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        app_label = 'base'
        db_table = 'base_player'
        
    def __unicode__(self):
        return self.name

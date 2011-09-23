from django.db import models

# Create your models here.

class Game(models.Model):
    team_home = models.ForeignKey('Team', related_name='team_home')
    team_visitor = models.ForeignKey('Team', related_name='team_visitor')
    goals_home = models.PositiveIntegerField(default=0)
    goals_visitor = models.PositiveIntegerField(default=0)

    
    class Meta:
        app_label = 'base'
        db_table = 'base_game'
        
    def __unicode__(self):
        return self.team_home.name + ' x ' + self.team_visitor.name

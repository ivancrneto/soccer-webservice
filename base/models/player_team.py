from django.db import models

# Create your models here.

class PlayerTeam(models.Model):
    player = models.ForeignKey('Player')
    team = models.ForeignKey('Team')
    
    class Meta:
        app_label = 'base'
        db_table = 'base_player_team'
    
    def __unicode__(self):
        return self.player.name + ' - ' + self.team.name

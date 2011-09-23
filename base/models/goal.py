import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from futebol.service.models import JsonEvent, XmlEvent
from xml.dom import minidom

from futebol.base.models.team import Team


# Create your models here.

class Goal(models.Model):
    player_team = models.ForeignKey('PlayerTeam')
    game = models.ForeignKey('Game')
    time = models.PositiveIntegerField()
    half = models.PositiveSmallIntegerField()
    
    class Meta:
        app_label = 'base'
        db_table = 'base_goal'

                
@receiver(post_save, sender=Goal, dispatch_uid="goal_post_save")
def create_goal_event(sender, **kwargs):
    if kwargs['created']:
        #saving in json format
        data = {}
        data['type'] = 'goal'
        goal = kwargs['instance']
        data['data'] = {'player': {
                            'id': goal.player_team.player.id,
                            'name': goal.player_team.player.name,
                        },
                        'game_id': goal.game.id,
                        'team': {
                            'id': goal.player_team.team.id,
                            'name': goal.player_team.team.name,
                        },
                        'minutes': str(goal.time)[:2],
                        'seconds': str(goal.time)[2:],
                        'half': goal.half,
                       }
        JsonEvent.objects.create(data=json.dumps(data))
        
        #saving in xml format
        doc = minidom.Document()
        event = doc.createElement('event')
        evtype = doc.createElement('type')
        evtype.appendChild(doc.createTextNode('goal'))
        event.appendChild(evtype)
        data = doc.createElement('data')
        game_id = doc.createElement('game_id')
        game_id.appendChild(doc.createTextNode('%s' % goal.game.id))
        data.appendChild(game_id)
        
        player = doc.createElement('player')
        player_id = doc.createElement('id')
        player_id.appendChild(doc.createTextNode('%s' % goal.player_team.player.id))
        player.appendChild(player_id)
        player_name = doc.createElement('name')
        player_name.appendChild(doc.createTextNode(goal.player_team.player.name))
        player.appendChild(player_name)
        data.appendChild(player)
        
        team = doc.createElement('team')
        team_id = doc.createElement('id')
        team_id.appendChild(doc.createTextNode('%s' % goal.player_team.team.id))
        team.appendChild(team_id)
        team_name = doc.createElement('name')
        team_name.appendChild(doc.createTextNode(goal.player_team.team.name))
        team.appendChild(team_name)
        data.appendChild(team)
        
        minutes = doc.createElement('minutes')
        minutes.appendChild(doc.createTextNode(str(goal.time)[:2]))
        data.appendChild(minutes)
        seconds = doc.createElement('seconds')
        seconds.appendChild(doc.createTextNode(str(goal.time)[2:]))
        data.appendChild(seconds)
        half = doc.createElement('half')
        half.appendChild(doc.createTextNode('%s' % goal.half))
        data.appendChild(half)
        event.appendChild(data)
        doc.appendChild(event)
        
        XmlEvent.objects.create(data=doc.toxml('UTF-8'))
 
    
post_save.connect(create_goal_event, sender=Goal, dispatch_uid="goal_post_save")

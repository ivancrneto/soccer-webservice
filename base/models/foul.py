import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from futebol.service.models import JsonEvent, XmlEvent
from xml.dom import minidom

# Create your models here.

class Foul(models.Model):
    player_team_made_foul = models.ForeignKey('PlayerTeam', related_name='player_team_made_foul')
    player_team_fouled = models.ForeignKey('PlayerTeam', related_name='player_team_fouled')
    game = models.ForeignKey('Game')
    time = models.PositiveIntegerField()
    half = models.PositiveSmallIntegerField()
    
    
    class Meta:
        app_label = 'base'
        db_table = 'base_foul'
        

@receiver(post_save, sender=Foul, dispatch_uid="foul_post_save")
def create_foul_event(sender, **kwargs):
    if kwargs['created']:
        #saving in json format
        event = {}
        event['type'] = 'foul'
        foul = kwargs['instance']
        event['data'] = {'player_made_foul': {
                            'id': foul.player_team_made_foul.player.id,
                            'name': foul.player_team_made_foul.player.name
                        },
                        'player_fouled': {
                            'id': foul.player_team_fouled.player.id,
                            'name': foul.player_team_fouled.player.name
                        },
                        'game_id': foul.game.id,
                        'minutes': str(foul.time)[:2],
                        'seconds': str(foul.time)[2:],
                        'half': foul.half,
                       }
        JsonEvent.objects.create(data=json.dumps(event))
        
        #saving in xml format
        doc = minidom.Document()
        event = doc.createElement('event')
        evtype = doc.createElement('type')
        evtype.appendChild(doc.createTextNode('foul'))
        event.appendChild(evtype)
        data = doc.createElement('data')
        game_id = doc.createElement('game_id')
        game_id.appendChild(doc.createTextNode('%s' % foul.game.id))
        data.appendChild(game_id)
        
        player_made_foul = doc.createElement('player_made_foul')
        player_made_foul_id = doc.createElement('id')
        player_made_foul_id.appendChild(doc.createTextNode(
            '%s' % foul.player_team_made_foul.player.id))
        player_made_foul.appendChild(player_made_foul_id)
        player_made_foul_name = doc.createElement('name')
        player_made_foul_name.appendChild(doc.createTextNode(
            foul.player_team_made_foul.player.name))
        player_made_foul.appendChild(player_made_foul_name)
        data.appendChild(player_made_foul)
        
        player_fouled = doc.createElement('player_fouled')
        player_fouled_id = doc.createElement('id')
        player_fouled_id.appendChild(doc.createTextNode(
            '%s' % foul.player_team_fouled.player.id))
        player_fouled.appendChild(player_fouled_id)
        player_fouled_name = doc.createElement('name')
        player_fouled_name.appendChild(doc.createTextNode(
            foul.player_team_fouled.player.name))
        player_fouled.appendChild(player_fouled_name)
        data.appendChild(player_fouled)
        
        minutes = doc.createElement('minutes')
        minutes.appendChild(doc.createTextNode(str(foul.time)[:2]))
        data.appendChild(minutes)
        seconds = doc.createElement('seconds')
        seconds.appendChild(doc.createTextNode(str(foul.time)[2:]))
        data.appendChild(seconds)
        half = doc.createElement('half')
        half.appendChild(doc.createTextNode('%s' % foul.half))
        data.appendChild(half)
        event.appendChild(data)
        doc.appendChild(event)
        
        XmlEvent.objects.create(data=doc.toxml('UTF-8'))
 
    
post_save.connect(create_foul_event, sender=Foul, dispatch_uid="foul_post_save")

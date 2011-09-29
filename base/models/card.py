import json
import time
import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from futebol.service.models import JsonEvent, XmlEvent
from xml.dom import minidom

# Create your models here.

class Card(models.Model):
    player_team = models.ForeignKey('PlayerTeam')
    game = models.ForeignKey('Game')
    cardtype = models.CharField(max_length=1, choices=(('Y', 'Yellow'), ('R', 'Red'),))
    time = models.PositiveIntegerField()
    half = models.PositiveSmallIntegerField()
    
    
    class Meta:
        app_label = 'base'
        db_table = 'base_card'
        
@receiver(post_save, sender=Card, dispatch_uid="card_post_save")
def create_card_event(sender, **kwargs):
    if kwargs['created']:
        #saving in json format
        event = {}
        event['type'] = 'card'
        card = kwargs['instance']
        event['data'] = {'player': {
                            'id': card.player_team.player.id,
                            'name': card.player_team.player.name
                        },
                        'cardtype': card.cardtype,
                        'game_id': card.game.id,
                        'minutes': str(card.time)[:2],
                        'seconds': str(card.time)[2:],
                        'half': card.half,
                       }
        JsonEvent.objects.create(data=json.dumps(event))
        
        #saving in xml format
        doc = minidom.Document()
        event = doc.createElement('event')
        evtype = doc.createElement('type')
        evtype.appendChild(doc.createTextNode('card'))
        event.appendChild(evtype)
        evttimestamps = doc.createElement('timestamps')
        evttimestamps.appendChild(doc.createTextNode('%s' % int(time.mktime(datetime.datetime.now().timetuple()))))
        event.appendChild(evttimestamps)
        data = doc.createElement('data')
        game_id = doc.createElement('game_id')
        game_id.appendChild(doc.createTextNode('%s' % card.game.id))
        data.appendChild(game_id)
        
        player = doc.createElement('player')
        player_id = doc.createElement('id')
        player_id.appendChild(doc.createTextNode('%s' % card.player_team.player.id))
        player.appendChild(player_id)
        player_name = doc.createElement('name')
        player_name.appendChild(doc.createTextNode(card.player_team.player.name))
        player.appendChild(player_name)
        data.appendChild(player)
        
        cardtype = doc.createElement('cardtype')
        cardtype.appendChild(doc.createTextNode(card.cardtype))
        data.appendChild(cardtype)
        
        minutes = doc.createElement('minutes')
        minutes.appendChild(doc.createTextNode(str(card.time)[:2]))
        data.appendChild(minutes)
        seconds = doc.createElement('seconds')
        seconds.appendChild(doc.createTextNode(str(card.time)[2:]))
        data.appendChild(seconds)
        half = doc.createElement('half')
        half.appendChild(doc.createTextNode('%s' % card.half))
        data.appendChild(half)
        event.appendChild(data)
        doc.appendChild(event)
        
        XmlEvent.objects.create(data=doc.toxml('UTF-8'))
 
    
post_save.connect(create_card_event, sender=Card, dispatch_uid="card_post_save")

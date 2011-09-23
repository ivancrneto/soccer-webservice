import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from futebol.service.models import JsonEvent, XmlEvent
from xml.dom import minidom

from django.conf import settings


# Create your models here.

class Replay(models.Model):
    game = models.ForeignKey('Game')
    video = models.FileField(upload_to='replays')
    description = models.CharField(max_length=180)
    time = models.PositiveIntegerField()
    half = models.PositiveSmallIntegerField()
    
    
    class Meta:
        app_label = 'base'
        db_table = 'base_replay'
        


@receiver(post_save, sender=Replay, dispatch_uid="replay_post_save")
def create_replay_event(sender, **kwargs):
    if kwargs['created']:
        event = {}
        event['type'] = 'replay'
        replay = kwargs['instance']
         
        #saving in json format
        event['data'] = {
                        'game_id': replay.game.id,
                        'description': replay.description,
                        'video': settings.BASE_URL + replay.video.url,
                        'minutes': str(replay.time)[:2],
                        'seconds': str(replay.time)[2:],
                        'half': replay.half,
                       }
        JsonEvent.objects.create(data=json.dumps(event)) 
        
        #saving in xml format
        doc = minidom.Document()
        event = doc.createElement('event')
        evtype = doc.createElement('type')
        evtype.appendChild(doc.createTextNode('replay'))
        event.appendChild(evtype)
        data = doc.createElement('data')
        game_id = doc.createElement('game_id')
        game_id.appendChild(doc.createTextNode('%s' % replay.game.id))
        data.appendChild(game_id)
        description = doc.createElement('description')
        description.appendChild(doc.createTextNode(replay.description))
        data.appendChild(description)
        video = doc.createElement('video')
        video.appendChild(doc.createTextNode(settings.BASE_URL + replay.video.url))
        data.appendChild(video)
        minutes = doc.createElement('minutes')
        minutes.appendChild(doc.createTextNode(str(replay.time)[:2]))
        data.appendChild(minutes)
        seconds = doc.createElement('seconds')
        seconds.appendChild(doc.createTextNode(str(replay.time)[2:]))
        data.appendChild(seconds)
        half = doc.createElement('half')
        half.appendChild(doc.createTextNode('%s' % replay.half))
        data.appendChild(half)
        event.appendChild(data)
        doc.appendChild(event)
        
        XmlEvent.objects.create(data=doc.toxml('UTF-8'))
        
    
post_save.connect(create_replay_event, sender=Replay, dispatch_uid="replay_post_save")



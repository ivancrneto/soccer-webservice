from futebol.base.models import Team
from futebol.base.models import Player
from futebol.base.models import PlayerTeam
from futebol.base.models import Game
from futebol.base.models import Goal
from futebol.base.models import Card
from futebol.base.models import Foul
from futebol.base.models import Replay
from django.contrib import admin


admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerTeam)
admin.site.register(Game)
admin.site.register(Goal)
admin.site.register(Card)
admin.site.register(Foul)
admin.site.register(Replay)

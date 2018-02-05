from mongoengine import *
import time

connect(host="localhost:27017")

# connect(username="andrew", password="sfhacks18", host="mongodb://main-shard-00-00-w6sow.mongodb.net:27017,main-shard-00-01-w6sow.mongodb.net:27017,main-shard-00-02-w6sow.mongodb.net:27017/test?ssl=true&replicaSet=main-shard-0&authSource=admin")

class Player(Document):
    name = StringField(max_length=50)

class Time(Document):
    stroke = StringField()
    distance = IntField()
    time = FloatField()
    player = ReferenceField(Player)

def getRoster():
    return Player.objects.order_by("name")

def addPlayer(name):
    Player(name=name).save()

def getPlayer(name):
    return Player.objects(name = name)[0]

def getPlayerById(id):
    return Player.objects(id = id)[0]

def addTime(stroke, distance, time, player_id):
    Time(stroke=stroke, distance=distance, time=time, player=player_id).save()

def getTopPlayers(stroke, distance):
    players = []
    times = []

    for i in range(5):
        query = Time.objects(stroke=stroke, distance=distance, player__nin=players).limit(1).order_by("time")
        if len(query) > 0:
            time = query[0]
            times.append(time)
            players.append(time.player)
    return times


def getAllTimesForPlayer(stroke, distance, player_id):
        return Time.objects(stroke=stroke, distance=distance, player=player_id).order_by("-id")

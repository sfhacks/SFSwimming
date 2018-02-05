from mongoengine import *

connect(username="andrew", password="sfhacks18", host="mongodb://main-shard-00-00-w6sow.mongodb.net:27017,main-shard-00-01-w6sow.mongodb.net:27017,main-shard-00-02-w6sow.mongodb.net:27017/test?ssl=true&replicaSet=main-shard-0&authSource=admin")

class Player(Document):
    name = StringField(max_length=50)

class Time(Document):
    stroke = StringField()
    distance = IntField()
    time = FloatField()
    player = ReferenceField(Player)

def getRoster():
    return Player.objects

def addPlayer(name):
    Player(name=name).save()

def getPlayer(name):
    return Player.objects(name = name)[0]

def getPlayerById(id):
    return Player.objects(id = id)[0]

def addStroke(stroke, distance, time, player_id):
    Time(stroke=stroke, distance=distance, time=time, player=player_id).save()

def getSortedStrokes(stroke, distance, player_id = None):
    if player_id:
        return Time.objects(stroke=stroke, distance=distance, player=player_id).order_by("time").limit(5)
    else:
        return Time.objects(stroke=stroke, distance=distance).order_by("time").limit(5)

def getAllTimesForPlayer(stroke, distance, player_id):
        return Time.objects(stroke=stroke, distance=distance, player=player_id)

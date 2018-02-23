from mongoengine import *
import time

import os

if not os.environ.get('DOCKER'):
    connect(host="localhost:27017")
else:
    connect(host="db:27017")

#Schemas

class Meet(Document):
    name = StringField()

    @staticmethod
    def all():
        return Meet.objects.order_by("name")

    @staticmethod
    def add(name):
        Meet(name = name).save()


class Player(Document):
    name = StringField(max_length=50)

    @staticmethod
    def all():
        return Player.objects.order_by("name")

    @staticmethod
    def remove(name):
        p = Player.objects.get(name=name)
        times = Time.objects(player=p)
        for time in times:
            time.delete()
        p.delete()

    @staticmethod
    def top_players(stroke, distance):
        players = []
        times = []

        for _ in range(5):
            query = Time.objects(stroke=stroke, distance=distance, player__nin=players).limit(1).order_by("time")
            if len(query) > 0:
                time = query[0]
                times.append(time)
                players.append(time.player)
        return times

    def times(self, stroke = None, distance = None):
        if stroke:
            return Time.objects(stroke=stroke, distance=distance, player=self).order_by("-id")
        else:
            return Time.objects(player=self).order_by("-id")


class Time(Document):
    stroke = StringField()
    distance = IntField()
    time = FloatField()
    player = ReferenceField(Player)
    meet = ReferenceField(Meet)

    @staticmethod
    def top_times(stroke, distance):
        return Time.objects(stroke=stroke, distance=distance).order_by("time")[:5]

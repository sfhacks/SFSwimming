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
    gender = StringField(max_length=50)
    team = StringField(max_length=50)

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
    def top_players(stroke, distance, gender, team):
        players = []
        times = []
        query = Time.objects(stroke=stroke, distance=distance, player__nin=players).order_by("time")

        for time in query:
            if str(time.player.name) not in players and str(time.player.gender) == gender and str(time.player.team) == team:
                times.append(time)
                players.append(time.player.name)

        return times[:5]

    @staticmethod
    def filter_by_team(gender, team):
        players = []
        query = Player.objects.order_by("name")

        for player in query:
            if str(player.gender) == gender and str(player.team) == team:
                players.append(player)

        return players

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
    str_time = StringField()

    @staticmethod
    def top_times(stroke, distance, gender, team):
        times = []
        query = Time.objects(stroke=stroke, distance=distance).order_by("time")

        for time in query:
            if str(time.player.gender) == gender and str(time.player.team) == team:
                times.append(time)

        return times[:5]

    @staticmethod
    def all_times():
        return Time.objects.order_by("name")

    @staticmethod
    def parse_time(str_time):
        # 04:10.21 -> 4 minutes, 10 seconds, 21 ms
        minute = int(str_time.split(":")[0])
        second = float(str_time.split(":")[1])
        total_time_seconds = minute * 60 + second

        return total_time_seconds

    @staticmethod
    def reverse_time(flt_time):
        minute = int(flt_time // 60)
        second = round(flt_time - (60 * minute), 2)
        return (str(minute) + ":" + str(second))

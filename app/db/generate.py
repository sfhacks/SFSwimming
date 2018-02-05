from mongoengine import *
import time
import random

connect( host="mongodb://127.0.0.1:27017/test")

from faker import Faker
fake = Faker()

fake.name()



class Player(Document):
    name = StringField(max_length=50)

class Time(Document):
    stroke = StringField()
    distance = IntField()
    time = FloatField()
    player = ReferenceField(Player)

for p in Player.objects:
    print(p.delete())

for t in Time.objects:
    print(t.delete())

for i in range(1000):
    p = Player(name = fake.name()).save()
    for i in range(250):
        Time(stroke="fly", distance=50, time=random.uniform(20,30), player=p).save()
        Time(stroke="free", distance=100, time=random.uniform(20,30), player=p).save()
        Time(stroke="fly", distance=100, time=random.uniform(20,30), player=p).save()
        Time(stroke="free", distance=50, time=random.uniform(20,30), player=p).save()

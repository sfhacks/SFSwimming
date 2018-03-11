from mongoengine import *
import time
import random

from db import Player, Time, Meet



connect(host="mongodb://127.0.0.1:27017/test")

from faker import Faker
fake = Faker()

fake.name()


for p in Player.objects:
    print(p.delete())

for t in Time.objects:
    print(t.delete())

for i in range(10):
    p = Player(name = fake.name(), team="Varsity", gender="M").save()
    for i in range(10):
        Time(stroke="fly", distance=50, time=random.uniform(20,30), player=p).save()
        Time(stroke="free", distance=100, time=random.uniform(20,30), player=p).save()
        Time(stroke="fly", distance=100, time=random.uniform(20,30), player=p).save()
        Time(stroke="free", distance=50, time=random.uniform(20,30), player=p).save()

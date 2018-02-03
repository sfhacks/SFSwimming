# for p in Player.objects:
#     print(p.delete())
#
# for t in Time.objects:
#     print(t.delete())
#
#
# ross = Player(name = "Dan Quinn").save()
#
# print(ross.id)
#
# time = Time(stroke = "free", distance = 50, time = 20.6, player = ross.id)
# time.save()
#
# print(time.player.name)
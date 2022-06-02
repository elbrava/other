import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Records(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    score = models.FloatField()


class Rooms(models.Model):
    condition = models.CharField(max_length=455,default="")
    room_id = models.UUIDField(unique=True, default=uuid.uuid4)
    max_users = models.IntegerField(default=5)
    count_s = models.IntegerField(default=0)
    in_session = models.BooleanField(default=False)
    empty = models.BooleanField(default=True)
    full = models.BooleanField(default=False)

    def upd(self):

        if self.count_s == self.max_users:
            self.full = True
        else:
            self.full = False
        if self.count_s == 0:
            self.empty = True
        else:
            self.empty = False
        self.save()
    def __str__(self):
        return self.condition

from django.db import models
from django.utils import timezone
# Create your models here.

class CalendarModel(models.Model):
    title = models.CharField(max_length=20)
    cal_data = models.JSONField("JSONデータ",blank=True,null=True)
    def __str__(self):
        return self.title

class TestModel(models.Model):
    title = models.CharField(max_length=20)
    startDay = models.DateTimeField("開始",default=timezone.now())
    endDay = models.DateTimeField("終了",default=timezone.now())
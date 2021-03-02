from django.db import models

# Create your models here.

class CalendarModel(models.Model):
    title = models.CharField(max_length=20)
    cal_data = models.JSONField(blank=True,null=True)
    def __str__(self):
        return self.title
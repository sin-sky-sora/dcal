from django.contrib import admin
from .models import CalendarModel,TestModel
# Register your models here.

admin.site.register(CalendarModel)
admin.site.register(TestModel)
from django.contrib import admin
from .models import *
# Register your models here.

# class TopicAdmin(admin.ModelAdmin):
#     list_display = ()

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
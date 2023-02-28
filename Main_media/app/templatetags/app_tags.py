from django import template
from django.db.models import *
from app.models import *

register = template.Library()

@register.simple_tag(name='topics')
def get_topic():
    return Topic.objects.all()

@register.inclusion_tag('app/sidebar.html')
def MainShowTopics():
    topics = Topic.objects.annotate(cnt=Count('room')).filter(cnt__gt=0)
    cnt_topics = Topic.objects.aggregate(cnt=Count('room'))
    return {'topics': topics, 'cnt_topics': cnt_topics}
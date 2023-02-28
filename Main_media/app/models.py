from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Topic(models.Model):
    name = models.CharField(max_length=200, verbose_name='Topic name')
    # slug = models.SlugField(max_length=200, verbose_name='Topic URL')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, verbose_name='Room name')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    # slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)
    content = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name= 'participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    password = models.CharField(max_length=25, blank=True, null=True)
    # private = models.BooleanField(default=True, verbose_name='Type of Room!')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField(max_length=200, )

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['created']
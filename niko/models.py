from autoslug  import AutoSlugField
from django.db import models

class Poll(models.Model):
    name =  models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.SlugField(max_length=300)
    slug = AutoSlugField(('slug'), max_length=300, unique=True,
        populate_from=('name'))
    def __str__(self):
        return self.name

class Vote(models.Model):

    BAD   = 0
    GREAT = 1
    OK    = 2
    MOOD  = (
        (BAD,   'Sad'),
        (GREAT, 'Great'),
        (OK,    'OK'),
    )
    ip = models.CharField(max_length=15)
    mood = models.PositiveSmallIntegerField(choices=MOOD, default=OK)
    poll = models.ForeignKey( Poll )
    pub_date = models.DateTimeField('date published', auto_now_add=True)

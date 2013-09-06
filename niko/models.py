from django.db import models

class Vote(models.Model):
    HAPPY = 'h'
    OK    = 'o'
    SAD   = 's'
    MOOD  = (
        (HAPPY, 'Happy'),
        (OK,    'OK'),
        (SAD,   'Sad'),
    )
    ip = models.CharField(max_length=15)
    mood = models.CharField(max_length=1,
        choices=MOOD, default= OK)
    pub_date = models.DateTimeField('date published')

from django.db import models

class Vote(models.Model):
    BAD   = 'b'
    GREAT = 'g'
    OK    = 'o'
    MOOD  = (
        (BAD,   'Sad'),
        (GREAT, 'Great'),
        (OK,    'OK'),
    )
    ip = models.CharField(max_length=15)
    mood = models.CharField(max_length=1,
        choices=MOOD, default= OK)
    pub_date = models.DateTimeField('date published')

from django.db import models

# Create your models here.

class Clubevents(models.Model):
    eventname=models.CharField(max_length = 200)
    eventurl=models.URLField(max_length=250)

    def __str__(self):
        return self.eventname

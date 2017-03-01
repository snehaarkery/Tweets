from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()

    #Python 2
    def __unicode__(self):
        return self.title

    #Python 3
    def __str__(self):
        return self.title




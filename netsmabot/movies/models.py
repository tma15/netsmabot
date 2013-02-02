from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    date = models.DateTimeField()
    class Meta:
        app_label = 'movies'

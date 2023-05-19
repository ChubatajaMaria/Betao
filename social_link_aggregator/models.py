from django.db import models

# Create your models here.
class Link(models.Model):
    url = models.URLField(unique=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

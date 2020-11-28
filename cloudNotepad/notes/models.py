from django.db import models
from django.utils import timezone

# Create your models here.

# class Notebook(models.Model):
#     title = models.CharField(max_length=50, unique=True)
#     id = models.CharField(max_length=25, default=1, primary_key=True)
#     color = models.CharField(max_length=25)

#      # Note: need to set the timezone to the user's default timezone
#     date_created = models.DateTimeField(default=timezone.now)
#     last_updated = models.DateTimeField(auto_now_add=True)   


class Note(models.Model):
    title = models.CharField(max_length=50, unique=True)
    id = models.CharField(max_length=25, default=1, primary_key=True)
    tags = models.CharField(max_length=25)
    text = models.TextField()
    # container = models.ForeignKey(
    #     'Notebook',
    #     on_delete=models.PROTECT,
    #     to_field='title',
    #     default='My Notebook'
    # )

    # Note: need to set the timezone to the user's default timezone
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True)

    @property
    def all_text(self):
        return '%s %s %s' % (self.title, self.tags, self.text)
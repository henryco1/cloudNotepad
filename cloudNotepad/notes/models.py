from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField

"""
Model class declarations
"""
class Notebook(models.Model):
    title = models.CharField(
        max_length=50, 
        unique=True, 
        primary_key=True, 
        default='My Notebook'
    )
    color = models.CharField(max_length=25, default='Red')

     # Note: need to set the timezone to the user's default timezone
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True)   
    slug = AutoSlugField(populate_from=['date_created'], unique=True, null=False)

class Note(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tags = models.CharField(max_length=25)
    text = models.TextField()
    container = models.ForeignKey(
        Notebook,
        on_delete=models.PROTECT,
    )

    # Note: need to set the timezone to the user's default timezone
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=['title', 'date_created'], unique=True, null=False)

    @property
    def all_text(self):
        return '%s %s %s' % (self.title, self.tags, self.text)

"""
Model form class declarations
"""
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'tags',
            'text',
            'container'
        ]

class NotebookForm(ModelForm):
    class Meta:
        model = Notebook
        fields = [
            'title',
            'color'
        ]

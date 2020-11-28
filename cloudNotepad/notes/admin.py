from django.contrib import admin
from .models import Note
from .models import Notebook

# Register your models here.
admin.site.register(Note)
admin.site.register(Notebook)

class NoteAdmin(admin.ModelAdmin):
    # search_fields = ['foreign_key__related_fieldname']
    pass

class NotebookAdmin(admin.ModelAdmin):
    pass
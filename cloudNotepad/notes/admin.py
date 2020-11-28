from django.contrib import admin
from .models import Note
# from .models import Notebook

# Register your models here.
admin.site.register(Note)
# admin.site.register(Notebook)

class NoteAdmin(admin.ModelAdmin):
    pass
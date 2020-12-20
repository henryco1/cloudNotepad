from django import forms
from notes.models import Notebook
from ckeditor.widgets import CKEditorWidget

class NoteForm(forms.Form):
    title = forms.CharField(label='title', max_length=50)
    tags = forms.CharField(label='tags', max_length=25, required=False)
    text = forms.CharField( widget=CKEditorWidget)
    container = forms.ModelChoiceField(queryset=Notebook.objects.all())
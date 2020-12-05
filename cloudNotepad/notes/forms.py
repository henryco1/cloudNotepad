from django import forms

class NoteForm(forms.Form):
    title = forms.CharField(label='title', max_length=50)
    tags = forms.Charield(label='tags', max_length=25)
    text = forms.TextField(label='text')
    container = forms.ModelChoiceField(label='folder')
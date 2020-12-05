from django.shortcuts import redirect, render
from django.http import HttpResponse
from notes.models import Note, Notebook

from notes.forms import NoteForm

# Create your views here.
def HomePage(request):
    if request.method == 'POST':
        
        # dummy_notebook = Notebook.objects.first()
        Note.objects.create(
            title=request.POST['title'], 
            tags=request.POST['tags'], 
            text=request.POST['text'], 
            container=Notebook.objects.get(title=request.POST['container'])
        )
        
        return redirect('/')
    elif request.method == 'GET':
        name_form = NoteForm

        # initialize default notebook
        curr_notebooks = Notebook.objects.all()
        if curr_notebooks.count() == 0:
            Notebook.objects.create()

    notes = Note.objects.all()
    notebooks = Notebook.objects.all()
    return render(request, 'home.html', {'notes': notes, 'notebooks': notebooks, 'form': name_form})

    # if request.method == 'POST':
    #     new_note_text = request.POST['note_text']
    #     Note.objects.create(text=new_note_text)
    # else:
    #     # always redirect after a POST
    #     new_note_text = ''

    # return render(request, 'home.html', {
    #     'new_note_text': request.POST.get('note_text', '')
    # })
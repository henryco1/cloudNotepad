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

        return redirect('/notepad/')
    elif request.method == 'GET':

        # initialize default notebook
        curr_notebooks = Notebook.objects.all()
        if curr_notebooks.count() == 0:
            Notebook.objects.create()

    notes = Note.objects.all()
    name_form = NoteForm({
        "title": notes.first().title,
        "tags": notes.first().tags,
        "text": notes.first().text,
    })
    notebooks = Notebook.objects.all().first()
    return render(request, 'home.html', {'notes': notes, 'notebooks': notebooks, 'form': name_form})

# Create your views here.
def NotePage(request, title, slug):
    if request.method == 'POST':
        
        # dummy_notebook = Notebook.objects.first()
        new_note = Note.objects.create(
            title=request.POST['title'], 
            tags=request.POST['tags'], 
            text=request.POST['text'], 
            container=Notebook.objects.get(title=request.POST['container'])
        )

        return redirect('/notepad/note/'+new_note.title+'/'+new_note.slug)

    # Otherwise we handle a get request

    # if request.path returns '/notepad/note/<str:title>/<slug:slug>/', splitting the string 
    # results in ['', 'notepad', 'note', '<str:title>', '<slug:slug>', '']
    curr_path = request.path.split('/')
    curr_slug = curr_path[4]

    curr_note = Note.objects.get(slug=curr_slug)
    name_form = NoteForm({
        "title": curr_note.title,
        "tags": curr_note.tags,
        "text": curr_note.text,
    })
    curr_notebook = curr_note.container
    notes = Note.objects.all()
    return render(request, 'home.html', {'notes': notes, 'notebooks': curr_notebook, 'form': name_form})

def NotebookPage(request, title, slug):
    if request.method == 'POST':
        return redirect('/notepad/notebook/' + request.POST['container'].slug + '/')
    elif request.method == 'GET':
        # initialize default notebook
        curr_notebooks = Notebook.objects.all()
        if curr_notebooks.count() == 0:
            Notebook.objects.create(title='My Notebook')

    notes = Note.objects.filter(container="My Notebook")
    # notebook = Notebook.objects.all()
    notebook = Notebook.objects.filter(slug=slug)
    return render(request, 'notebook.html', {'notes': notes, 'notebook': notebook})
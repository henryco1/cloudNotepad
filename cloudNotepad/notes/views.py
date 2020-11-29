from django.shortcuts import redirect, render
from django.http import HttpResponse
from notes.models import Note, Notebook

# Create your views here.
def HomePage(request):
    if request.method == 'POST':
        
        # dummy_notebook = Notebook.objects.first()
        Note.objects.create(text=request.POST['note_text'], container=Notebook.objects.create())
        return redirect('/')

    notes = Note.objects.all()
    return render(request, 'home.html', {'notes': notes})

    # if request.method == 'POST':
    #     new_note_text = request.POST['note_text']
    #     Note.objects.create(text=new_note_text)
    # else:
    #     # always redirect after a POST
    #     new_note_text = ''

    # return render(request, 'home.html', {
    #     'new_note_text': request.POST.get('note_text', '')
    # })
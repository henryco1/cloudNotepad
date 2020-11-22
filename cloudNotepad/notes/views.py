from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def HomePage(request):
    return HttpResponse('<html><title>Notes</title></html>')
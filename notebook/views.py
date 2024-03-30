from django.http import Http404
from django.shortcuts import render
from .models import *

VALID_IDS = ['drylab','design']

# Create your views here.
def notebook(request, id):
    if id in VALID_IDS:
        notes = Notes.objects.filter(notebook=id).all().order_by('created').reverse()
    else:
        raise Http404('Notebook does not exist!')
    return render(request, "notebook/notebook.html", {'notes': notes})

def index(request):
    return render(request, 'notebook/index.html')
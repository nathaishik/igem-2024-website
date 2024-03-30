from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.
class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        exclude = ['user', 'id', 'created']
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": "true"}),
        }
    
    def clean(self):
        super(NewNoteForm, self).clean()
        return self.cleaned_data


def index(request):
    return render(request, "notebook/index.html")

@login_required
def dashboard(request):
    notes = Notes.objects.filter(user=request.user).all().order_by("created").reverse()
    return render(request, 'notebook/dashboard.html', {
        "notes": notes
    })

@login_required
def upload(request):
    if request.method == "POST":
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            notebook = form.cleaned_data["notebook"]
            content = form.cleaned_data["content"]
            file = form.cleaned_data["file"]
            note = Notes(
                user=request.user,
                title=title,
                notebook=notebook,
                content=content,
                file=file
            )
            note.save()  
            return HttpResponseRedirect(reverse("notebook:dashboard"), status=201)
        else:
            return render(request, 'notebook/upload.html', {
                "form": form
            })
    return render(request, 'notebook/upload.html', {
        "form": NewNoteForm()
    })

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        if password != confirmation:
            return render(request, 'notebook/register.html', {
                "message": "Passwords must match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first
            user.last_name = last
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("notebook:dashboard"))
        except IntegrityError:
            return render(request, 'notebook/register.html', {
                "message": "Username already taken"
            })
    return render(request, 'notebook/register.html', {
    })
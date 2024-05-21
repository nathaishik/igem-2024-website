from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import *
from markdown2 import Markdown
import os

# Create your views here.
class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user', 'id', 'created']
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": "true", "placeholder": "Title"}),
            "content": forms.Textarea(attrs={"placeholder": "You can use markdown and LaTeX here!"}),
            "published": forms.CheckboxInput(attrs={"class": "toggle_button"}),
        }
    
    def clean(self):
        super(NewNoteForm, self).clean()
        return self.cleaned_data

def index(request):
    return render(request, "notebook/index.html", {
        "departments": Department.objects.all()
    })

def notebook(request, code):
    try:
        department = Department.objects.get(code=code)
    except Department.DoesNotExist:
        raise Http404('Notebook does not exist!')
    notes = Note.objects.filter(department=department, published=True).all().order_by('last_edited').reverse()
    return render(request, "notebook/notebook.html", {
        'notes': notes,
        'notebook': department.name
    })

def note(request, id):
    note = Note.objects.get(id=id)
    md = Markdown()
    try:
        note.content = md.convert(note.content)
    except:
        note.content = "Markprocessing error" + note.content
    return render(request, "notebook/note.html", {'note': note})



@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user).all().order_by('last_edited').reverse()
    return render(request, 'notebook/dashboard.html', {
        "notes": notes
    })

@login_required
def admin(request):
    pass

@login_required
def manage_note(request):
    heading = "Edit Note"
    if request.method == "POST" and request.POST.get("delete"):
        note = Note.objects.get(id=request.POST["delete"])
        if request.user != note.user:
            return HttpResponseRedirect(reverse("notebook:login"))
        note.delete()
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    if request.method == "POST" and request.POST.get("edit"):
        note = Note.objects.get(id=request.POST["edit"])
        if request.user != note.user:
            return HttpResponseRedirect(reverse("notebook:login"))
        form = NewNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            title = form.cleaned_data["title"]
            department = form.cleaned_data["department"]
            content = form.cleaned_data["content"]
            published= form.cleaned_data["published"]
            note.title = title
            note.department = department
            note.content = content
            note.published = published
            note.save()
            return HttpResponseRedirect(reverse("notebook:note", args=[note.id]))
        else:
            return render(request, 'notebook/manage_note.html', {
                "form": form,
                "args": note.id,
                "link": "notebook:manage_note",
                "message": "Something went wrong. Please try again.",
                "title": heading,
            }, status=406)
    return render(request, 'notebook/manage_note.html', {
        "link": "notebook:manage_note",
        "note_id": Note.objects.get(id=request.GET["edit"]).id,
        "form": NewNoteForm(instance=Note.objects.get(id=request.GET["edit"])),
        "title": heading,
    })

@login_required
def upload(request):
    heading = "New Note"
    if request.user.verified == False:
        return HttpResponseRedirect(reverse("notebook:dashboard"), status=302)
    if request.method == "POST":
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            department = form.cleaned_data["department"]
            content = form.cleaned_data["content"]
            file = form.cleaned_data["file"]
            published = form.cleaned_data["published"]
            note = Note(
                user=request.user,
                title=title,
                department=department,
                content=content,
                file=file,
                published=published
            )
            note.save()
            return HttpResponseRedirect(reverse("notebook:dashboard"))
        else:
            return render(request, 'notebook/manage_note.html', {
                "form": form,
                "link": "notebook:upload",
                "title": heading,
                "message": "Something went wrong. Please try again.",
            }, status=406)
    return render(request, 'notebook/manage_note.html', {
        "form": NewNoteForm(),
        "link": "notebook:upload",
        "title": heading,
    })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("notebook:dashboard"))
        else:
            return render(request, 'notebook/login.html', {
                "message": "Invalid credentials"
            })
    return render(request, 'notebook/login.html', {
    })

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("notebook:index"))

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
                "message": "Invalid username"
            })
    return render(request, 'notebook/register.html', {
    })
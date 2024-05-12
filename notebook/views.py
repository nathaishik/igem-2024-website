from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import *
from markdown2 import Markdown

# Create your views here.
class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user', 'id', 'created', 'published']
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": "true", "placeholder": "Title"}),
            "content": forms.Textarea(attrs={"placeholder": "You can use markdown here!"}),
        }
    
    def clean(self):
        super(NewNoteForm, self).clean()
        return self.cleaned_data

def notebook(request, id):
    VALID_IDS = {
        "drylab": ["DRYLAB", "Dry Lab"],
        "wetlab": ["WETLAB", "Wet Lab"],
        "webdev": ["WEBDEV", "Web Development"],
        "design": ["DESIGN", "Design"],
        "hp": ["HMNPRC", "Human Practices"],
    }
    if id in VALID_IDS.keys():
        department = Department.objects.get(code=VALID_IDS[id][0])
        notes = Note.objects.filter(dept=department).all().order_by('created').reverse()
        print(notes)
    else:
        raise Http404('Notebook does not exist!')
    return render(request, "notebook/notebook.html", {
        'notes': notes,
        'notebook': department
    })

def note(request, id):
    note = Note.objects.get(id=id)
    md = Markdown()
    try:
        note.content = md.convert(note.content)
    except:
        pass
    return render(request, "notebook/note.html", {'note': note})

def index(request):
    return render(request, "notebook/index.html")

@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user).all().order_by('created').reverse()
    return render(request, 'notebook/dashboard.html', {
        "notes": notes
    })

@login_required
def admin(request):
    pass

def manage_note(request, id):
    note = Note.objects.get(id=id)
    if request.method == "POST":
        if request.POST.get("delete"):
            note.delete()
            return HttpResponseRedirect(reverse("notebook:dashboard"))
        if request.POST.get("edit"):
            form = NewNoteForm(request.POST, request.FILES, instance=note)
            if form.is_valid():
                title = form.cleaned_data["title"]
                notebook = form.cleaned_data["notebook"]
                content = form.cleaned_data["content"]
                file = form.cleaned_data["file"]
                published = form.cleaned_data["published"]
                note.title = title
                note.notebook = notebook
                note.content = content
                note.file = file
                note.published = published
                note.save()
                return HttpResponseRedirect(reverse("notebook:dashboard"))
            else:
                return render(request, 'notebook/upload.html', {
                    "form": form
                })
    return render(request, 'notebook/upload.html', {
        "form": NewNoteForm(instance=note)
    })

@login_required
def upload(request):
    if request.user.verified == False:
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    if request.method == "POST":
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            notebook = form.cleaned_data["notebook"]
            content = form.cleaned_data["content"]
            file = form.cleaned_data["file"]
            note = Note(
                user=request.user,
                title=title,
                notebook=notebook,
                content=content,
                file=file
            )
            note.save()  
            return HttpResponseRedirect(reverse("notebook:dashboard"))
        else:
            return render(request, 'notebook/upload.html', {
                "form": form
            })
    return render(request, 'notebook/upload.html', {
        "form": NewNoteForm()
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
                "message": "Username already taken"
            })
    return render(request, 'notebook/register.html', {
    })
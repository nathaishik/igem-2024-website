from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse
from .models import *
from markdown2 import Markdown
from .forms import *

# Create your views here.

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
        'notebook': department.name,
        'departments': Department.objects.all()
    })

def note(request, id):
    note = Note.objects.get(id=id)
    md = Markdown()
    try:
        note.content = md.convert(note.content)
    except:
        note.content = "Markprocessing error" + note.content
    return render(request, "notebook/note.html", {
        'note': note,
        'departments': Department.objects.all()
    })



@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user).all().order_by('last_edited').reverse()
    return render(request, 'notebook/dash_notes.html', {
        "notes": notes,
    })

@login_required
def teams(request, typeId):
    if typeId not in ['all','my','other']:
        raise Http404('Page does not exist!')

    if typeId=='all':
        if not request.user.position == 'STUDLDR':
            raise PermissionDenied
        team_list = Department.objects.all()
    elif typeId=='my':
        team_list = request.user.leader_of.all().union(request.user.departments.all())
    elif typeId=='other':
        team_list = Department.objects.all().difference(request.user.departments.all().union(request.user.leader_of.all()))
    
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        department = Department.objects.get(code=request.POST['code'])
        department.waitlist.add(user)
    return render(request, 'notebook/teams.html',{
        "teams": team_list
    })

@login_required
def team(request, code, typeId):
    try:
        department = Department.objects.get(code=code)
    except ObjectDoesNotExist:
        raise Http404('Page does not exist!')
    
    if typeId == 'Waitlist':
        if request.user not in department.leader.all():
            raise PermissionDenied
        userlist = department.waitlist.all()
        buttonlist = ['Verify']
    elif typeId == 'Members':
        userlist = department.members.all()
        buttonlist = []
        if request.user in department.leader.all():
            buttonlist = ['Make Leader', 'Remove']
    elif typeId == 'Leaders':
        userlist = department.leader.all()
        buttonlist =[]
    else:
        raise Http404('Page does not exist!')
    
    if request.method == "POST":
        if request.user not in department.leader.all():
            raise PermissionDenied
        clicked_user= User.objects.get(username=request.POST['username'])
        if 'Verify' in request.POST:
            department.waitlist.remove(clicked_user)
            department.members.add(clicked_user)
        elif 'Remove' in request.POST:
            department.members.remove(clicked_user)
        elif 'Make Leader' in request.POST:
            department.members.remove(clicked_user)
            department.leader.add(clicked_user)

    return render(request, 'notebook/team.html',{
        "team" : department,
        "userlist" : userlist,
        "buttonlist": buttonlist
    })

def upload_images(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse("notebook:login"))
    if request.user.verified == False:
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = form.cleaned_data["image"]
            image = AttachedImages(user=request.user, image=images)
            image.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse({"error": "Something went wrong. Please try again."}, status=406)

@login_required
def manage_note(request):
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
        form = NewNoteForm(request.user, request.POST, request.FILES, instance=note)
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
            }, status=406)
    return render(request, 'notebook/manage_note.html', {
        "link": "notebook:manage_note",
        "note_id": Note.objects.get(id=request.GET["edit"]).id,
        "form": NewNoteForm(request.user, instance=Note.objects.get(id=request.GET["edit"])),
        "image_upload_form": ImageForm(),
        "images": AttachedImages.objects.filter(user=request.user).all(),
    })

@login_required
def upload(request):
    if request.user.verified == False:
        return HttpResponseRedirect(reverse("notebook:dashboard"), status=302)
    if request.method == "POST":
        form = NewNoteForm(request.user, request.POST, request.FILES)
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
                "message": "Something went wrong. Please try again.",
            }, status=406)
    return render(request, 'notebook/manage_note.html', {
        "form": NewNoteForm(request.user),
        "link": "notebook:upload",
        "image_upload_form": ImageForm(),
        "images": AttachedImages.objects.filter(user=request.user).all(),
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
            return HttpResponseRedirect(reverse("notebook:teams",args=['all']))
        except IntegrityError:
            return render(request, 'notebook/register.html', {
                "message": "Invalid username"
            })
    return render(request, 'notebook/register.html', {
    })
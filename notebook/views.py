from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse
from .models import *
from django.contrib.auth.password_validation import validate_password, password_changed
import json
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
        note.content = "Markdown processing error" + note.content
    return render(request, "notebook/note.html", {
        'note': note,
        'departments': Department.objects.all()
    })



@login_required
def dashboard(request):
    if request.GET.get('filter'):
        if request.GET['filter'] == 'drafts':
            notes = Note.objects.filter(user=request.user, published=False).all().order_by('last_edited').reverse()
        elif request.GET['filter'] == 'all' and request.user.position == 3:
            notes = Note.objects.filter(published=True).all().all().order_by('last_edited').reverse()
        else:
            return HttpResponseRedirect(reverse("notebook:dashboard"))
    else:
        notes = Note.objects.filter(user=request.user, published=True).all().order_by('last_edited').reverse()
    return render(request, 'notebook/dash_notes.html', {
        "notes": notes,
    })

@login_required
def teams(request):
    if request.method == "POST":
        if request.POST.get("code"):
            department = Department.objects.get(code=request.POST['code'])
            if request.POST.get('action') == 'join':
                if department in request.user.departments.all() | request.user.waitlist.all() :
                    return HttpResponseRedirect(reverse("notebook:team", args=[department.code]))
                if request.user.position > 1:
                    department.members.add(request.user)
                    return HttpResponseRedirect(reverse("notebook:team", args=[department.code]))
                department.waitlist.add(request.user)
            elif request.POST.get('action') == 'withdraw' and request.user in department.waitlist.all():
                department.waitlist.remove(request.user)
            elif request.POST.get('action') == 'leave' and request.user in department.members.all():
                department.members.remove(request.user)
                if request.user in department.leader.all():
                    department.leader.remove(request.user)
            else:
                return HttpResponse("<h1>400</h1>No proper action received.", status=400)
            return HttpResponseRedirect(reverse("notebook:teams") + "?filter=all")
        else:
            return HttpResponse("<h1>400</h1>Error fetching the team.", status=400)
    if request.GET.get('filter') == 'all':
        team_list = Department.objects.all()
    else:
        team_list = request.user.departments.all() | request.user.leader_of.all()
    return render(request, 'notebook/teams.html',{
        "teams": team_list

    })

@login_required
def team(request, code):
    try:
        department = Department.objects.get(code=code)
    except ObjectDoesNotExist:
        raise Http404('Team does not exist!')
    
    if request.method == "POST":
        if request.user not in department.leader.all() and request.user.position == 1:
            raise PermissionDenied
        clicked_user= User.objects.get(username=request.POST['username'])
        if clicked_user not in department.members.all():
            if request.POST.get('action') == 'add':
                department.members.add(clicked_user)
                department.waitlist.remove(clicked_user)
            elif request.POST.get('action') == 'remove':
                department.waitlist.remove(clicked_user)
            else:
                return HttpResponse("<h1>400</h1>No proper action received.", status=400)
        else:
            if clicked_user not in department.leader.all():
                if request.POST.get('action') == 'remove':
                    department.members.remove(clicked_user)
                elif request.POST.get('action') == 'promote':
                    department.leader.add(clicked_user)
            elif request.user.position == 3:
                if request.POST.get('action') == 'demote':
                    department.leader.remove(clicked_user)
                elif request.POST.get('action') == 'remove':
                    department.leader.remove(clicked_user)
                    department.members.remove(clicked_user)
                else:
                    return HttpResponse("<h1>400</h1>No proper action received.", status=400)
            else:
                raise PermissionDenied
        return HttpResponseRedirect(reverse("notebook:team", args=[department.code]))
    
    if (request.user in department.leader.all() or request.user.position > 1) and request.GET.get('fetch') == 'waitlist':
        userlist = department.waitlist.filter(verified=True).all()
    else:
        userlist = department.members.filter(leader_of=department).all() | department.members.exclude(leader_of=department).all()
    return render(request, 'notebook/team.html',{
        "team" : department,
        "memberlist" : userlist,
    })

@login_required
def upload_images(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse("notebook:login"))
    if request.user.verified == False:
        return HttpResponseRedirect(reverse("notebook:dashboard"))
    if request.method == "POST" and request.FILES.get("image") is not None:
        img = AttachedImages(user=request.user, image=request.FILES["image"])
        img.save()
        image_list = AttachedImages.objects.filter(user=request.user).all()
        return JsonResponse({"images": image.serialise() for image in image_list})
    if request.method == 'DELETE':
        data = json.loads(request.body)
        if data.get("id"):
            image = AttachedImages.objects.get(id=data["id"])
            if image.user != request.user:
                return JsonResponse({"error": "You are not authorised to delete this image."}, status=403)
            image.delete()
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"error": "ID not found."}, status=403)
    else:
        return JsonResponse({"error": "Something went wrong. Please try again."}, status=403)
    

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
            }, status=403)
    return render(request, 'notebook/manage_note.html', {
        "link": "notebook:manage_note",
        "note_id": Note.objects.get(id=request.GET["edit"]).id,
        "form": NewNoteForm(request.user, instance=Note.objects.get(id=request.GET["edit"])),
        "images": AttachedImages.objects.filter(user=request.user).order_by("-created").all()
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
            }, status=403)
    return render(request, 'notebook/manage_note.html', {
        "form": NewNoteForm(request.user),
        "link": "notebook:upload",
        "images": AttachedImages.objects.filter(user=request.user).all()
        })

@login_required
def admin(request):
    if request.user.position != 3:
        raise PermissionDenied
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
        except ObjectDoesNotExist:
            return HttpResponse("<h1>400</h1>Error fetching the user.", status=400)
        if request.POST.get("action") == 'revoke':
            if user != request.user:
                user.position = None
                user.verified = False
                user.save()
            else:
                return HttpResponse("<h1>400</h1>You cannot change your own verification.", status=400)
        elif request.POST.get("action") == 'verify' and request.POST.get("position") in ['1', '2', '3']:
            user.position = request.POST["position"]
            user.verified = True
            user.save()
        elif request.POST.get("action") == 'update' and request.POST.get("position") in ['1', '2', '3']:
                user.position = request.POST["position"]
                user.save()
        else:
            return HttpResponse("<h1>400</h1>Proper fields not received.", status=400)
    if request.GET.get('filter') == 'new':
        users = User.objects.filter(verified=False).all()
    else:
        users = User.objects.filter(verified=True).all()
    return render(request, 'notebook/admin.html', {
        "departments": Department.objects.all(),
        "users": users,
        "unverified": User.objects.filter(verified=False).count()
    })

@login_required
def account(request):
    if request.method == "POST":
        if request.POST.get("first_name"):
            request.user.first_name = request.POST["first_name"]
        if request.POST.get("last_name"):
            request.user.last_name = request.POST["last_name"]
        if request.POST.get("email"):
            request.user.email = request.POST["email"]
        request.user.save()
    return render(request, 'notebook/account.html', {
        "user": request.user
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
    return HttpResponseRedirect(reverse("notebook:login"))

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
            validate_password(request.POST["password"])
        except:
            return render(request, 'notebook/register.html', {
                "message": "Password not strong enough."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first
            user.last_name = last
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("notebook:teams"))
        except IntegrityError:
            return render(request, 'notebook/register.html', {
                "message": "Invalid username"
            })
    return render(request, 'notebook/register.html', {
    })
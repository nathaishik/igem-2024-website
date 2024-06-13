from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django_distill import distill_path
from .models import *

def get_notebooks():
    for department in Department.objects.all():
        yield {'code': department.code}

def get_notes():
    for note in Note.objects.all():
        yield {'id': note.id}

app_name = 'notebook'

urlpatterns = [
    distill_path('', views.index, name='index', distill_file='index.html'),
    path('new/', views.upload, name='upload'),
    path('notes/', views.dashboard, name='dashboard'),
    distill_path('notebook/<str:code>.html', views.notebook, name='notebook', distill_func=get_notebooks),
    distill_path('note/<str:id>.html', views.note, name='note', distill_func=get_notes),
    path('manage_note', views.manage_note, name='manage_note'),
    path('image-upload', views.upload_images, name='image_upload'),
    path('teams', views.teams, name='teams'),
    path('teams/<str:code>',views.team, name='team'),
    path('users', views.admin, name='admin'),
    path('signup/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path("change-password/", auth_views.PasswordChangeView.as_view(), name="change_password"),
]
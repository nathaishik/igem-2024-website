from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .models import *

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.upload, name='upload'),
    path('notes/', views.dashboard, name='dashboard'),
    path('notebook/<str:code>', views.notebook, name='notebook'),
    path('note/<str:id>', views.note, name='note'),
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
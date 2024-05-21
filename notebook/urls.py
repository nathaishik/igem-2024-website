from django.urls import path
from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.upload, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notebook/<str:code>', views.notebook, name='notebook'),
    path('note/<str:id>', views.note, name='note'),
    path('manage_note', views.manage_note, name='manage_note'),
    path('signup/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teams/', views.teams, name='teams'),
    path('manage/',views.admin, name='manage'),
    path('manage/verify/<str:code>',views.verify, name='verify'),
    path('manage/roles/<str:code>',views.roles, name='roles')
]
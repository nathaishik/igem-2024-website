from django.urls import path
from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.upload, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notebook/<str:id>', views.notebook, name='notebook'),
    path('note/<str:id>', views.note, name='note'),
    path('signup/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
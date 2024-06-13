from . import views
from django_distill import distill_path
from .models import *

def get_notebooks():
    for department in Department.objects.all():
        yield {'code': department.code}

def get_notes():
    for note in Note.objects.all():
        yield {'id': note.id}

app_name = 'notebook'

SITE = 'igem-2024-website'

urlpatterns = [
    distill_path(SITE, views.index, name='index', distill_file='index.html'),
    distill_path(f'{SITE}/notebook/<str:code>.html', views.notebook, name='notebook', distill_func=get_notebooks),
    distill_path(f'{SITE}/note/<str:id>.html', views.note, name='note', distill_func=get_notes),
]
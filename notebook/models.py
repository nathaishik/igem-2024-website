from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
def upload_files(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s__%s_%s.%s" % (instance.user.username, instance, uuid.uuid4().hex, ext)
    return "{0}/{1}/{2}".format(instance.notebook, "files", filename)

DEPT_CHOICES = [
    ("DRYLAB", "Dry Lab"),
    ("WETLAB", "Wet Lab"),
    ("WEBDEV", "Web Development"),
    ("DESIGN", "Design"),
    ("HMNPRC", "Human Practices"),
]

class User(AbstractUser):
    global DEPT_CHOICES
    POSITION_CHOICES = [
        ("STUDLDR", "Student Leader"),
        ("STUDENT", "Students"),
        ("TEAMLDR", "Team Leader"),
        ("PRMRYPI", "Primary PI"),
        ("ADVISOR", "Advisor"),
    ]

    position = models.CharField(max_length=7, choices=POSITION_CHOICES)
    team = models.CharField(max_length=6, choices=DEPT_CHOICES)
    email_verified = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    pass

class Note(models.Model):
    global DEPT_CHOICES
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notes")
    title = models.CharField(max_length=255)
    notebook = models.CharField(max_length=6, choices=DEPT_CHOICES)
    file = models.FileField(upload_to=upload_files, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    id = models.TextField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    
    def __str__(self):
        return f"{self.title} by {'User no longer exists' if self.user == None else self.user.username}"
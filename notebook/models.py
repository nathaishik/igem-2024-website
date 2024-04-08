from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
def upload_files(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s__%s_%s.%s" % (instance.user.username, instance, uuid.uuid4().hex, ext)
    return "{0}/{1}/{2}".format(instance.notebook, "files", filename)


class User(AbstractUser):
    POSITION_CHOICES = [
        ("STUDLDR", "Student Leader"),
        ("STUDENT", "Students"),
        ("PRMRYPI", "Primary PI"),
        ("ADVISOR", "Advisor"),
    ]
    TEAM_CHOICES = [
        ("DRYLAB", "Dry Lab"),
        ("WETLAB", "Wet Lab"),
        ("WEBDEV", "Web Development"),
        ("DESIGN", "Design"),
        ("HMNPRC", "Human Practices"),
    ]
    position = models.CharField(max_length=7, choices=POSITION_CHOICES)
    team = models.CharField(max_length=6, choices=TEAM_CHOICES)
    verified = models.BooleanField(default=False)
    pass

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    NOTE_CHOICES = [
    ("DRYLAB", "Dry Lab"),
    ("WETLAB", "Wet Lab"),
    ("WEBDEV", "Web Development"),
    ("DESIGN", "Design"),
    ("HMNPRC", "Human Practices"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notes")
    title = models.CharField(max_length=255)
    notebook = models.CharField(max_length=6, choices=NOTE_CHOICES)
    content = models.TextField()
    file = models.FileField(upload_to=upload_files, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {'User no longer exists' if self.user == None else self.user.username}"
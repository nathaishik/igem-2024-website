from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
def upload_files(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s.%s" % (instance.user.username, instance, uuid.uuid4().hex, ext)
    return "{0}/{1}/{2}".format(instance.department, "files", filename)

class User(AbstractUser):
    POSITION_CHOICES = [
        ("STUDLDR", "Student Leader"),
        ("STUDENT", "Students"),
        ("PRMRYPI", "Primary PI"),
        ("ADVISOR", "Advisor"),
    ]
    position = models.CharField(max_length=7, choices=POSITION_CHOICES, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, unique=True)
    leader = models.ManyToManyField(User, blank=True, related_name="leader_of")
    members = models.ManyToManyField(User, blank=True, related_name="departments")
    waitlist = models.ManyToManyField(User, blank=True, related_name="waitlist")
    
    def __str__(self):
        return self.name
    
    def published_notes(self):
        return self.notes.filter(published=True).all()

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notes")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="notes")
    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    file = models.FileField(upload_to=upload_files, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {'User no longer exists' if self.user == None else self.user.username}"

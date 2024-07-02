from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
import uuid
import os

def filename_separator(filename):
    filename = filename[::-1].split(".", 1)
    ext = filename[0][::-1]
    filename = filename[1][::-1]
    return [filename, ext]

# Create your models here.
def upload_files(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s.%s" % (instance.user.username, instance, uuid.uuid4().hex, ext)
    return "{0}/{1}/{2}".format(instance.department, "files", filename)

def upload_images(instance, filename):
    file = filename_separator(filename)
    ext = file[1]
    filename = "%s_%s.%s" % (file[0], uuid.uuid4().hex, ext)
    return "{0}/{1}/{2}".format(instance.user.username, "images", filename)

class User(AbstractUser):
    POSITION_CHOICES = [
        (3, "Student Leader"),
        (2, "PI/Advisor"),
        (1, "Student"),
    ]
    position = models.IntegerField(choices=POSITION_CHOICES, default=1)

    def waitlist_pending(self):
        if self.position > 1:
            dept_list = Department.objects.all()
        else:
            dept_list = self.departments.all() | self.leader_of.all()
        for dept in dept_list:
            if dept.waitlist.all().count() > 0:
                return True
        return False

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

class AttachedImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="images")
    image = models.ImageField(upload_to=upload_images, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id} by {'User no longer exists' if self.user == None else self.user.username}"
    
    def location(self):
        filename = os.path.basename(self.image.name)
        file = filename_separator(filename)
        filename = file[0][::-1]
        name = filename.split("_", 1)[1][::-1]
        return f"{name}.{file[1]}"

    
    def serialise(self):
        return {
            "url": self.image.url,
            "location": self.location(),
            "id": self.id,
        }

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notes")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="notes")
    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    file = models.FileField(upload_to=upload_files, null=True, blank=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {'User no longer exists' if self.user == None else self.user.username}"


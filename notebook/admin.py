from django.contrib import admin
from .models import *

class DepartmentAdmin(admin.ModelAdmin):
    filter_horizontal = ['leader', 'members', 'waitlist',]

# Register your models here.
admin.site.register(User)
admin.site.register(Note)
admin.site.register(Department, DepartmentAdmin)
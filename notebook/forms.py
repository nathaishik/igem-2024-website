from django import forms
from .models import Note, Department, AttachedImages

class NewNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        exclude = ['user', 'id', 'created', 'last_edited']
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": "true", "placeholder": "Title"}),
            "content": forms.Textarea(attrs={"placeholder": "You can use markdown and LaTeX here!"}),
            "published": forms.CheckboxInput(attrs={"class": "toggle_button"}),
        }

        labels = {
            "department": ("Team"),
        }

    def __init__(self, user, *args, **kwargs):
        super(NewNoteForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = (user.departments.all() | user.leader_of.all()) if user.position != "STUDLDR" else Department.objects.all()
        if self.fields['department'].queryset.count() > 0:
            self.fields['department'].empty_label = None if self.fields['department'].queryset.count() == 1 else "Choose team..."
        else:
            self.fields['department'].empty_label = "No teams available"
    
    def clean(self):
        super(NewNoteForm, self).clean()
        return self.cleaned_data
    
class ImageForm(forms.ModelForm):

    class Meta:
        model = AttachedImages
        exclude = ['user', 'id', 'created']
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

        labels = {
            "image": ("Upload Images"),
        }

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].widget.attrs["multiple"] = True
        self.fields['image'].widget.attrs["accept"] = "image/*"
    
    def clean(self):
        super(ImageForm, self).clean()
        return self.cleaned_data
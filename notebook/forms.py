from django import forms
from .models import Note, Department

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
    
from django import forms
from .models import Tag, Note
from django.core.exceptions import ValidationError

class NoteAddForm(forms.ModelForm):
    title = forms.CharField(label="Заголовок")
    content = forms.Textarea()
    # slug = forms.SlugField(label="Слаг")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label="Список тегов", widget=forms.CheckboxSelectMultiple, required=True)


    class Meta:
        model = Note
        fields = ('title', 'content', 'tags')
        widgets = {
                "title": forms.TextInput(attrs={"class": "form-control"}),
                "content": forms.Textarea(attrs={"class": "form-control"}),
                "author": forms.HiddenInput,
                }


class TagAddForm(forms.ModelForm):
    name = forms.CharField(label="Тэг")
    # slug = forms.SlugField(label="Слаг")

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        return new_slug

    def clean_name(self):
        new_name = self.cleaned_data['name'].lower()
        return new_name

    class Meta:
        model = Tag
        fields = ('name',)
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"}),
                "author": forms.HiddenInput,
                }

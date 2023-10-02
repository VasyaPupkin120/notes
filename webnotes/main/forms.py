from django import forms
from django.forms.widgets import TextInput, Textarea
from .models import Tag, Note
from django.core.exceptions import ValidationError

class NoteAddForm(forms.ModelForm):
    title = forms.CharField(label="Заголовок", widget=TextInput(attrs={"class": "form-control forms-field-color"}))
    content = forms.CharField(label="Содержание", widget=Textarea(attrs={"class": "form-control forms-field-color"}))
    # slug = forms.SlugField(label="Слаг")
    tags = forms.ModelMultipleChoiceField(queryset=None, label="Список тегов", widget=forms.CheckboxSelectMultiple, required=True)


    def __init__(self, *args, **kwargs):
        """
        Переопределение для использования проброшенного в форму запроса request
        для ограничения тегов только теми, которые принадлежат данному пользователю
        """
        super().__init__(*args, **kwargs)
        # судя по всему, initial - это данные для внесения в форму при get-запросе, по умолчанию этот словарь заполняется в FormMixin, 
        #!!!!А В МОЕМ СЛУЧАЕ ОН ДОПОЛНЯЕТСЯ В views.NoteFormCreate.get_form и  vievs.NoteUpdate
        # дополняется этот словарь копией запроса request, так как похоже по дефолту он в форму не передается
        self.user_pk = kwargs["initial"]["request"].user.pk
        # обращение к полям идет через атрибут fields (увидел где то в исходниках)
        self.fields["tags"].queryset = Tag.objects.filter(author=self.user_pk)

    class Meta:
        model = Note
        fields = ('title', 'content', 'tags')



class TagAddForm(forms.ModelForm):
    name = forms.CharField(label="Тэг", widget=TextInput(attrs={"class": "form-control forms-field-color"}))
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

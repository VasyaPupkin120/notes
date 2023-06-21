from django.shortcuts import render

from .models import Tag, Note
# Create your views here.

def index(request):
    notes_list = Note.objects.all()
    tags_list = Tag.objects.all()
    context = {"notes_list": notes_list, "tags_list": tags_list}
    return render(request, 'index.html', context=context)

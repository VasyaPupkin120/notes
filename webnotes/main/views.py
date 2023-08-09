from django.db.models import Q, QuerySet
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from .models import Tag, Note
from .forms import NoteAddForm, TagAddForm


# чтоб не забыть как выглядят функции-обработчики
# def index(request):
#     notes_list = Note.objects.all()
#     tags_cloud = Tag.objects.all()
#     context = {"notes_list": notes_list, "tags_cloud": tags_cloud}
#     return render(request, 'main/index.html', context=context)

search_request_global = ""


class Index(ListView):
    template_name = "main/index.html"
    model = Note
    context_object_name = "notes_list"
    queryset = Note.objects.all()
    paginate_by = 2


class NoteFormCreate(CreateView):
    template_name = "main/note_create.html"
    form_class = NoteAddForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context


class NoteRead(DetailView):
    model = Note
    template_name = "main/note_read.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context

class NoteUpdate(UpdateView):
    model = Note
    template_name = "main/note_update.html"
    form_class = NoteAddForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context

class NoteDelete(DeleteView):
    model = Note
    success_url = "/"
    template_name = "main/note_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context


class TagFormCreate(CreateView):
    template_name = "main/tag_create.html"
    form_class = TagAddForm
    success_url = reverse_lazy("tag_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagList(ListView):
    template_name = "main/tag_list.html"
    model = Tag
    context_object_name = "tags_list"
    queryset = Tag.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context


class TagLinkPosts(ListView):
    template_name = "main/tag_link_posts.html"
    context_object_name = "notes_list"
    paginate_by = 2

    def get_queryset(self):
        tag = Tag.objects.get(slug__iexact=self.kwargs["slug"])
        return tag.note_set.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context


class TagUpdate(UpdateView):
    model = Tag
    template_name = "main/tag_update.html"
    form_class = TagAddForm
    success_url = reverse_lazy("tag_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context



class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy("tag_list")
    template_name = "main/tag_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_cloud"] = Tag.objects.all()
        return context


class SearchList(ListView):
    template_name = "main/search_list.html"
    model = Note
    context_object_name = "notes_list"
    paginate_by: int = 2

    # для отладки 
    # def get(self, *args, **kwargs):
    #     print(self.queryset)
    #     return super().get(*args, **kwargs)

    def get_queryset(self):
        search_request = self.request.GET.get("field_search", "")
        #FIXME icontains для русских слов становится как contains - т.е. для учитывается регистр
        notes_list = Note.objects.filter(Q(title__icontains=search_request) | Q(content__icontains=search_request))
        return notes_list

    def get_context_data(self, **kwargs):
        global search_request_global
        context = super().get_context_data(**kwargs)

        # это для сохранения значения из поля поиска - т.е. после первого перехода по пагинациям оно теряется
        # этот код сохраняет значение и использует до получения нового значения
        if self.request.GET.get("field_search", None):
            search_request_global = self.request.GET["field_search"]
        context["search_request"] = search_request_global

        return context

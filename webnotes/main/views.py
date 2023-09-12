from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, QuerySet
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import Http404

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
    paginate_by = 10

    def get_queryset(self):
        current_author = self.request.user.pk
        notes_list = Note.objects.filter(author=current_author)
        return notes_list


class NoteFormCreate(CreateView):
    template_name = "main/note_create.html"
    form_class = NoteAddForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        """
        Переопределение нужно для проброса запроса request в форму NoteAddForm
        для ограничения списка тегов только теми тегами, которые принадлежат текущему пользователю.
        """
        self.initial.update({"request": self.request})
        return super().get_form(*args, **kwargs)




class NoteRead(DetailView):
    template_name = "main/note_read.html"

    # ограничение записей для выбора одной только соответствующими аутентифицированному пользователю
    def get_queryset(self):
        current_author = self.request.user.pk
        notes_list = Note.objects.filter(author=current_author)
        return notes_list


class NoteUpdate(UpdateView):
    model = Note
    template_name = "main/note_update.html"
    form_class = NoteAddForm
    success_url = "/"

    def get_queryset(self):
        current_author = self.request.user.pk
        notes_list = Note.objects.filter(author=current_author)
        return notes_list

    def get_form(self, *args, **kwargs):
        """
        Переопределение нужно для проброса запроса request в форму NoteAddForm
        для ограничения списка тегов только теми тегами, которые принадлежат текущему пользователю.
        """
        self.initial.update({"request": self.request})
        print(self.initial)
        return super().get_form(*args, **kwargs)


class NoteDelete(DeleteView):
    model = Note
    success_url = "/"
    template_name = "main/note_delete.html"

    def get_queryset(self):
        current_author= self.request.user.pk
        notes_list = Note.objects.filter(author=current_author)
        return notes_list

# @method_decorator(login_required, name="dispatch")
# class CreateProductView(CreateView):
#     template_name = "control/catalog/form-add.html"
#     form_class = SellProductAlphaForm
#     success_url = "/control/catalog/sell/edit/{id}"
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

class TagFormCreate(CreateView):
    template_name = "main/tag_create.html"
    form_class = TagAddForm
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TagList(ListView):
    template_name = "main/tag_list.html"
    model = Tag
    context_object_name = "tags_list"
    queryset = Tag.objects.all()

    def get_queryset(self):
        current_author = self.request.user.pk
        tags_list = Tag.objects.filter(author=current_author)
        return tags_list


class TagLinkPosts(ListView):
    template_name = "main/tag_link_posts.html"
    context_object_name = "notes_list"
    paginate_by = 10

    def get_queryset(self):
        current_author = self.request.user.pk
        filter_author = Q(author=current_author)
        filter_list_posts = Q(slug__iexact=self.kwargs["slug"])
        tags = Tag.objects.filter(filter_author & filter_list_posts) # в получившемся qeryset'е либо один тег либо нет тегов 
        if tags:
            return tags[0].note_set.all()
        else:
            raise Http404


class TagUpdate(UpdateView):
    model = Tag
    template_name = "main/tag_update.html"
    form_class = TagAddForm
    success_url = reverse_lazy("tag_list")

    def get_queryset(self):
        current_author = self.request.user.pk
        tags_list = Tag.objects.filter(author=current_author)
        return tags_list



class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy("tag_list")
    template_name = "main/tag_delete.html"

    def get_queryset(self):
        current_author = self.request.user.pk
        tags_list = Tag.objects.filter(author=current_author)
        return tags_list


class SearchList(ListView):
    template_name = "main/search_list.html"
    model = Note
    context_object_name = "notes_list"
    paginate_by: int = 10

    # для отладки 
    # def get(self, *args, **kwargs):
    #     print(self.queryset)
    #     return super().get(*args, **kwargs)

    def get_queryset(self):
        #FIXME icontains для русских слов становится как contains - т.е. для учитывается регистр
        search_request = self.request.GET.get("field_search", "")
        current_author = self.request.user.pk
        filter_author = Q(author=current_author)
        filter_search_posts = Q(title__icontains=search_request) | Q(content__icontains=search_request)
        notes_list = Note.objects.filter(filter_author & filter_search_posts)
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



class LoginPage(LoginView):
    template_name = "main/auth_login.html"
    

class LogoutPage(LogoutView):
    template_name = "main/auth_logout.html"








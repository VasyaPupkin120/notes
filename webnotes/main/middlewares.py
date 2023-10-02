from django.shortcuts import redirect
from django.urls import reverse
from .models import Tag


def context_processor_tags(request):
    """
    Отправляет в каждый шаблон список всех тегов текущего пользователя 
    для вставки в облако тегов.
    """
    if request.user.is_authenticated:
        return {"tags_cloud": Tag.objects.filter(author=request.user.pk)}
    else:
        return {"tags_cloud": None}


def CheckAuthenticationMiddleware(next_mw):
    """
    Перенаправляет запросы от всех неаутентифицированных пользователей
    на страничку логина. Перенаправляет аутентифицированных пользователей
    вместо странички логина на главную страничку.
    """
    def core_mw(request):
        if request.user.is_authenticated:
            if request.path == "/login/":
                return redirect(reverse("index"))
            else:
                # переход к запрошенной вьюхе или следующему middleware
                response = next_mw(request)
                return response
        else:
            if (request.path == "/login/") or ("/static/" in request.path):
                # аналогично, просто выполняется вьюха аутентификации или запрос статического файла
                response = next_mw(request)
                return response
            else:
                return redirect(reverse("login"))
    return core_mw

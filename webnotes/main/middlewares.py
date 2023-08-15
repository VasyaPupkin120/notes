from .models import Tag

def context_processor_tags(request):
    if request.user.is_authenticated:
        return {"tags_cloud": Tag.objects.filter(author=request.user.pk)}
    else:
        return {"tags_cloud": None}


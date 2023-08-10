from .models import Tag

def context_processor_tags(request):
    return {"tags_cloud": Tag.objects.all()}


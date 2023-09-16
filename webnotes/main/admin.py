from django.contrib import admin
from .models import Tag, Note

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "slug",)
    list_display_links = ("name",)
    search_fields = ("name", "slug")

class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "slug", "created_at", "tags", )
    list_display_links = ("title", )
    search_fields = ("title", "slug", "created_at", "tags",)



# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Note, NoteAdmin)

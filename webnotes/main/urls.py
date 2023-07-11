from django.urls import path
from .views import *


#app_name = "main"
urlpatterns = [
        path('', index, name="index"),
        path('note_create/', NoteFormCreate.as_view(), name="note_create"),
        path("note/<str:slug>/", NoteRead.as_view(), name="note_read"),
        path('note_update/<str:slug>', NoteUpdate.as_view(), name="note_update"),
        path('note_delete/<str:slug>', NoteDelete.as_view(), name="note_delete"),
        path('tag_create/', TagFormCreate.as_view(), name="tag_create"),
        path('tag/<str:slug>/', TagItems.as_view(), name="tag_items"),
        path('tag_delete/<str:slug>', TagDelete.as_view(), name="tag_delete"),
        path('tag_update/<str:slug>', TagUpdate.as_view(), name="tag_update"),
        path('tag_list/', TagList.as_view(), name="tag_list"),
]

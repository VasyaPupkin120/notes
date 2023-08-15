from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.utils.text import slugify
from time import time

def gen_slug(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug + "-" + str(int(time()))


class Note(models.Model): 
    """
    Собственно одна заметка
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, db_index=True, blank=True, null=True, unique=True, verbose_name="Слаг заметки", )
    title = models.CharField(max_length=256, verbose_name="Заголовок заметки",)
    content = models.TextField(verbose_name="Содержание заметки",)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата, время создания",)
    tags = models.ManyToManyField("Tag", blank=True, null=True)

    def __str__(self):
        return f"note: {self.title}"

    def get_absolute_url(self):
        return reverse_lazy("note_read", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # если запись в БД есть - то слаг пересоздавать не нужно - это для случая редактирования заметки
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at',]



class Tag(models.Model):
    """
    Модель тега
    """
    def __str__(self):
        return self.name

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, db_index=True, blank=True, null=True, unique=True, verbose_name="Слаг тэга", )
    name = models.CharField(
            max_length=30,
            db_index=True,
            unique=True,
            verbose_name="Название тега",
            )

    def save(self, *args, **kwargs):
        # слаг тэга пересоздается в том числе при редактировании
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("tag_link_posts", kwargs={"slug": self.slug})

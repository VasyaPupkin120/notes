from django.db import models

# Create your models here.

class Note(models.Model): 
    """
    Собственно одна заметка
    """
    title = models.CharField(
            max_length=256,
            verbose_name="Заголовок заметки",
            )
    content = models.TextField(
            verbose_name="Содержание заметки",
            )
    created_at = models.DateTimeField(
            auto_now_add=True,
            db_index=True,
            verbose_name="Дата, время создания",
            )

class Tag(models.Model):
    """
    Модель тега
    """
    name = models.CharField(
            max_length=30,
            db_index=True,
            unique=True,
            verbose_name="Название тега",
            )
    notes = models.ManyToManyField(Note,)

# class LinkTag(models.Model):
#     """
#     Связующая модель
#     """
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     note = models.ForeignKey(Note, on_delete=models.CASCADE)
#     count = models.IntegerField()


# Generated by Django 4.2.2 on 2023-06-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_note_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Слаг заметки'),
        ),
    ]

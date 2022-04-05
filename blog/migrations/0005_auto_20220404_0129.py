# Generated by Django 3.2 on 2022-04-03 19:29

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
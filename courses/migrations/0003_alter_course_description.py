# Generated by Django 5.2.1 on 2025-05-24 11:07

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_enrolled_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=markdownx.models.MarkdownxField(),
        ),
    ]

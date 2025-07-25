# Generated by Django 5.2.1 on 2025-05-29 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_alter_quiz_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='max_attempts',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='quiz',
            name='time_limit',
            field=models.PositiveIntegerField(default=0, help_text='Time limit in minutes'),
        ),
    ]

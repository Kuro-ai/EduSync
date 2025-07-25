# Generated by Django 5.2.1 on 2025-05-27 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_remove_lesson_file_lessonfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirusTotalScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(max_length=500, unique=True)),
                ('scan_date', models.DateTimeField(auto_now=True)),
                ('scan_result', models.JSONField()),
                ('is_clean', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_scan_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('clean', 'Clean'), ('unsafe', 'Unsafe'), ('error', 'Error')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='lessonfile',
            name='file_scan_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('clean', 'Clean'), ('unsafe', 'Unsafe'), ('error', 'Error')], default='pending', max_length=10),
        ),
    ]

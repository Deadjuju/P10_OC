# Generated by Django 4.0.4 on 2022-05-31 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('description', models.CharField(max_length=2048, verbose_name='Description')),
                ('type', models.CharField(choices=[
                    ('back-end', 'Back-End'),
                    ('front-end', 'Front-End'),
                    ('ios', 'iOS'),
                    ('android', 'Android')
                ], max_length=15, verbose_name='Type')),
                ('author_user_id', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)
                 ),
            ],
        ),
    ]
# Generated by Django 4.0.4 on 2022-06-05 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributor',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='user_id',
            new_name='user',
        ),
    ]
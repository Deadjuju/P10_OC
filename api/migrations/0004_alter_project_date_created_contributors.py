# Generated by Django 4.0.4 on 2022-05-31 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_project_date_created_project_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('author', 'Author'), ('contributor', 'Contributor')], max_length=128, verbose_name='Roles')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_contributor', to='api.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

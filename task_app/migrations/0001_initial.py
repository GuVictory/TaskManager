# Generated by Django 3.1.1 on 2020-09-29 19:39

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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=32)),
                ('description', models.TextField(blank=True, max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('New', 'Новая'), ('Planned', 'Запланированная'), ('in Work', 'в Работе'), ('Compleated', 'Завершённая')], default='New', max_length=16)),
                ('finish_date', models.DateField(blank=True, default=None, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, name='creator')
    title = models.CharField(max_length=32, default='')
    description = models.TextField(max_length=256, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    NEW = 'New'
    PLANNED = 'Planned'
    IN_WORK = 'in Work'
    COMPLETED = 'Compleated'
    STATUS_CHOICES = [
        (NEW, 'Новая'),
        (PLANNED, 'Запланированная'),
        (IN_WORK, 'в Работе'),
        (COMPLETED, 'Завершённая'),
    ]
    status = models.CharField(
            max_length=16,
            choices=STATUS_CHOICES,
            default=NEW,
    )
    finish_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

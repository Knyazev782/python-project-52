from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels

class Tasks(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, verbose_name='Статус')
    author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='author_tasks', verbose_name='Автор')
    assigned_to = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='assigned_tasks', verbose_name='Исполнитель', null=True, blank=True)
    labels = models.ManyToManyField(Labels, verbose_name='Метки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
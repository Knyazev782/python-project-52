from django.db import models
from task_manager.users.models import Users

class Labels(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    created_by = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='Автор', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        ordering = ['name']
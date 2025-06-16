from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels

class Tasks(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=False)
    assigned_to = models.ForeignKey(Users, on_delete=models.PROTECT, null=False, related_name='assigned_tasks')
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, null=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='created_tasks')
    labels = models.ManyToManyField(Labels, blank=True, related_name='tasks')

    def __str__(self):
        return self.name
from django.db import models
from django.conf import settings

class Statuses(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)
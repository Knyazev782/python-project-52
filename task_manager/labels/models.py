from django.db import models

class Labels(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'users_users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
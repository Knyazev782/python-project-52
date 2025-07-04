# Generated by Django 5.2.1 on 2025-06-30 13:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0003_alter_labels_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='labels',
            options={'ordering': ['name'], 'verbose_name': 'Метка', 'verbose_name_plural': 'Метки'},
        ),
        migrations.AddField(
            model_name='labels',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]

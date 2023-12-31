# Generated by Django 3.1.2 on 2023-06-24 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20230623_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemscarrito',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='usuarios',
            field=models.ManyToManyField(through='core.ItemsCarrito', to=settings.AUTH_USER_MODEL),
        ),
    ]

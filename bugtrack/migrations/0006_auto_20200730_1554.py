# Generated by Django 3.0.8 on 2020-07-30 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrack', '0005_auto_20200730_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solver',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solverUser', to=settings.AUTH_USER_MODEL),
        ),
    ]

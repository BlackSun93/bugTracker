# Generated by Django 3.0.8 on 2020-08-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrack', '0015_bug_notiftype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='notifType',
        ),
        migrations.AddField(
            model_name='user',
            name='notifType',
            field=models.CharField(blank=True, default='none', max_length=50, null=True),
        ),
    ]

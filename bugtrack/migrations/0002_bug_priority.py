# Generated by Django 3.0.8 on 2020-07-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='priority',
            field=models.CharField(default='med', max_length=10),
            preserve_default=False,
        ),
    ]

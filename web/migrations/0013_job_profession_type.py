# Generated by Django 2.0.6 on 2018-07-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20180710_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='profession_type',
            field=models.CharField(default='General', max_length=100),
        ),
    ]

# Generated by Django 2.0.6 on 2018-07-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_event_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.CharField(default='Accra', max_length=300),
            preserve_default=False,
        ),
    ]
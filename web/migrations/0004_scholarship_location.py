# Generated by Django 2.0.6 on 2018-07-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_scholarship_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='location',
            field=models.CharField(default='ghana', max_length=100),
            preserve_default=False,
        ),
    ]
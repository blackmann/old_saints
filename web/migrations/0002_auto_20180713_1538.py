# Generated by Django 2.0.6 on 2018-07-13 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_images',
        ),
        migrations.AddField(
            model_name='project',
            name='image1',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image2',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image3',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image4',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image5',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='project',
            name='image6',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]

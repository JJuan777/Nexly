# Generated by Django 5.1 on 2024-08-28 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nexly', '0007_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner_picture',
            field=models.ImageField(blank=True, null=True, upload_to='banner_pictures/'),
        ),
    ]

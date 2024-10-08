# Generated by Django 5.1 on 2024-08-23 23:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nexly', '0003_post_shared_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='shared_post',
        ),
        migrations.AddField(
            model_name='post',
            name='original_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reposts', to='Nexly.post'),
        ),
    ]

# Generated by Django 5.1.1 on 2025-05-12 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_room_myname_alter_myprofile_room_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='myname',
        ),
    ]

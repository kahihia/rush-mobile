# Generated by Django 2.1.2 on 2019-04-08 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_auto_20190407_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='isOpen',
            new_name='is_open',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='distance',
        ),
    ]

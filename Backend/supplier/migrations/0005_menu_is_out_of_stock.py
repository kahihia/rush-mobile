# Generated by Django 2.1.2 on 2019-03-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0004_auto_20190313_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_out_of_stock',
            field=models.BooleanField(default=False),
        ),
    ]

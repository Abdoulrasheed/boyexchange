# Generated by Django 3.2.5 on 2021-07-17 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_exchangepair_pair_equivalent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='price',
        ),
    ]

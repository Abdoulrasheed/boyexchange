# Generated by Django 3.2.5 on 2021-07-17 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210717_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangepair',
            name='pair_equivalent',
            field=models.FloatField(default=10, help_text='x number of currency, gives how much of its pair ?', verbose_name='currency_rate'),
        ),
    ]
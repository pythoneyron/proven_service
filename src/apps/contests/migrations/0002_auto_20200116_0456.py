# Generated by Django 2.2.3 on 2020-01-16 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penalty',
            name='point',
            field=models.FloatField(default=0, verbose_name='Штраф'),
        ),
    ]
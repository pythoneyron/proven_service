# Generated by Django 2.2.3 on 2020-01-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_auto_20200116_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='team_images/', verbose_name='Изображение'),
        ),
    ]

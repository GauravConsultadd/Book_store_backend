# Generated by Django 5.0.1 on 2024-01-30 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_bookmodel_cover_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='cover_image_url',
            field=models.CharField(max_length=500),
        ),
    ]

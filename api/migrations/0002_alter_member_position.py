# Generated by Django 5.0.2 on 2024-10-12 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='position',
            field=models.CharField(blank=True, max_length=250, verbose_name='Должность'),
        ),
    ]

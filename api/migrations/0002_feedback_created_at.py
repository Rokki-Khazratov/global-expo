# Generated by Django 5.0.2 on 2024-10-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]

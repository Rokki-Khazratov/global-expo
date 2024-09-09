# Generated by Django 5.0.2 on 2024-09-09 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_participant_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='member',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Ф. И. О.'),
        ),
        migrations.AlterField(
            model_name='member',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='member',
            name='position',
            field=models.CharField(blank=True, max_length=150, verbose_name='Должность'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(max_length=255, unique=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='api.member')),
            ],
        ),
    ]

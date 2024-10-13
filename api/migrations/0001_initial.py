# Generated by Django 5.0.2 on 2024-10-13 14:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ф. И. О.')),
                ('expo', models.IntegerField(choices=[(1, 'Banks&Business'), (2, 'UzCharmEURASIA')], default=1)),
                ('company', models.CharField(blank=True, max_length=200, null=True, verbose_name='Компания')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон')),
                ('position', models.CharField(blank=True, max_length=250, verbose_name='Должность')),
                ('role', models.IntegerField(choices=[(1, 'VIP'), (2, 'Exhibitor'), (3, 'Visitor'), (4, 'Not gived')], default=4)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/members/')),
                ('registration_time', models.TimeField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_body', models.TextField(blank=True, null=True)),
                ('stars', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bank')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='api.member')),
            ],
        ),
    ]

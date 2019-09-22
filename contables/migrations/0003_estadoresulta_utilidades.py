# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-19 02:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contables', '0002_estadoresulta'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadoresulta',
            name='utilidades',
            field=models.DecimalField(decimal_places=2, max_digits=50, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Utilildad'),
        ),
    ]

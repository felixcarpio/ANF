# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-20 04:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contables', '0017_auto_20171130_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadocomprobacion',
            name='id_periodoContable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contables.PeriodoContable'),
        ),
    ]

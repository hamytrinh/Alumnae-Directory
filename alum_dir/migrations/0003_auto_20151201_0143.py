# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alum_dir', '0002_auto_20151201_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='school',
        ),
        migrations.RemoveField(
            model_name='question',
            name='year',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alum_dir', '0007_auto_20151201_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alum',
            name='pub_date',
        ),
    ]

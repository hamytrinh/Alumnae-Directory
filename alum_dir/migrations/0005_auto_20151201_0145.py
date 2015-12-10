# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alum_dir', '0004_auto_20151201_0143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='email',
        ),
    ]

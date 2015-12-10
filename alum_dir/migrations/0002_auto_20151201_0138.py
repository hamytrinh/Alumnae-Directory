# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alum_dir', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='email',
        ),
        migrations.AddField(
            model_name='question',
            name='first_name',
            field=models.CharField(default='name', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='last_name',
            field=models.CharField(default='name', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='school',
            field=models.CharField(default='school', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='year',
            field=models.CharField(default='0000', max_length=200),
            preserve_default=False,
        ),
    ]

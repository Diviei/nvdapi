# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0002_auto_20150308_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productversion',
            name='version',
            field=models.CharField(max_length=25, blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='version',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]

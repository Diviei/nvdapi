# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerability',
            name='cvss',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]

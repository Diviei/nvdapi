# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0010_vulnerability_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerability',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]

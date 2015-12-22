# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0007_auto_20150315_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='vulnerability',
            name='modified_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='released_on',
            field=models.DateTimeField(),
        ),
    ]

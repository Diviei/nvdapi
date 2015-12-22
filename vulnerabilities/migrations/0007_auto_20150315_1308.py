# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0006_auto_20150315_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerabilitysource',
            name='url',
            field=models.URLField(max_length=500),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0004_auto_20150308_1826'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vulnerabilitysource',
            unique_together=set([('vulnerability', 'url')]),
        ),
    ]

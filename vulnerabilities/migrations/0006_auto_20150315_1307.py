# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0005_auto_20150308_2120'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vulnerabilitysource',
            unique_together=set([]),
        ),
    ]

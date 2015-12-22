# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0008_auto_20151207_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vulnerability',
            name='cvss',
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='access_complexity',
            field=models.CharField(default=b'MEDIUM', max_length=20),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='access_vector',
            field=models.CharField(default=b'NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='authentication',
            field=models.CharField(default=b'NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='availability_impact',
            field=models.CharField(default=b'NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='confidentiality_impact',
            field=models.CharField(default=b'NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='integrity_impact',
            field=models.CharField(default=b'NONE', max_length=20),
        ),
    ]

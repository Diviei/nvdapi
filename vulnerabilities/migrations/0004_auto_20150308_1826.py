# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vulnerabilities', '0003_auto_20150308_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productversion',
            name='version',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='cvss',
            field=models.CharField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='released_on',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]

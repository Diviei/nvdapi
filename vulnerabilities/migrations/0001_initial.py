# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1)),
                ('vendor', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=50, blank=True)),
                ('cpe', models.CharField(unique=True, max_length=255)),
                ('product', models.ForeignKey(to='vulnerabilities.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cve', models.CharField(unique=True, max_length=50)),
                ('released_on', models.DateTimeField()),
                ('modified_on', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField()),
                ('access_complexity', models.CharField(default=b'MEDIUM', max_length=20, null=True)),
                ('authentication', models.CharField(default=b'NONE', max_length=20, null=True)),
                ('confidentiality_impact', models.CharField(default=b'NONE', max_length=20, null=True)),
                ('integrity_impact', models.CharField(default=b'NONE', max_length=20, null=True)),
                ('availability_impact', models.CharField(default=b'NONE', max_length=20, null=True)),
                ('access_vector', models.CharField(default=b'NONE', max_length=20, null=True)),
                ('score', models.FloatField(default=0)),
                ('product_version', models.ManyToManyField(to='vulnerabilities.ProductVersion')),
            ],
        ),
        migrations.CreateModel(
            name='VulnerabilitySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=500)),
                ('vulnerability', models.ForeignKey(to='vulnerabilities.Vulnerability')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('vendor', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='productversion',
            unique_together=set([('product', 'version')]),
        ),
    ]

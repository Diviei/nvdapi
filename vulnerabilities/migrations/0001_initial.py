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
                ('vendor', models.CharField(max_length=50)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=25)),
                ('product', models.ForeignKey(to='vulnerabilities.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cve', models.CharField(unique=True, max_length=50)),
                ('released_on', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('cvss', models.CharField(max_length=20, blank=True)),
                ('product_version', models.ManyToManyField(to='vulnerabilities.ProductVersion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VulnerabilitySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('vulnerability', models.ForeignKey(to='vulnerabilities.Vulnerability')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productversion',
            unique_together=set([('product', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('vendor', 'name')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coercion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Data',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('identifier', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('coercion', models.ForeignKey(related_name='datatypes', to='igecas.Coercion')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('identifier', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.CharField(max_length=32, unique=True)),
                ('origin', models.ForeignKey(related_name='prototypes', to='igecas.Origin')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('reference', models.CharField(max_length=128)),
                ('datatype', models.ManyToManyField(related_name='references', to='igecas.DataType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferenceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(blank=True, null=True, editable=False)),
                ('value', models.CharField(max_length=64)),
                ('confidence', models.DecimalField(max_digits=5, null=True, decimal_places=2)),
                ('prevalence', models.DecimalField(max_digits=5, null=True, decimal_places=2)),
                ('datatype', models.ForeignKey(related_name='typevalues', to='igecas.DataType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reference',
            name='reference_type',
            field=models.ForeignKey(related_name='references', to='igecas.ReferenceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datatype',
            name='prototype',
            field=models.ForeignKey(related_name='datatypes', to='igecas.Prototype'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='data',
            name='datatype',
            field=models.ForeignKey(related_name='data', to='igecas.DataType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='data',
            name='person',
            field=models.ForeignKey(related_name='data', to='igecas.Person'),
            preserve_default=True,
        ),
    ]

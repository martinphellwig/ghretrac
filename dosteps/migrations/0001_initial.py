# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dosteps.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', dosteps.models.Name(unique=True, max_length=16)),
                ('description', dosteps.models.Description(null=True, blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeWorkflow',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, editable=False, blank=True)),
                ('attribute', models.ForeignKey(to='dosteps.Attribute')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', dosteps.models.Name(unique=True, max_length=16)),
                ('description', dosteps.models.Description(null=True, blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NamedAttributeWorkflow',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', dosteps.models.Name(unique=True, max_length=16)),
                ('description', dosteps.models.Description(null=True, blank=True, max_length=128)),
                ('attribute_workflow_entries', models.ManyToManyField(to='dosteps.AttributeWorkflow')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', dosteps.models.Name(unique=True, max_length=16)),
                ('description', dosteps.models.Description(null=True, blank=True, max_length=128)),
                ('parent', models.ForeignKey(to='dosteps.Workflow')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workflow',
            unique_together=set([('parent', 'name')]),
        ),
        migrations.AddField(
            model_name='item',
            name='identifier',
            field=models.ForeignKey(to='dosteps.NamedAttributeWorkflow'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(to='dosteps.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='workflow',
            field=models.ForeignKey(to='dosteps.Workflow'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributeworkflow',
            name='workflow',
            field=models.ForeignKey(to='dosteps.Workflow'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attributeworkflow',
            unique_together=set([('attribute', 'workflow')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=128, null=True, blank=True, help_text='If name is given use that over UName.')),
                ('line_1', models.CharField(max_length=40)),
                ('line_2', models.CharField(max_length=40, null=True, blank=True)),
                ('line_3', models.CharField(max_length=40, null=True, blank=True)),
                ('line_4', models.CharField(max_length=40, null=True, blank=True)),
                ('line_5', models.CharField(max_length=40, null=True, blank=True)),
                ('code', models.CharField(max_length=16, null=True, blank=True)),
                ('city', models.CharField(max_length=64)),
                ('region', models.CharField(max_length=64, null=True, blank=True)),
                ('country', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'ContactCategory',
                'verbose_name_plural': 'ContactCategories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
                ('regex', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'ContactType',
                'verbose_name_plural': 'ContactTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IdentityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
                ('regex', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'IdentityType',
                'verbose_name_plural': 'IdentityTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'RelationType',
                'verbose_name_plural': 'RelationTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('address', models.ForeignKey(to='inacar.Address')),
            ],
            options={
                'verbose_name': 'uAddress',
                'verbose_name_plural': 'uAddresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('category', models.ForeignKey(to='inacar.ContactCategory')),
                ('contact', models.ForeignKey(to='inacar.Contact')),
            ],
            options={
                'verbose_name': 'uContact',
                'verbose_name_plural': 'uContacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UIdentities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('value', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'UIdentity',
                'verbose_name_plural': 'UIdentities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('first', models.CharField(max_length=32, help_text='Given name of person')),
                ('go_by', models.CharField(max_length=32, null=True, blank=True, help_text='The name the person goes by')),
                ('middle', models.TextField(null=True, blank=True, help_text='All middle names')),
                ('prefix', models.CharField(max_length=16, null=True, blank=True, help_text='Prefix to the family name')),
                ('family', models.TextField(help_text='The surname')),
                ('affix', models.CharField(max_length=16, null=True, blank=True, help_text='Affix to the family name')),
                ('official', models.TextField(help_text='The official names, including titles')),
            ],
            options={
                'verbose_name': 'uName',
                'verbose_name_plural': 'uNames',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='URelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('relation', models.ForeignKey(to='inacar.RelationType')),
            ],
            options={
                'verbose_name': 'uRelation',
                'verbose_name_plural': 'uRelations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UUID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dts_insert', models.DateTimeField(auto_now_add=True)),
                ('dts_update', models.DateTimeField(auto_now=True)),
                ('dts_delete', models.DateTimeField(null=True, blank=True, editable=False)),
                ('uuid', models.CharField(max_length=36, unique=True, editable=False, null=True, help_text='UUID RFC4122 compliant (uuid5)')),
                ('poid', models.CharField(max_length=90, editable=False, default='1.3.6.1.4.1.44797.1.1.22804077943924435831475450687692183245429423284210119033077979070886', help_text='The parents OID')),
            ],
            options={
                'verbose_name': 'UUID',
                'verbose_name_plural': 'UUIDs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='urelation',
            name='uuid_one',
            field=models.ForeignKey(related_name='uuid_one', to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='urelation',
            name='uuid_two',
            field=models.ForeignKey(related_name='uuid_two', to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uname',
            name='uuid',
            field=models.ForeignKey(to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uidentities',
            name='uuid',
            field=models.ForeignKey(to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uidentities',
            name='value_type',
            field=models.ForeignKey(to='inacar.IdentityType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ucontact',
            name='uuid',
            field=models.ForeignKey(to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uaddress',
            name='uuid',
            field=models.ForeignKey(to='inacar.UUID', to_field='uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='value_type',
            field=models.ForeignKey(to='inacar.ContactType'),
            preserve_default=True,
        ),
    ]

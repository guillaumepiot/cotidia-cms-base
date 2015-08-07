# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cmsbase.models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('home', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False, verbose_name='Active')),
                ('approval_needed', models.BooleanField(default=False)),
                ('template', models.CharField(default='cms/page.html', max_length=250)),
                ('display_title', models.CharField(verbose_name='Display title', max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=60, verbose_name='Unique Page Identifier', null=True)),
                ('order_id', models.IntegerField(default=0)),
                ('publish', models.BooleanField(default=False, verbose_name='Publish this page. The page will also be set to Active.')),
                ('approve', models.BooleanField(default=False, verbose_name='Submit for approval')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('redirect_to_url', models.URLField(blank=True, verbose_name='Redirect to URL', help_text='Redirect this page to a given URL')),
                ('target', models.CharField(default='_self', verbose_name='Open page in', choices=[('_self', 'the same window'), ('_blank', 'a new window')], max_length=50)),
                ('hide_from_nav', models.BooleanField(default=False, verbose_name='Hide from navigation')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'permissions': (('can_publish', 'Can publish'),),
                'verbose_name_plural': 'Pages',
                'verbose_name': 'Page',
            },
        ),
        migrations.CreateModel(
            name='PageDataSet',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('config', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Page data sets',
                'verbose_name': 'Page data set',
            },
        ),
        migrations.CreateModel(
            name='PageDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, verbose_name='Name', max_length=250)),
                ('document', models.FileField(upload_to=cmsbase.models.call_document_naming)),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(to='cmsbase.Page')),
            ],
            options={
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
                'ordering': ('order_id',),
            },
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('link_name', models.CharField(blank=True, verbose_name='Link to (name)', help_text='Eg: Click here for more info', max_length=250)),
                ('url', models.URLField(blank=True, verbose_name='Link to (URL)', help_text='Eg: http://example.com/info', max_length=250)),
                ('description', models.TextField(blank=True, verbose_name='Description', max_length=250)),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(to='cmsbase.Page')),
            ],
            options={
                'verbose_name_plural': 'Links',
                'verbose_name': 'Link',
                'ordering': ('order_id', 'link_name'),
            },
        ),
        migrations.CreateModel(
            name='PageTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Page title', max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('language_code', models.CharField(verbose_name='language', choices=[('en', 'English')], max_length=7)),
                ('content', models.TextField(blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='cmsbase.Page')),
            ],
            options={
                'verbose_name_plural': 'Content',
                'verbose_name': 'Content',
                'abstract': False,
            },
            bases=(models.Model, cmsbase.models.PublishTranslation),
        ),
        migrations.AddField(
            model_name='page',
            name='dataset',
            field=models.ForeignKey(blank=True, null=True, to='cmsbase.PageDataSet'),
        ),
        migrations.AddField(
            model_name='page',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, to='cmsbase.Page', related_name='children'),
        ),
        migrations.AddField(
            model_name='page',
            name='published_from',
            field=models.ForeignKey(blank=True, null=True, to='cmsbase.Page'),
        ),
        migrations.AddField(
            model_name='page',
            name='redirect_to',
            field=models.ForeignKey(blank=True, null=True, to='cmsbase.Page', related_name='redirect_to_page'),
        ),
        migrations.AddField(
            model_name='page',
            name='related_pages',
            field=models.ManyToManyField(blank=True, to='cmsbase.Page', related_name='related_pages_rel_+'),
        ),
        migrations.AlterUniqueTogether(
            name='pagetranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
    ]

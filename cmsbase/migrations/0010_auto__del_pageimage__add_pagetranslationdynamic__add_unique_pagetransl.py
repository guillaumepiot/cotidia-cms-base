# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PageImage'
        db.delete_table(u'cmsbase_pageimage')

        # Adding model 'PageTranslationDynamic'
        db.create_table(u'cmsbase_pagetranslationdynamic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations_dynamic', to=orm['cmsbase.PageDynamic'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'cmsbase', ['PageTranslationDynamic'])

        # Adding unique constraint on 'PageTranslationDynamic', fields ['parent', 'language_code']
        db.create_unique(u'cmsbase_pagetranslationdynamic', ['parent_id', 'language_code'])

        # Adding model 'PageMask'
        db.create_table(u'cmsbase_pagemask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('config', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cmsbase', ['PageMask'])

        # Adding model 'PageDynamic'
        db.create_table(u'cmsbase_pagedynamic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approval_needed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template', self.gf('django.db.models.fields.CharField')(default='cms/page.html', max_length=250)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['cmsbase.PageDynamic'])),
            ('published_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsbase.PageDynamic'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=60, null=True, blank=True)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='redirect_to_page', null=True, to=orm['cmsbase.PageDynamic'])),
            ('redirect_to_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(default='_self', max_length=50)),
            ('hide_from_nav', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'cmsbase', ['PageDynamic'])

        # Adding M2M table for field related_pages on 'PageDynamic'
        m2m_table_name = db.shorten_name(u'cmsbase_pagedynamic_related_pages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_pagedynamic', models.ForeignKey(orm[u'cmsbase.pagedynamic'], null=False)),
            ('to_pagedynamic', models.ForeignKey(orm[u'cmsbase.pagedynamic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_pagedynamic_id', 'to_pagedynamic_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageTranslationDynamic', fields ['parent', 'language_code']
        db.delete_unique(u'cmsbase_pagetranslationdynamic', ['parent_id', 'language_code'])

        # Adding model 'PageImage'
        db.create_table(u'cmsbase_pageimage', (
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsbase.Page'])),
            ('order_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cmsbase', ['PageImage'])

        # Deleting model 'PageTranslationDynamic'
        db.delete_table(u'cmsbase_pagetranslationdynamic')

        # Deleting model 'PageMask'
        db.delete_table(u'cmsbase_pagemask')

        # Deleting model 'PageDynamic'
        db.delete_table(u'cmsbase_pagedynamic')

        # Removing M2M table for field related_pages on 'PageDynamic'
        db.delete_table(db.shorten_name(u'cmsbase_pagedynamic_related_pages'))


    models = {
        u'cmsbase.page': {
            'Meta': {'object_name': 'Page'},
            'approval_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'hide_from_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cmsbase.Page']"}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']", 'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirect_to_page'", 'null': 'True', 'to': u"orm['cmsbase.Page']"}),
            'redirect_to_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'related_pages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_pages_rel_+'", 'blank': 'True', 'to': u"orm['cmsbase.Page']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'default': "'_self'", 'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'cms/page.html'", 'max_length': '250'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cmsbase.pagedocument': {
            'Meta': {'ordering': "('order_id',)", 'object_name': 'PageDocument'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']"})
        },
        u'cmsbase.pagedynamic': {
            'Meta': {'object_name': 'PageDynamic'},
            'approval_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'hide_from_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cmsbase.PageDynamic']"}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.PageDynamic']", 'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirect_to_page'", 'null': 'True', 'to': u"orm['cmsbase.PageDynamic']"}),
            'redirect_to_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'related_pages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_pages_rel_+'", 'blank': 'True', 'to': u"orm['cmsbase.PageDynamic']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'default': "'_self'", 'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'cms/page.html'", 'max_length': '250'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cmsbase.pagelink': {
            'Meta': {'ordering': "('order_id', 'link_name')", 'object_name': 'PageLink'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'cmsbase.pagemask': {
            'Meta': {'object_name': 'PageMask'},
            'config': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cmsbase.pagetranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'PageTranslation'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['cmsbase.Page']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cmsbase.pagetranslationdynamic': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'PageTranslationDynamic'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations_dynamic'", 'to': u"orm['cmsbase.PageDynamic']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cmsbase']
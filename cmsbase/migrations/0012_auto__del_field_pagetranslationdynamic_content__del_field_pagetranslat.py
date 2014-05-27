# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PageTranslationDynamic.content'
        db.delete_column(u'cmsbase_pagetranslationdynamic', 'content')

        # Deleting field 'PageTranslationDynamic.meta_description'
        db.delete_column(u'cmsbase_pagetranslationdynamic', 'meta_description')

        # Deleting field 'PageTranslationDynamic.meta_title'
        db.delete_column(u'cmsbase_pagetranslationdynamic', 'meta_title')

        # Deleting field 'PageTranslationDynamic.title'
        db.delete_column(u'cmsbase_pagetranslationdynamic', 'title')

        # Deleting field 'PageTranslationDynamic.slug'
        db.delete_column(u'cmsbase_pagetranslationdynamic', 'slug')


    def backwards(self, orm):
        # Adding field 'PageTranslationDynamic.content'
        db.add_column(u'cmsbase_pagetranslationdynamic', 'content',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'PageTranslationDynamic.meta_description'
        db.add_column(u'cmsbase_pagetranslationdynamic', 'meta_description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'PageTranslationDynamic.meta_title'
        db.add_column(u'cmsbase_pagetranslationdynamic', 'meta_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'PageTranslationDynamic.title'
        db.add_column(u'cmsbase_pagetranslationdynamic', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'PageTranslationDynamic.slug'
        db.add_column(u'cmsbase_pagetranslationdynamic', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=100),
                      keep_default=False)


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
            'mask': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.PageMask']", 'null': 'True', 'blank': 'True'}),
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
            'mask': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.PageMask']", 'null': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations_dynamic'", 'to': u"orm['cmsbase.PageDynamic']"})
        }
    }

    complete_apps = ['cmsbase']
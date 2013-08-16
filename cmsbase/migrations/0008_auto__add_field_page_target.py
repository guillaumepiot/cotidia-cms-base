# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.target'
        db.add_column(u'cmsbase_page', 'target',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Page.target'
        db.delete_column(u'cmsbase_page', 'target')


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
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cmsbase.Page']"}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']", 'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirect_to_page'", 'null': 'True', 'to': u"orm['cmsbase.Page']"}),
            'redirect_to_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'related_pages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_pages_rel_+'", 'blank': 'True', 'to': u"orm['cmsbase.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'cms/page.html'", 'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cmsbase.pagedocument': {
            'Meta': {'ordering': "('order_id',)", 'object_name': 'PageDocument'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']"})
        },
        u'cmsbase.pageimage': {
            'Meta': {'ordering': "('order_id',)", 'object_name': 'PageImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.Page']"})
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
        u'cmsbase.pagetranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'PageTranslation'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['cmsbase.Page']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cmsbase']
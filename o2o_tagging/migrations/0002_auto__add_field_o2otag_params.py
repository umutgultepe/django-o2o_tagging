# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'O2OTag.params'
        db.add_column('o2o_tagging_o2otag', 'params',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'O2OTag.params'
        db.delete_column('o2o_tagging_o2otag', 'params')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'o2o_tagging.o2otag': {
            'Meta': {'unique_together': "(('tagger_content_type', 'tagger_object_id', 'tagged_content_type', 'tagged_object_id', 'tagged_in_content_type', 'tagged_in_object_id'),)", 'object_name': 'O2OTag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'params': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'tagged_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggeds'", 'to': "orm['contenttypes.ContentType']"}),
            'tagged_in_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['contenttypes.ContentType']"}),
            'tagged_in_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tagged_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tagger_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggers'", 'to': "orm['contenttypes.ContentType']"}),
            'tagger_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['o2o_tagging']
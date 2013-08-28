# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'O2OTag'
        db.create_table('o2o_tagging_o2otag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tagger_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taggers', to=orm['contenttypes.ContentType'])),
            ('tagger_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tagged_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taggeds', to=orm['contenttypes.ContentType'])),
            ('tagged_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tagged_in_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['contenttypes.ContentType'])),
            ('tagged_in_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('o2o_tagging', ['O2OTag'])

        # Adding unique constraint on 'O2OTag', fields ['tagger_content_type', 'tagger_object_id', 'tagged_content_type', 'tagged_object_id', 'tagged_in_content_type', 'tagged_in_object_id']
        db.create_unique('o2o_tagging_o2otag', ['tagger_content_type_id', 'tagger_object_id', 'tagged_content_type_id', 'tagged_object_id', 'tagged_in_content_type_id', 'tagged_in_object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'O2OTag', fields ['tagger_content_type', 'tagger_object_id', 'tagged_content_type', 'tagged_object_id', 'tagged_in_content_type', 'tagged_in_object_id']
        db.delete_unique('o2o_tagging_o2otag', ['tagger_content_type_id', 'tagger_object_id', 'tagged_content_type_id', 'tagged_object_id', 'tagged_in_content_type_id', 'tagged_in_object_id'])

        # Deleting model 'O2OTag'
        db.delete_table('o2o_tagging_o2otag')


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
            'tagged_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggeds'", 'to': "orm['contenttypes.ContentType']"}),
            'tagged_in_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['contenttypes.ContentType']"}),
            'tagged_in_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tagged_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tagger_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggers'", 'to': "orm['contenttypes.ContentType']"}),
            'tagger_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['o2o_tagging']
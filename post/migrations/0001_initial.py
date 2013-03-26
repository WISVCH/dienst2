# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('post_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('grouping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('counting', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('post', ['Category'])

        # Adding model 'Source'
        db.create_table('post_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('post', ['Source'])

        # Adding model 'Item'
        db.create_table('post_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['post.Source'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['post.Source'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post.Category'])),
        ))
        db.send_create_signal('post', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('post_category')

        # Deleting model 'Source'
        db.delete_table('post_source')

        # Deleting model 'Item'
        db.delete_table('post_item')


    models = {
        'post.category': {
            'Meta': {'object_name': 'Category'},
            'counting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grouping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'post.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post.Category']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': "orm['post.Source']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['post.Source']"})
        },
        'post.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['post']

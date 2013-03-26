# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table('kas_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('method', self.gf('django.db.models.fields.CharField')(default='C', max_length=1)),
        ))
        db.send_create_signal('kas', ['Transaction'])

        # Adding model 'Closure'
        db.create_table('kas_closure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('num_e500', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e200', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e100', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e50', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e20', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e10', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e5', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e050', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e020', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e010', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_e005', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('pin', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('transactions_pin', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('transactions_cash', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('kas', ['Closure'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table('kas_transaction')

        # Deleting model 'Closure'
        db.delete_table('kas_closure')


    models = {
        'kas.closure': {
            'Meta': {'ordering': "['date']", 'object_name': 'Closure'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_e005': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e010': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e020': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e050': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e10': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e100': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e20': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e200': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e5': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e50': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_e500': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pin': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'total': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'transactions_cash': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'transactions_pin': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'kas.transaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['kas']
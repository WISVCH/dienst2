# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Person.legacy_ID'
        db.delete_column('ldb_person', 'legacy_ID')


    def backwards(self, orm):
        # Adding field 'Person.legacy_ID'
        db.add_column('ldb_person', 'legacy_ID',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    models = {
        'ldb.alumnus': {
            'Meta': {'object_name': 'Alumnus'},
            'contact_method': ('django.db.models.fields.CharField', [], {'default': "'e'", 'max_length': '1'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'study_first_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'study_last_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'study_paper': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'study_professor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'study_research_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'work_company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'work_position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'work_sector': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'ldb.committee': {
            'Meta': {'object_name': 'Committee'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ldb.Person']", 'through': "orm['ldb.CommitteeMembership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ldb.committeemembership': {
            'Meta': {'object_name': 'CommitteeMembership'},
            'board': ('django.db.models.fields.IntegerField', [], {}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ldb.Committee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ldb.Person']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ras_months': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ldb.employee': {
            'Meta': {'object_name': 'Employee'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'faculty': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone_internal': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'ldb.entity': {
            'Meta': {'object_name': 'Entity'},
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'address_3': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'board_invites': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'christmas_card': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'constitution_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('ldb.country_field.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machazine': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_fixed': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'yearbook': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ldb.member': {
            'Meta': {'object_name': 'Member'},
            'amount_paid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'associate_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_paid': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'donating_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'honorary_date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'merit_date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'merit_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'merit_invitations': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ldb.modification': {
            'Meta': {'object_name': 'Modification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'modification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ldb.Person']"})
        },
        'ldb.organization': {
            'Meta': {'object_name': 'Organization', '_ormbases': ['ldb.Entity']},
            'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_short': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'salutation': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ldb.person': {
            'Meta': {'object_name': 'Person', '_ormbases': ['ldb.Entity']},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'ldap_username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'linkedin_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'living_with': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'mail_announcements': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mail_company': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'postfix_titles': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'preposition': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'ldb.student': {
            'Meta': {'object_name': 'Student'},
            'date_verified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'graduated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone_parents': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'student_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'yearbook_permission': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['ldb']
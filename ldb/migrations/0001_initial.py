# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Entity'
        db.create_table('ldb_entity', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone_fixed', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('board_invites', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('christmas_card', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
            ('country', self.gf('ldb.country_field.CountryField')(default='NL', max_length=2, blank=True)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('constitution_card', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('machazine', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('yearbook', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ldb', ['Entity'])

        # Adding model 'Organization'
        db.create_table('ldb_organization', (
            ('entity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Entity'], unique=True, primary_key=True)),
            ('name_short', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('salutation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_prefix', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('ldb', ['Organization'])

        # Adding model 'Person'
        db.create_table('ldb_person', (
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('living_with', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Person'], unique=True, null=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('mail_announcements', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('postfix_titles', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ldap_username', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('preposition', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('titles', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('phone_mobile', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('legacy_ID', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mail_company', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('entity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Entity'], unique=True, primary_key=True)),
            ('deceased', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('ldb', ['Person'])

        # Adding model 'Member'
        db.create_table('ldb_member', (
            ('donating_member', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('date_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('merit_date_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_paid', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Person'], unique=True, primary_key=True)),
            ('honorary_date_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('merit_history', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('merit_invitations', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('amount_paid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('associate_member', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('ldb', ['Member'])

        # Adding model 'Student'
        db.create_table('ldb_student', (
            ('phone_parents', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('first_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('study', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Person'], unique=True, primary_key=True)),
            ('yearbook_permission', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('graduated', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('student_number', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
        ))
        db.send_create_signal('ldb', ['Student'])

        # Adding model 'Alumnus'
        db.create_table('ldb_alumnus', (
            ('study_paper', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('study_last_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('study_research_group', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('study', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('work_sector', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('study_first_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Person'], unique=True, primary_key=True)),
            ('study_professor', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('work_company', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('work_position', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('contact_method', self.gf('django.db.models.fields.CharField')(default='e', max_length=1)),
        ))
        db.send_create_signal('ldb', ['Alumnus'])

        # Adding model 'Employee'
        db.create_table('ldb_employee', (
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ldb.Person'], unique=True, primary_key=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_internal', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('faculty', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ldb', ['Employee'])

        # Adding model 'Committee'
        db.create_table('ldb_committee', (
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ldb', ['Committee'])

        # Adding model 'CommitteeMembership'
        db.create_table('ldb_committeemembership', (
            ('ras_months', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ldb.Person'])),
            ('board', self.gf('django.db.models.fields.IntegerField')()),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ldb.Committee'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ldb', ['CommitteeMembership'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entity'
        db.delete_table('ldb_entity')

        # Deleting model 'Organization'
        db.delete_table('ldb_organization')

        # Deleting model 'Person'
        db.delete_table('ldb_person')

        # Deleting model 'Member'
        db.delete_table('ldb_member')

        # Deleting model 'Student'
        db.delete_table('ldb_student')

        # Deleting model 'Alumnus'
        db.delete_table('ldb_alumnus')

        # Deleting model 'Employee'
        db.delete_table('ldb_employee')

        # Deleting model 'Committee'
        db.delete_table('ldb_committee')

        # Deleting model 'CommitteeMembership'
        db.delete_table('ldb_committeemembership')
    
    
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
            'board_invites': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'christmas_card': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'constitution_card': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'country': ('ldb.country_field.CountryField', [], {'default': "'NL'", 'max_length': '2', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machazine': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'phone_fixed': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'yearbook': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'ldb.member': {
            'Meta': {'object_name': 'Member'},
            'amount_paid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'associate_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_paid': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'donating_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'honorary_date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'merit_date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'merit_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'merit_invitations': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'})
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
            'deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'ldap_username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'legacy_ID': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'living_with': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'mail_announcements': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'mail_company': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'postfix_titles': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'preposition': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'ldb.student': {
            'Meta': {'object_name': 'Student'},
            'first_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'graduated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ldb.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone_parents': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'student_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'yearbook_permission': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['ldb']

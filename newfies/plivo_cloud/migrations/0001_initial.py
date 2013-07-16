# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlivoSubAccount'
        db.create_table(u'plivo_cloud_plivosubaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('auth_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('auth_token', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'plivo_cloud', ['PlivoSubAccount'])


    def backwards(self, orm):
        # Deleting model 'PlivoSubAccount'
        db.delete_table(u'plivo_cloud_plivosubaccount')


    models = {
        u'plivo_cloud.plivosubaccount': {
            'Meta': {'object_name': 'PlivoSubAccount'},
            'auth_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'auth_token': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['plivo_cloud']
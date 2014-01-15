# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FilerType'
        db.create_table(u'tx_tecreports_filertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['FilerType'])

        # Adding model 'Filer'
        db.create_table(u'tx_tecreports_filer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filer_id', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('filer_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filers', to=orm['tx_tecreports.FilerType'])),
            ('last_name', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('first_name', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('name_prefix', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('name_suffix', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('nickname', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'tx_tecreports', ['Filer'])

        # Adding model 'FilingType'
        db.create_table(u'tx_tecreports_filingtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['FilingType'])

        # Adding model 'Employer'
        db.create_table(u'tx_tecreports_employer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['Employer'])

        # Adding model 'Travel'
        db.create_table(u'tx_tecreports_travel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('first_name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('title', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('suffix', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('means_of', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('departure_location', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('departure_date', self.gf('django.db.models.fields.DateField')()),
            ('distination', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('arrival_date', self.gf('django.db.models.fields.DateField')()),
            ('purpose', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['Travel'])

        # Adding model 'Report'
        db.create_table(u'tx_tecreports_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('report_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('is_original', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('through_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'tx_tecreports', ['Report'])

        # Adding model 'ContributorType'
        db.create_table(u'tx_tecreports_contributortype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['ContributorType'])

        # Adding model 'Contributor'
        db.create_table(u'tx_tecreports_contributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contributors', to=orm['tx_tecreports.ContributorType'])),
            ('is_individual', self.gf('django.db.models.fields.BooleanField')()),
            ('is_entity', self.gf('django.db.models.fields.BooleanField')()),
            ('last_name', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('first_name', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('title', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('suffix', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('address_1', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('address_2', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('city', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('state', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
            ('zipcode', self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'tx_tecreports', ['Contributor'])

        # Adding model 'Receipt'
        db.create_table(u'tx_tecreports_receipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receipts', to=orm['tx_tecreports.Report'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['tx_tecreports.Receipt'])),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receipts', to=orm['tx_tecreports.Contributor'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tx_tecreports.Employer'], null=True, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('travel', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='receipt', unique=True, null=True, to=orm['tx_tecreports.Travel'])),
            ('name_of_schedule', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('receipt_id', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('is_out_of_state_pac', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fec_id', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'tx_tecreports', ['Receipt'])

        # Adding model 'ContributionsByAmount'
        db.create_table(u'tx_tecreports_contributionsbyamount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('tx_tecreports.fields.MaxCharField')(max_length=250)),
            ('low', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('high', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats_by_amount', to=orm['tx_tecreports.Report'])),
        ))
        db.send_create_signal(u'tx_tecreports', ['ContributionsByAmount'])

        # Adding model 'ContributionsByDate'
        db.create_table(u'tx_tecreports_contributionsbydate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats_by_date', to=orm['tx_tecreports.Report'])),
        ))
        db.send_create_signal(u'tx_tecreports', ['ContributionsByDate'])

        # Adding model 'ContributionsByState'
        db.create_table(u'tx_tecreports_contributionsbystate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats_by_state', to=orm['tx_tecreports.Report'])),
        ))
        db.send_create_signal(u'tx_tecreports', ['ContributionsByState'])

        # Adding model 'ContributionsByZipcode'
        db.create_table(u'tx_tecreports_contributionsbyzipcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats_by_zipcode', to=orm['tx_tecreports.Report'])),
        ))
        db.send_create_signal(u'tx_tecreports', ['ContributionsByZipcode'])

        # Adding model 'FilingMethod'
        db.create_table(u'tx_tecreports_filingmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'tx_tecreports', ['FilingMethod'])

        # Adding model 'Filing'
        db.create_table(u'tx_tecreports_filing', (
            ('report_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, primary_key=True)),
            ('filer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filings', to=orm['tx_tecreports.Filer'])),
            ('is_correction', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('report_type', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('report_due', self.gf('django.db.models.fields.DateField')()),
            ('report_filed', self.gf('django.db.models.fields.DateField')()),
            ('filing_method', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filings', to=orm['tx_tecreports.FilingMethod'])),
        ))
        db.send_create_signal(u'tx_tecreports', ['Filing'])


    def backwards(self, orm):
        # Deleting model 'FilerType'
        db.delete_table(u'tx_tecreports_filertype')

        # Deleting model 'Filer'
        db.delete_table(u'tx_tecreports_filer')

        # Deleting model 'FilingType'
        db.delete_table(u'tx_tecreports_filingtype')

        # Deleting model 'Employer'
        db.delete_table(u'tx_tecreports_employer')

        # Deleting model 'Travel'
        db.delete_table(u'tx_tecreports_travel')

        # Deleting model 'Report'
        db.delete_table(u'tx_tecreports_report')

        # Deleting model 'ContributorType'
        db.delete_table(u'tx_tecreports_contributortype')

        # Deleting model 'Contributor'
        db.delete_table(u'tx_tecreports_contributor')

        # Deleting model 'Receipt'
        db.delete_table(u'tx_tecreports_receipt')

        # Deleting model 'ContributionsByAmount'
        db.delete_table(u'tx_tecreports_contributionsbyamount')

        # Deleting model 'ContributionsByDate'
        db.delete_table(u'tx_tecreports_contributionsbydate')

        # Deleting model 'ContributionsByState'
        db.delete_table(u'tx_tecreports_contributionsbystate')

        # Deleting model 'ContributionsByZipcode'
        db.delete_table(u'tx_tecreports_contributionsbyzipcode')

        # Deleting model 'FilingMethod'
        db.delete_table(u'tx_tecreports_filingmethod')

        # Deleting model 'Filing'
        db.delete_table(u'tx_tecreports_filing')


    models = {
        u'tx_tecreports.contributionsbyamount': {
            'Meta': {'ordering': "['low']", 'object_name': 'ContributionsByAmount'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'high': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats_by_amount'", 'to': u"orm['tx_tecreports.Report']"}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tx_tecreports.contributionsbydate': {
            'Meta': {'ordering': "['date']", 'object_name': 'ContributionsByDate'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats_by_date'", 'to': u"orm['tx_tecreports.Report']"}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tx_tecreports.contributionsbystate': {
            'Meta': {'ordering': "['-amount']", 'object_name': 'ContributionsByState'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats_by_state'", 'to': u"orm['tx_tecreports.Report']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tx_tecreports.contributionsbyzipcode': {
            'Meta': {'ordering': "['-amount']", 'object_name': 'ContributionsByZipcode'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats_by_zipcode'", 'to': u"orm['tx_tecreports.Report']"}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.contributor': {
            'Meta': {'object_name': 'Contributor'},
            'address_1': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'address_2': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'city': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'first_name': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_entity': ('django.db.models.fields.BooleanField', [], {}),
            'is_individual': ('django.db.models.fields.BooleanField', [], {}),
            'last_name': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'state': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'suffix': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contributors'", 'to': u"orm['tx_tecreports.ContributorType']"}),
            'zipcode': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'tx_tecreports.contributortype': {
            'Meta': {'object_name': 'ContributorType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.employer': {
            'Meta': {'object_name': 'Employer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.filer': {
            'Meta': {'object_name': 'Filer'},
            'filer_id': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'filer_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filers'", 'to': u"orm['tx_tecreports.FilerType']"}),
            'first_name': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_prefix': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_suffix': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'nickname': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'tx_tecreports.filertype': {
            'Meta': {'object_name': 'FilerType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.filing': {
            'Meta': {'object_name': 'Filing'},
            'filer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filings'", 'to': u"orm['tx_tecreports.Filer']"}),
            'filing_method': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filings'", 'to': u"orm['tx_tecreports.FilingMethod']"}),
            'is_correction': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'report_due': ('django.db.models.fields.DateField', [], {}),
            'report_filed': ('django.db.models.fields.DateField', [], {}),
            'report_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'primary_key': 'True'}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.filingmethod': {
            'Meta': {'object_name': 'FilingMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.filingtype': {
            'Meta': {'object_name': 'FilingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'})
        },
        u'tx_tecreports.receipt': {
            'Meta': {'ordering': "['date']", 'object_name': 'Receipt'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipts'", 'to': u"orm['tx_tecreports.Contributor']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tx_tecreports.Employer']", 'null': 'True', 'blank': 'True'}),
            'fec_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_out_of_state_pac': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_of_schedule': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tx_tecreports.Receipt']"}),
            'receipt_id': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipts'", 'to': u"orm['tx_tecreports.Report']"}),
            'travel': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'receipt'", 'unique': 'True', 'null': 'True', 'to': u"orm['tx_tecreports.Travel']"})
        },
        u'tx_tecreports.report': {
            'Meta': {'object_name': 'Report'},
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_original': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'report_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'report_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'through_date': ('django.db.models.fields.DateField', [], {})
        },
        u'tx_tecreports.travel': {
            'Meta': {'object_name': 'Travel'},
            'arrival_date': ('django.db.models.fields.DateField', [], {}),
            'departure_date': ('django.db.models.fields.DateField', [], {}),
            'departure_location': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'distination': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'first_name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'means_of': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'purpose': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'suffix': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'title': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['tx_tecreports']
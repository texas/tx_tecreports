# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Report.filer_id'
        db.add_column(u'tx_tecreports_report', 'filer_id',
                      self.gf('tx_tecreports.fields.OptionalMaxCharField')(max_length=250, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Report.filer_id'
        db.delete_column(u'tx_tecreports_report', 'filer_id')


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
            'cash_on_hand': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'filer_id': ('tx_tecreports.fields.OptionalMaxCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_original': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'outstanding_loans': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'report_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'report_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'through_date': ('django.db.models.fields.DateField', [], {}),
            'total_contributions': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'total_expenditures': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'unitemized_contributions': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'unitemized_expenditures': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'unitemized_loans': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'unitemized_pledges': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'})
        },
        u'tx_tecreports.travel': {
            'Meta': {'object_name': 'Travel'},
            'arrival_date': ('django.db.models.fields.DateField', [], {}),
            'departure_date': ('django.db.models.fields.DateField', [], {}),
            'departure_location': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
            'destination': ('tx_tecreports.fields.MaxCharField', [], {'max_length': '250'}),
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
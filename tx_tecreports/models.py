from django.db import models


class MaxCharField(models.CharField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = 250
        super(MaxCharField, self).__init__(**kwargs)


class OptionalMaxCharField(MaxCharField):
    def __init__(self, **kwargs):
        kwargs.update({
            'null': True,
            'blank': True,
        })
        super(OptionalMaxCharField, self).__init__(**kwargs)


class FilerType(models.Model):
    name = MaxCharField()

    def __unicode__(self):
        return self.name


class Filer(models.Model):
    filer_id = MaxCharField()
    filer_type = models.ForeignKey(FilerType, related_name='filers')
    last_name = OptionalMaxCharField()
    first_name = OptionalMaxCharField()
    name_prefix = OptionalMaxCharField()
    name_suffix = OptionalMaxCharField()
    nickname = OptionalMaxCharField()


class FilingType(models.Model):
    name = MaxCharField()

    def __unicode__(self):
        return self.name


class Employer(models.Model):
    name = MaxCharField()

    def __unicode__(self):
        return self.name


class Travel(models.Model):
    last_name = MaxCharField()
    first_name = MaxCharField()
    title = MaxCharField()
    suffix = MaxCharField()
    means_of = MaxCharField()
    departure_location = MaxCharField()
    departure_date = models.DateField()
    distination = MaxCharField()
    arrival_date = models.DateField()
    purpose = MaxCharField()


class Report(models.Model):
    report_number = models.PositiveIntegerField(default=0)
    is_original = models.BooleanField(default=True)
    from_date = models.DateField()
    through_date = models.DateField()
    # election = models.ForeignKey(tx_elections.Race)

    @property
    def total_receipts(self):
        pass


class ContributorType(models.Model):
    name = MaxCharField()

    def __unicode__(self):
        return self.name


class Contributor(models.Model):
    type_of = models.ForeignKey(ContributorType, related_name='contributors')
    is_individual = models.BooleanField()
    is_entity = models.BooleanField()
    last_name = OptionalMaxCharField()
    first_name = OptionalMaxCharField()
    title = OptionalMaxCharField()
    suffix = OptionalMaxCharField()
    address_1 = OptionalMaxCharField()
    address_2 = OptionalMaxCharField()
    city = OptionalMaxCharField()
    state = OptionalMaxCharField()
    zipcode = OptionalMaxCharField()


class Receipt(models.Model):
    report = models.ForeignKey(Report, related_name='receipts')
    parent = models.ForeignKey('self', related_name='children', blank=True,
            null=True)
    contributor = models.ForeignKey(Contributor, related_name='receipts')
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    employer = models.ForeignKey(Employer, null=True, blank=True)
    job_title = models.CharField(max_length=250, null=True, blank=True)
    travel = models.OneToOneField(Travel, related_name='receipt', null=True,
            blank=True)

    name_of_schedule = models.CharField(max_length=250)
    receipt_id = models.CharField(max_length=250)
    is_out_of_state_pac = models.BooleanField(default=False)
    fec_id = models.fec_id = models.CharField(max_length=250, null=True,
            blank=True)


class FilingMethod(models.Model):
    method = models.CharField(max_length=250)

    def __unicode__(self):
        return self.method


class Filing(models.Model):
    report_id = models.CharField(max_length=250, unique=True, primary_key=True)
    # TODO: Make this into a Filer
    filer = models.ForeignKey(Filer, related_name='filings')
    is_correction = models.BooleanField(default=False)
    report_type = models.CharField(max_length=250)
    report_due = models.DateField()
    report_filed = models.DateField()
    filing_method = models.ForeignKey(FilingMethod, related_name='filings')

    class Meta:
        get_latest_by = ['report_filed', ]

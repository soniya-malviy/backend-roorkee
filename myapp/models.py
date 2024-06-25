from django.db import models
from django.utils import timezone
import pytz

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set on creation
            tz = pytz.timezone('Asia/Kolkata')
            now = timezone.now()
            now = timezone.localtime(now, tz)
            self.created_at = now
        super().save(*args, **kwargs)

class State(TimeStampedModel):
    state_name = models.CharField(max_length=255, default="Tamil Nadu")

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ['state_name']
    def __str__(self):
        return self.state_name

class Department(TimeStampedModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='departments', null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['department_name']

    def __str__(self):
        return self.department_name

class Organisation(TimeStampedModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='organisations', null=True, blank=True)
    organisation_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ['organisation_name']
    
    def __str__(self):
        return self.organisation_name

class Scheme(TimeStampedModel):
    title = models.TextField(null = True, blank = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schemes', null=True, blank=True)
    introduced_on = models.DateTimeField(null = True, blank = True)
    valid_upto = models.DateTimeField(null = True, blank = True)
    funding_pattern = models.CharField(max_length=255, default="State")
    description = models.TextField(null = True, blank = True)
    scheme_link = models.URLField(null = True, blank = True)
    beneficiaries = models.ManyToManyField('Beneficiary', related_name='schemes', through='SchemeBeneficiary')
    documents = models.ManyToManyField('Document', related_name='schemes', through='SchemeDocument')
    sponsors = models.ManyToManyField('Sponsor', related_name='schemes', through='SchemeSponsor')

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        ordering = ['introduced_on']

    def __str__(self):
        return self.title

class Beneficiary(TimeStampedModel):
    beneficiary_type = models.CharField(max_length=255, default="SC/ST")

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ['beneficiary_type']
    
    def __str__(self):
        return self.beneficiary_type

class SchemeBeneficiary(TimeStampedModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='scheme_beneficiaries')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='beneficiary_schemes')

    class Meta:
        verbose_name = "Scheme Beneficiary"
        verbose_name_plural = "Scheme Beneficiaries"
        ordering = ['scheme', 'beneficiary']

    

class Benefit(TimeStampedModel):
    benefit_type = models.CharField(max_length=255, default="Grant")

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"
        ordering = ['benefit_type']

    def __str__(self):
        return self.benefit_type


# DOUBT BELOW
class Criteria(TimeStampedModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='criteria', null=True, blank=True)
    description = models.TextField(null = True, blank = True)
    value = models.TextField(null = True, blank = True)

    class Meta:
        verbose_name = "Criteria"
        verbose_name_plural = "Criteria"
        ordering = ['description']

    def __str__(self):
        return self.description

class Procedure(TimeStampedModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='procedures', null=True, blank=True)
    step_description = models.TextField(null = True, blank = True)

    class Meta:
        verbose_name = "Procedure"
        verbose_name_plural = "Procedures"
        ordering = ['scheme']

    def __str__(self):
        return self.step_description

class Document(TimeStampedModel):
    document_name = models.CharField(max_length=255, default="Aadhar Card")

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['document_name']

    def __str__(self):
        return self.document_name

class SchemeDocument(TimeStampedModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='scheme_documents')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_schemes')

    class Meta:
        verbose_name = "Scheme Document"
        verbose_name_plural = "Scheme Documents"
        ordering = ['scheme', 'document']

class Sponsor(TimeStampedModel):
    sponsor_type = models.CharField(max_length=255, default="State")

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ['sponsor_type']

    def __str__(self):
        return self.sponsor_type

class SchemeSponsor(TimeStampedModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='scheme_sponsors')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsor_schemes')

    class Meta:
        verbose_name = "Scheme Sponsor"
        verbose_name_plural = "Scheme Sponsors"
        ordering = ['scheme', 'sponsor']

    

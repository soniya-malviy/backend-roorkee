from django.db import models
from django.utils import timezone
import pytz

class Scheme(models.Model):
    
    scheme_id = models.IntegerField(null=True, blank = True)
    department = models.CharField(max_length=255, null=True, blank = True)
    scheme_name = models.CharField(max_length=255, default="Unknown")
    description = models.TextField()
    lower_age = models.IntegerField(default=0)
    upper_age = models.IntegerField(default=0)
    introduced_on = models.DateTimeField()
    valid_upto = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set on creation
            tz = pytz.timezone('Asia/Kolkata')
            now = timezone.now()
            now = timezone.localtime(now, tz)
            self.created_at = now
        super().save(*args, **kwargs)

    

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        ordering = ['scheme_name']


class SchemeDetail(models.Model):

    scheme = models.OneToOneField(Scheme, on_delete=models.CASCADE, related_name='details',null=True, blank = True)
    beneficiaries = models.CharField(max_length=255, default="Unknown")
    benefits = models.CharField(max_length=255)
    how_to_avail = models.CharField(max_length=255, default="Unknown")
    category = models.CharField(max_length=255, default="Unknown")
    objective = models.CharField(max_length=255, default="Unknown")
    funding_pattern = models.CharField(max_length=255, default="Unknown")
    application_process = models.CharField(max_length=255, default="Unknown")
    contact_office = models.CharField(max_length=255, default="Unknown")
    scheme_link = models.URLField()
    required_documents = models.CharField(max_length=255, default="Unknown")
    other_information = models.CharField(max_length=255, default="Unknown")
    test_info = models.URLField(default = "www.google.com")

    

    class Meta:
        verbose_name = "Scheme Detail"
        verbose_name_plural = "Scheme Details"


class Criteria(models.Model):
    
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='criteria',null=True, blank = True)
    income = models.IntegerField()
    age = models.IntegerField()
    community = models.CharField(max_length=255)
    other_details = models.CharField(max_length=255)

    

    class Meta:
        verbose_name = "Criteria"
        verbose_name_plural = "Criteria"
        ordering = ['community']


class Sponsor(models.Model):
    
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='sponsors',null=True, blank = True)
    sponsor_id = models.IntegerField()
    sponsor_name = models.CharField(max_length=255)

    

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ['sponsor_name']
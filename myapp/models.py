from django.db import models
from django.utils import timezone
import pytz




class Scheme(models.Model):
    scheme_id = models.CharField(max_length=360,default = "Unknown")
    department = models.CharField(max_length=255,default = "Unknown")
    scheme_name = models.CharField(max_length=255,default = "Unknown")
    description = models.TextField()
    beneficiaries = models.CharField(max_length=255,default = "Unknown")
    benefits = models.CharField(max_length=255)
    how_to_avail = models.CharField(max_length=255,default = "Unknown")
    sponsors = models.CharField(max_length=255,default = "Unknown")
    lower_age = models.IntegerField(default = 0)
    upper_age = models.IntegerField(default = 0)
    introduced_on = models.IntegerField(default = 0)
    valid_upto = models.IntegerField(default = 0)
    category = models.CharField(max_length=255,default = "Unknown")
    objective = models.CharField(max_length=255,default = "Unknown")
    funding_pattern = models.CharField(max_length=255,default = "Unknown")
    application_process = models.CharField(max_length=255,default = "Unknown")
    contact_office = models.CharField(max_length=255, default = "Unknown")
    scheme_link = models.URLField()
    required_documents = models.CharField(max_length=255,default = "Unknown")
    other_information = models.CharField(max_length=255,default = "Unknown")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set on creation
            tz = pytz.timezone('Asia/Kolkata')
            now = timezone.now()
            now = timezone.localtime(now, tz)
            self.created_at = now
        super().save(*args, **kwargs)

    def __str__(self):
        return self.scheme_name

class Criteria(models.Model):
    income = models.IntegerField()
    age = models.IntegerField()
    community = models.CharField(max_length=255)
    other_details = models.CharField(max_length=255)
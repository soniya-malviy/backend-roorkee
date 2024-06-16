from django.db import models


class Department(models.Model):
    department_id = models.CharField(max_length=36, unique=True)
    department_name = models.CharField(max_length=255)

class Scheme(models.Model):
    scheme_id = models.CharField(max_length=36, unique=True)
    department = models.CharField(max_length=255, default='Unknown')
    scheme_name = models.CharField(max_length=255)
    description = models.TextField()
    scheme_beneficiary = models.CharField(max_length=255)
    scheme_benefits = models.CharField(max_length=255)
    how_to_avail = models.CharField(max_length=255)
    sponsors = models.CharField(max_length=255)
    age_from = models.CharField(max_length=255, blank=True, null=True)
    age_to = models.CharField(max_length=255, blank=True, null=True)
    funding = models.CharField(max_length=255)
    scheme_link = models.URLField()
    json_data = models.JSONField()

    def __str__(self):
        return self.scheme_name


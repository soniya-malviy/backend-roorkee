from django.db import models
from django.utils import timezone
import pytz
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
import re
from dirtyfields import DirtyFieldsMixin
from orderable.models import Orderable

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_MEDIA_STORAGE_BUCKET_NAME
    location = "media"
    file_overwrite = False


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set on creation
            tz = pytz.timezone("Asia/Kolkata")
            now = timezone.now()
            now = timezone.localtime(now, tz)
            self.created_at = now
        super().save(*args, **kwargs)


# Existing models
class State(TimeStampedModel):
    state_name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def clean(self):
        if not self.state_name.strip():  # Disallow empty or whitespace-only names
            raise ValidationError("State name cannot be empty or whitespace.")
        if re.search(r"\d", self.state_name):  # Check if state_name contains any digit
            raise ValidationError("State name cannot contain numeric characters.")

    def save(self, *args, **kwargs):
        # Strip whitespace before saving
        if self.state_name is not None:
            self.state_name = self.state_name.strip().title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["state_name"]

    def __str__(self):
        return self.state_name or "N/A"


class Department(TimeStampedModel):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="departments",
        null=False,
        blank=False,
    )
    department_name = models.CharField(max_length=255, null=True, blank=True)

    def clean(self):
        if re.search(r"\d", self.department_name):
            raise ValidationError("Department name cannot contain numeric characters.")

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["department_name"]

    def __str__(self):
        return self.department_name or "N/A"

    def get_group(self):
        department_name = self.department_name.lower() if self.department_name else ""

        EDUCATION_KEYWORDS = [
            "education",
            "scholarship",
            "training",
            "student",
            "care and protection",
            "vocational",
        ]
        AGRICULTURE_KEYWORDS = [
            "agriculture",
            "farmer",
            "soil",
            "water",
            "conservation",
        ]
        HEALTH_KEYWORDS = ["health", "medical", "family welfare"]
        SOCIAL_WELFARE_KEYWORDS = [
            "social welfare",
            "women and child development",
            "child development",
            "welfare of sc/st/obc & minority",
            "social",
        ]
        INFRASTRUCTURE_KEYWORDS = [
            "public works",
            "urban development",
            "housing",
            "rural development",
        ]
        EMPLOYMENT_KEYWORDS = [
            "employment",
            "labour",
            "skill development",
            "entrepreneurship",
        ]
        OTHER_KEYWORDS = [
            "tourism",
            "culture",
            "information technology",
            "science and technology",
        ]

        # Check for each group and return the appropriate classification
        if any(keyword in department_name for keyword in HEALTH_KEYWORDS):
            return "Health"
        elif any(keyword in department_name for keyword in SOCIAL_WELFARE_KEYWORDS):
            return "Social Welfare"
        elif any(keyword in department_name for keyword in INFRASTRUCTURE_KEYWORDS):
            return "Infrastructure"
        elif any(keyword in department_name for keyword in EMPLOYMENT_KEYWORDS):
            return "Employment"
        elif any(keyword in department_name for keyword in AGRICULTURE_KEYWORDS):
            return "Agriculture"
        elif any(keyword in department_name for keyword in EDUCATION_KEYWORDS):
            return "Education"
        elif any(keyword in department_name for keyword in OTHER_KEYWORDS):
            return "Other"
        else:
            return "Unclassified"


class Organisation(TimeStampedModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="organisations",
        null=True,
        blank=True,
    )
    organisation_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ["organisation_name"]

    def __str__(self):
        return self.organisation_name or "N/A"


class Tag(DirtyFieldsMixin, TimeStampedModel):
    CATEGORY_CHOICES = [
        ("scholarship", "Scholarship"),
        ("job", "Job Opening"),
        ("sc", "Scheduled Caste (SC)"),
        ("st", "Scheduled Tribe (ST)"),
        ("obc", "Other Backward Classes (OBC)"),
        ("minority", "Minority Community"),
        ("general", "General"),
    ]
    name = models.CharField(max_length=255, unique=True)
    weight = models.FloatField(default=1.0)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="general"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        scholarship_keywords = ["scholarship", "fellowship", "grant"]
        job_keywords = ["job", "employment", "recruitment", "vacancy", "career"]
        sc_keywords = ["sc", "scheduled caste"]
        st_keywords = ["st", "scheduled tribe"]
        obc_keywords = ["obc", "other backward classes"]
        minority_keywords = [
            "minority",
            "muslim",
            "christian",
            "sikh",
            "buddhist",
            "jain",
            "parsi",
        ]

        tag_lower = self.name.lower()

        if any(keyword in tag_lower for keyword in scholarship_keywords):
            self.category = "scholarship"
        elif any(keyword in tag_lower for keyword in job_keywords):
            self.category = "job"
        elif any(keyword in tag_lower for keyword in sc_keywords):
            self.category = "sc"
        elif any(keyword in tag_lower for keyword in st_keywords):
            self.category = "st"
        elif any(keyword in tag_lower for keyword in obc_keywords):
            self.category = "obc"
        elif any(keyword in tag_lower for keyword in minority_keywords):
            self.category = "minority"
        else:
            self.category = "general"

        if self.pk:
            old_tag = Tag.objects.get(pk=self.pk)
            if old_tag.weight != self.weight:
                related_tags = Tag.objects.filter(category=self.category)
                related_tags.update(weight=self.weight)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or "N/A"


class Scheme(TimeStampedModel):
    title = models.TextField(null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="schemes",
        null=True,
        blank=True,
    )
    introduced_on = models.TextField(null=True, blank=True)
    valid_upto = models.TextField(null=True, blank=True)
    funding_pattern = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    scheme_link = models.URLField(null=True, blank=True)
    beneficiaries = models.ManyToManyField(
        "Beneficiary", related_name="schemes", through="SchemeBeneficiary"
    )
    documents = models.ManyToManyField(
        "Document", related_name="schemes", through="SchemeDocument"
    )
    pdf_url = models.URLField(null=True, blank=True)
    sponsors = models.ManyToManyField(
        "Sponsor", related_name="schemes", through="SchemeSponsor"
    )
    tags = models.ManyToManyField(
        "Tag", related_name="schemes", blank=True
    )  # Add this line
    benefits = models.ManyToManyField("Benefit", related_name="schemes", blank=True)

    def clean(self):
        if not self.title.strip():  # Disallow empty or whitespace-only names
            raise ValidationError("Title name cannot be empty or whitespace.")

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        ordering = ["introduced_on"]

    def __str__(self):
        return self.title or "N/A"


class Benefit(TimeStampedModel):
    benefit_type = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"
        ordering = ["benefit_type"]

    def __str__(self):
        return self.benefit_type or "N/A"


class Beneficiary(TimeStampedModel):
    beneficiary_type = models.CharField(max_length=255, null=True, blank=True)

    def clean(self):
        if re.search(r"\d", self.beneficiary_type):
            raise ValidationError("Beneficiary cannot contain numeric characters.")

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["beneficiary_type"]

    def __str__(self):
        return self.beneficiary_type or "N/A"


class SchemeBeneficiary(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="scheme_beneficiaries"
    )
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.CASCADE, related_name="beneficiary_schemes"
    )

    class Meta:
        verbose_name = "Scheme Beneficiary"
        verbose_name_plural = "Scheme Beneficiaries"
        ordering = ["scheme", "beneficiary"]


# DOUBT BELOW
class Criteria(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="criteria", null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    criteria_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Criteria"
        verbose_name_plural = "Criteria"
        ordering = ["description"]

    def __str__(self):
        return self.description if self.description else "Unnamed Criteria"


class Procedure(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.CASCADE,
        related_name="procedures",
        null=True,
        blank=True,
    )
    step_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Procedure"
        verbose_name_plural = "Procedures"
        ordering = ["scheme"]

    def __str__(self):
        return self.step_description or "N/A"


class Document(TimeStampedModel):
    document_name = models.CharField(max_length=255, null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ["document_name"]

    def __str__(self):
        return self.document_name or "N/A"


class SchemeDocument(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="scheme_documents"
    )
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="document_schemes"
    )

    class Meta:
        verbose_name = "Scheme Document"
        verbose_name_plural = "Scheme Documents"
        ordering = ["scheme", "document"]


class Sponsor(TimeStampedModel):
    sponsor_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ["sponsor_type"]

    def __str__(self):
        return self.sponsor_type or "N/A"


class SchemeSponsor(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="scheme_sponsors"
    )
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="sponsor_schemes"
    )

    class Meta:
        verbose_name = "Scheme Sponsor"
        verbose_name_plural = "Scheme Sponsors"
        ordering = ["scheme", "sponsor"]


# Temporary models for new data


class TempState(TimeStampedModel):
    state_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.state_name or "N/A"


class TempDepartment(TimeStampedModel):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="temp_departments",
        null=True,
        blank=True,
    )
    department_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.department_name


class TempOrganisation(TimeStampedModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="temp_organisations",
        null=True,
        blank=True,
    )
    organisation_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.organisation_name


class TempScheme(TimeStampedModel):
    title = models.TextField(null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="temp_schemes",
        null=True,
        blank=True,
    )
    introduced_on = models.DateTimeField(null=True, blank=True)
    valid_upto = models.DateTimeField(null=True, blank=True)
    funding_pattern = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    scheme_link = models.URLField(null=True, blank=True)
    beneficiaries = models.ManyToManyField(
        "Beneficiary", related_name="temp_schemes", through="TempSchemeBeneficiary"
    )
    documents = models.ManyToManyField(
        "Document", related_name="temp_schemes", through="TempSchemeDocument"
    )
    sponsors = models.ManyToManyField(
        "Sponsor", related_name="temp_schemes", through="TempSchemeSponsor"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class TempSchemeBeneficiary(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="temp_scheme_beneficiaries"
    )
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.CASCADE, related_name="temp_beneficiary_schemes"
    )

    class Meta:
        abstract = True


class TempBenefit(TimeStampedModel):
    benefit_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.benefit_type


class TempCriteria(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.CASCADE,
        related_name="temp_criteria",
        null=True,
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.description


class TempProcedure(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.CASCADE,
        related_name="temp_procedures",
        null=True,
        blank=True,
    )
    step_description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.step_description


class TempDocument(TimeStampedModel):
    document_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.document_name


class TempSchemeDocument(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="temp_scheme_documents"
    )
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="temp_document_schemes"
    )

    class Meta:
        abstract = True


class TempSponsor(TimeStampedModel):
    sponsor_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.sponsor_type


class TempSchemeSponsor(TimeStampedModel):
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="temp_scheme_sponsors"
    )
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="temp_sponsor_schemes"
    )

    class Meta:
        abstract = True


# USER REGISTRATION START


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


def default_verification_token_expiry():
    return timezone.now() + timedelta(days=1)


# class Choice(models.Model):
#     CATEGORY_CHOICES = [
#         ('education', 'Education'),
#         ('disability', 'Disability'),
#         ('employment', 'Employment'),
#     ]

#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
#     name = models.CharField(max_length=100)  # The actual choice value
#     description = models.TextField(blank=True, null=True)  # Optional field for additional details
#     is_active = models.BooleanField(default=True)  # To allow enabling/disabling specific choices

#     def __str__(self):
#         return f"{self.category} - {self.name}"


class ProfileField(models.Model):
    FIELD_TYPE_CHOICES = [
        ("char", "Text"),
        ("integer", "Integer"),
        ("boolean", "Boolean"),
        ("decimal", "Decimal"),
        ("date", "Date"),
        ("choice", "Choice"),
    ]

    name = models.CharField(max_length=100, unique=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    min_value = models.IntegerField(
        blank=True, null=True, help_text="Minimum value for integer fields."
    )
    max_value = models.IntegerField(
        blank=True, null=True, help_text="Maximum value for integer fields."
    )
    position = models.IntegerField(default=1)

    def clean(self):
        # Ensure min_value is less than max_value if both are set
        if (
            self.field_type == "integer"
            and self.min_value is not None
            and self.max_value is not None
        ):
            if self.min_value > self.max_value:
                raise ValidationError(
                    "Minimum value cannot be greater than the maximum value."
                )

    def save(self, *args, **kwargs):
        if self.pk:
            original_field = ProfileField.objects.get(pk=self.pk)
            if original_field.position != self.position:
                self.shift_positions(original_field.position, self.position)

        super(ProfileField, self).save(*args, **kwargs)

    def shift_positions(self, old_position, new_position):
        if old_position < new_position:
            ProfileField.objects.filter(
                position__gt=old_position, position__lte=new_position
            ).update(position=models.F("position") - 1)
        elif old_position > new_position:
            ProfileField.objects.filter(
                position__gte=new_position, position__lt=old_position
            ).update(position=models.F("position") + 1)

        self.position = new_position

    def __str__(self):
        return self.name


class ProfileFieldChoice(models.Model):
    field = models.ForeignKey(
        ProfileField, on_delete=models.CASCADE, related_name="choices"
    )
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.field.name} - {self.value}"


class ProfileFieldValue(models.Model):
    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="profile_field_values"
    )
    field = models.ForeignKey(ProfileField, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.field.name}: {self.value}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    CATEGORY_CHOICES = [
        ("General", "General"),
        ("OBC", "OBC"),
        ("SC", "SC"),
        ("ST", "ST"),
    ]

    STATE_CHOICES = [
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Arunachal Pradesh", "Arunachal Pradesh"),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jharkhand", "Jharkhand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telangana", "Telangana"),
        ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("Uttarakhand", "Uttarakhand"),
        ("West Bengal", "West Bengal"),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    saved_schemes = models.ManyToManyField("Scheme", related_name="saved_by_users")
    # DETAILS BELOW
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_field_value = models.JSONField(blank=True, null=True)
    # gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    # age = models.PositiveIntegerField(blank=True, null=True)
    # occupation = models.CharField(max_length=100, blank=True, null=True)
    # income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # education = models.CharField(max_length=100, choices=[('None', 'None'), ('High School', 'High School'), ('Undergraduate', 'Undergraduate'), ('Postgraduate', 'Postgraduate'), ('Doctoral', 'Doctoral'),('Pre-primary', 'Pre-primary'), ('Secondary', 'Secondary'), ('Higher Secondary', 'Higher Secondary'), ('Diploma/Certification', 'Diploma/Certification')], blank=True, null=True)
    # education = models.ForeignKey(EducationChoice, on_delete=models.SET_NULL, blank=True, null=True)
    # employment_status = models.CharField(max_length=100, choices=[('Employed', 'Employed'), ('Self-employed', 'Business'), ('Unemployed', 'Unemployed')], blank=True, null=True)
    # education = models.ForeignKey(
    #     Choice,
    #     on_delete=models.SET_NULL,
    #     limit_choices_to={'category': 'education'},
    #     null=True,
    #     blank=True,
    #     related_name='education_choices'
    # )
    # disability = models.ForeignKey(
    #     Choice,
    #     on_delete=models.SET_NULL,
    #     limit_choices_to={'category': 'disability'},
    #     null=True,
    #     blank=True,
    #     related_name='disability_choices'
    # )
    # employment_status = models.ForeignKey(
    #     Choice,
    #     on_delete=models.SET_NULL,
    #     limit_choices_to={'category': 'employment'},
    #     null=True,
    #     blank=True,
    #     related_name='employment_choices'
    # )
    # government_employee = models.BooleanField(default=False)
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    # minority = models.BooleanField(default=False)
    # state_of_residence = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    # disability = models.ForeignKey(DisabilityChoice, on_delete=models.SET_NULL, blank=True, null=True)
    # bpl_card_holder = models.CharField(max_length=255, default = "NO")

    is_email_verified = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


# BANNER BELOW


class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        storage=MediaStorage(), upload_to="banners/", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


User = get_user_model()


class SavedFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    criteria = models.JSONField()  # Store filter criteria as JSON

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class SchemeReport(models.Model):
    REPORT_CATEGORIES = [
        ("incorrect_info", "Incorrect Information"),
        ("outdated_info", "Outdated Information"),
        ("other", "Other"),
    ]

    scheme_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    report_category = models.CharField(max_length=50, choices=REPORT_CATEGORIES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Scheme {self.scheme_id} - {self.report_category}"


class WebsiteFeedback(models.Model):
    FEEDBACK_CATEGORIES = [
        ("bug", "Bug Report"),
        ("improvement", "Improvement Suggestion"),
        ("general", "General Feedback"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50, choices=FEEDBACK_CATEGORIES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback - {self.category}"


class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    interaction_value = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)


class SchemeFeedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scheme_feedbacks"
    )
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="feedbacks"
    )
    feedback = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.scheme.title}"


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event_type} - {self.scheme.title}"


class LayoutItem(models.Model):
    COLUMN_CHOICES = [
        ("Schemes", "Schemes"),
        ("Scholarships", "Scholarships"),
        ("Jobs", "Jobs"),
    ]

    column_name = models.CharField(max_length=20, choices=COLUMN_CHOICES, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.get_column_name_display()

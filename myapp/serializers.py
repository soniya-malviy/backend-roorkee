from rest_framework import serializers
from .models import (State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, Criteria
                     , Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor, CustomUser,Banner, SavedFilter )
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
import pytz
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django.utils.text import slugify
import random
import string

User = get_user_model()
class TimeStampedModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z', read_only=True)


    def create(self, validated_data):
        tz = pytz.timezone('Asia/Kolkata')
        now = timezone.now()
        now = timezone.localtime(now, tz)
        validated_data['created_at'] = now
        return super().create(validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tz = pytz.timezone('Asia/Kolkata')
        created_at = instance.created_at
        if created_at:
            created_at = timezone.localtime(created_at, tz)
            ret['created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S %Z')
        return ret


class StateSerializer(TimeStampedModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'state_name', 'created_at']

class DepartmentSerializer(TimeStampedModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), source='state.state_name')
    group = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = '__all__'

    def get_group(self, obj):
        return obj.get_group()

class OrganisationSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'



class BeneficiarySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'

class SponsorSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class BenefitSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class SchemeSerializer(TimeStampedModelSerializer):
    department = DepartmentSerializer()
    beneficiaries = BeneficiarySerializer(many=True)
    sponsors = SponsorSerializer(many=True)
    benefits = BenefitSerializer(many=True, read_only=True)
    class Meta:
        model = Scheme
        fields = '__all__'

class SchemeBeneficiarySerializer(TimeStampedModelSerializer):
    beneficiary = BeneficiarySerializer()
    class Meta:
        model = SchemeBeneficiary
        fields = '__all__'



class CriteriaSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Criteria
        fields = '__all__'

class ProcedureSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'document_name', 'created_at']

class SchemeDocumentSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()
    document = DocumentSerializer()

    class Meta:
        model = SchemeDocument
        fields = ['id', 'created_at', 'scheme', 'document']



class SchemeSponsorSerializer(TimeStampedModelSerializer):
    sponsor = serializers.StringRelatedField()
    class Meta:
        model = SchemeSponsor
        fields = '__all__'

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'preferences', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']

# UserPreferencesSerializer
# class UserPreferencesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPreferences
#         fields = ['preferred_categories', 'dark_mode', 'language', 'browsing_history']

# UserSerializer
# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer(required=False)
#     preferences = UserPreferencesSerializer(required=False)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'profile', 'preferences']

#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         preferences_data = validated_data.pop('preferences', None)

#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()

#         # Handle profile data
#         if profile_data:
#             UserProfile.objects.update_or_create(user=instance, defaults=profile_data)

#         # Handle preferences data
#         if preferences_data:
#             UserPreferences.objects.update_or_create(user=instance, defaults=preferences_data)

#         return instance

# SaveSchemeSerializer
class SaveSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['saved_schemes']

    def update(self, instance, validated_data):
        saved_schemes = validated_data.get('saved_schemes')
        instance.saved_schemes.set(saved_schemes)
        instance.save()
        return instance

# UserRegistrationSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    is_email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_email_verified']
        extra_kwargs = {
            
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if len(value) < 4:
            raise serializers.ValidationError("The username must be at least 4 characters long.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    # def send_verification_email(self, user):
    #     token = default_token_generator.make_token(user)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     verification_link = f"{settings.SITE_URL}/verify-email/{uid}/{token}/"

    #     subject = 'Verify your email'
    #     message = render_to_string('email_verification.html', {
    #         'user': user,
    #         'verification_link': verification_link,
    #     })

    #     email = EmailMessage(
    #         subject=subject,
    #         body=message,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         to=[user.email]
    #     )
    #     email.content_subtype = 'html'  # Set the email content type to HTML
    #     email.send(fail_silently=False)

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"{settings.SITE_URL}/verify-email/{uid}/{token}/"

        subject = 'Verify your email'
        
        # Render the HTML content from your template
        html_content = render_to_string('email_verification.html', {
            'user': user,
            'verification_link': verification_link,
        })
        
        # Optionally, create a plain text alternative
        text_content = strip_tags(html_content)  # Import strip_tags if not already done

        # Create the email with both plain text and HTML content
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # This can be the plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")  # Attach the HTML version
        email.send(fail_silently=False)

    def create(self, validated_data):
        email = validated_data['email']
        username_base = slugify(email.split('@')[0])

        if len(username_base) < 4:
            username_base += ''.join(random.choices(string.ascii_lowercase + string.digits, k=4-len(username_base)))

        username = username_base

        if User.objects.filter(username=username).exists():
            counter = 1
            new_username = f"{username}{counter}"
            while User.objects.filter(username=new_username).exists():
                counter += 1
                new_username = f"{username}{counter}"
            username = new_username

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )

        # Send verification email
        self.send_verification_email(user)

        return user
    
    

    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'name', 'gender', 'age', 'category', 'minority', 'state_of_residence', 
            'disability', 'bpl_card_holder', 'occupation', 'income', 'education', 
            'government_employee', 'employment_status'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    


# BELOW USER LOGIN SERIALIZER


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Using email for authentication
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return {'user': user}
        
        raise serializers.ValidationError('Invalid credentials')
    
# BANNER SER BELOW
    
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'description', 'image', 'is_active')

class SavedFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedFilter
        fields = ['id', 'name', 'criteria']



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = force_bytes(urlsafe_base64_decode(attrs['uid']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid UID.")
        
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError("Invalid token.")
        
        return attrs

    def save(self):
        uid = force_bytes(urlsafe_base64_decode(self.validated_data['uid']))
        user = CustomUser.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
    


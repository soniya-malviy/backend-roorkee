from rest_framework import serializers
from .models import State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor
from django.utils import timezone
import pytz

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
    class Meta:
        model = Department
        fields = '__all__'

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

class SchemeSerializer(TimeStampedModelSerializer):
    department = DepartmentSerializer()
    beneficiaries = BeneficiarySerializer(many=True)
    sponsors = SponsorSerializer(many=True)
    class Meta:
        model = Scheme
        fields = '__all__'

class SchemeBeneficiarySerializer(TimeStampedModelSerializer):
    beneficiary = BeneficiarySerializer()
    class Meta:
        model = SchemeBeneficiary
        fields = '__all__'

class BenefitSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Benefit
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


# from django.contrib.auth.models import User
# from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['bio']

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'profile']

#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile')
#         profile = instance.profile

#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()

#         profile.bio = profile_data.get('bio', profile.bio)
#         profile.save()

#         return instance
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'preferences', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']  # These fields are read-only

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'profile']

#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         profile = instance.profile

#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()

#         if profile_data:
#             profile.bio = profile_data.get('bio', profile.bio)
#             profile.preferences = profile_data.get('preferences', profile.preferences)
#             profile.save()

#         return instance

# myapp/serializers.py

from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserPreferences


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'preferences', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['preferred_categories', 'dark_mode', 'language', 'browsing_history']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    preferences = UserPreferencesSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'preferences']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        preferences_data = validated_data.pop('preferences', None)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Handle profile data
        if profile_data:
            UserProfile.objects.update_or_create(user=instance, defaults=profile_data)

        # Handle preferences data
        if preferences_data:
            UserPreferences.objects.update_or_create(user=instance, defaults=preferences_data)

        return instance


# class BrowsingHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BrowsingHistory
#         fields = ['item_id', 'viewed_at']

# class RecommendationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recommendation
#         fields = ['item_id', 'recommended_at', 'score']
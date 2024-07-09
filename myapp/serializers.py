from rest_framework import serializers
from .models import State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor, CustomUser
from django.utils import timezone
from django.contrib.auth import authenticate
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

class SaveSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['saved_schemes']

    def update(self, instance, validated_data):
        saved_schemes = validated_data.get('saved_schemes')
        instance.saved_schemes.set(saved_schemes)
        instance.save()
        return instance
    
# BELOW USER REGISTRATION SERIALIZER
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
# BELOW USER LOGIN SERIALIZER
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError('Invalid credentials')
    

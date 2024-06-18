from myapp.models import Scheme, Criteria, Sponsor
from rest_framework import serializers
from django.utils import timezone
import pytz

class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = '__all__'


class SchemeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    class Meta:
        model = Scheme
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert UTC time to IST
        ist_timezone = pytz.timezone('Asia/Kolkata')
        data['created_at'] = instance.created_at.astimezone(ist_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
        data['updated_at'] = instance.updated_at.astimezone(ist_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
        return data
    
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'
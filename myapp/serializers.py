from myapp.models import Scheme, Department
from rest_framework import serializers

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "deprtment_id",
            "department_name"
        )


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = ( 
            "scheme_id", 
            "department",
            "scheme_name",
            "description",
            "scheme_beneficiary",
            "scheme_benefits",
            "how_to_avail",
            "sponsors",
            "age_from",
            "age_to",

            "scheme_link"
        
        )
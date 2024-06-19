from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from myapp.models import Scheme, Criteria, Sponsor
from .serializers import SchemeSerializer, SponsorSerializer, CriteriaSerializer

class SchemeAPIView(generics.ListAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at'] 

    def get_queryset(self):
        department = self.request.query_params.get('department', None)  
        if department:
            return self.queryset.filter(department=department)  
        return self.queryset.all()  
    
class CriteriaAPIView(generics.ListAPIView):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer 
    

    def get_queryset(self):
        scheme_id = self.request.query_params.get('scheme_id', None)  
        if scheme_id:
            return self.queryset.filter(scheme__id=scheme_id)  
        return self.queryset.all()


class SponsorAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 
    

    def get_queryset(self):
        scheme_id = self.request.query_params.get('scheme_id', None)  
        if scheme_id:
            return self.queryset.filter(scheme__id=scheme_id)  
        return self.queryset.all()
    

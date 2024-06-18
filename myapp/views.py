from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from myapp.models import Scheme
from .serializers import SchemeSerializer

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
    

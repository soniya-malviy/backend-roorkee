from django.shortcuts import render
from rest_framework import generics
from myapp.models import Scheme
from .serializers import SchemeSerializer

class SchemeAPIView(generics.ListAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer 
    

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor
from .serializers import StateSerializer, DepartmentSerializer, OrganisationSerializer, SchemeSerializer, BeneficiarySerializer, SchemeBeneficiarySerializer, BenefitSerializer, CriteriaSerializer, ProcedureSerializer, DocumentSerializer, SchemeDocumentSerializer, SponsorSerializer, SchemeSponsorSerializer

class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class OrganisationListAPIView(generics.ListAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SchemeListAPIView(generics.ListAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['introduced_on']
    ordering = ['-introduced_on']

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return self.queryset.filter(department_id=department_id)
        return self.queryset.all()

class SchemeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer

class BeneficiaryListAPIView(generics.ListAPIView):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SchemeBeneficiaryListAPIView(generics.ListAPIView):
    queryset = SchemeBeneficiary.objects.all()
    serializer_class = SchemeBeneficiarySerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class BenefitListAPIView(generics.ListAPIView):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class CriteriaListAPIView(generics.ListAPIView):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.request.query_params.get('scheme_id')
        if scheme_id:
            return self.queryset.filter(scheme_id=scheme_id)
        return self.queryset.all()

class ProcedureListAPIView(generics.ListAPIView):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.request.query_params.get('scheme_id')
        if scheme_id:
            return self.queryset.filter(scheme_id=scheme_id)
        return self.queryset.all()

class DocumentListAPIView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SchemeDocumentListAPIView(generics.ListAPIView):
    queryset = SchemeDocument.objects.all()
    serializer_class = SchemeDocumentSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SchemeSponsorListAPIView(generics.ListAPIView):
    queryset = SchemeSponsor.objects.all()
    serializer_class = SchemeSponsorSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

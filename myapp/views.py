from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import (
    State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, 
    Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor
)
from .serializers import (
    StateSerializer, DepartmentSerializer, OrganisationSerializer, SchemeSerializer, 
    BeneficiarySerializer, SchemeBeneficiarySerializer, BenefitSerializer, 
    CriteriaSerializer, ProcedureSerializer, DocumentSerializer, 
    SchemeDocumentSerializer, SponsorSerializer, SchemeSponsorSerializer
)
from rest_framework.exceptions import NotFound
from .filters import CustomOrderingFilter


class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'state_name']
    ordering = ['-created_at']

class StateSchemesListAPIView(generics.ListAPIView):
    serializer_class = SchemeSerializer

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        if state_id:
            return Scheme.objects.filter(department__state_id=state_id)
        return Scheme.objects.none() # or return an appropriate queryset when state_id is not provided
    
class StateDetailAPIView(generics.RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'department_name']
    ordering = ['-created_at']

class OrganisationListAPIView(generics.ListAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'organisation_name']
    ordering = ['-created_at']

class SchemeListAPIView(generics.ListAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['introduced_on', 'title']
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
    ordering_fields = ['created_at', 'beneficiary_type']
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
    ordering_fields = ['created_at', 'benefit_type']
    ordering = ['-created_at']

class CriteriaListAPIView(generics.ListAPIView):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'description']
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
    ordering_fields = ['created_at', 'document_name']
    ordering = ['-created_at']

class SchemeDocumentListAPIView(generics.ListAPIView):
    serializer_class = SchemeDocumentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs['scheme_id']
        return SchemeDocument.objects.filter(scheme__id=scheme_id)

    

class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'sponsor_type']
    ordering = ['-created_at']

class SchemeSponsorListAPIView(generics.ListAPIView):
    queryset = SchemeSponsor.objects.all()
    serializer_class = SchemeSponsorSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class StateDepartmentsListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'department_name']
    ordering = ['-created_at']

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        if not state_id:
            raise NotFound("State ID not provided.")
        return Department.objects.filter(state_id=state_id)

class DepartmentSchemesListAPIView(generics.ListAPIView):
    serializer_class = SchemeSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['introduced_on', 'title']
    ordering = ['-introduced_on']

    def get_queryset(self):
        department_id = self.kwargs.get('department_id')
        if not department_id:
            raise NotFound("Department ID not provided.")
        return Scheme.objects.filter(department_id=department_id)

class SchemeBeneficiariesListAPIView(generics.ListAPIView):
    serializer_class = SchemeBeneficiarySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs.get('scheme_id')
        if not scheme_id:
            raise NotFound("Scheme ID not provided.")
        return SchemeBeneficiary.objects.filter(scheme_id=scheme_id)

class SchemeCriteriaListAPIView(generics.ListAPIView):
    serializer_class = CriteriaSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'description']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs.get('scheme_id')
        if not scheme_id:
            raise NotFound("Scheme ID not provided.")
        return Criteria.objects.filter(scheme_id=scheme_id)

class SchemeProceduresListAPIView(generics.ListAPIView):
    serializer_class = ProcedureSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs.get('scheme_id')
        if not scheme_id:
            raise NotFound("Scheme ID not provided.")
        return Procedure.objects.filter(scheme_id=scheme_id)

class SchemeDocumentsListAPIView(generics.ListAPIView):
    serializer_class = SchemeDocumentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs.get('scheme_id')
        if not scheme_id:
            raise NotFound("Scheme ID not provided.")
        return SchemeDocument.objects.filter(scheme_id=scheme_id)

class SchemeSponsorsListAPIView(generics.ListAPIView):
    serializer_class = SchemeSponsorSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        scheme_id = self.kwargs.get('scheme_id')
        if not scheme_id:
            raise NotFound("Scheme ID not provided.")
        return SchemeSponsor.objects.filter(scheme_id=scheme_id)


# from rest_framework import generics, permissions
# from rest_framework.permissions import IsAuthenticated

# from .models import UserProfile
# from .serializers import UserSerializer, UserProfileSerializer
# from django.contrib.auth.models import User

# class UserProfileDetail(generics.RetrieveAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile

# class UserProfileUpdate(generics.UpdateAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile

# profiles/views.py

# from rest_framework import generics, permissions
# from django.contrib.auth.models import User
# from .models import UserProfile
# from .serializers import UserSerializer

# class UserProfileAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

# myapp/views.py

from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserPreferences

from .serializers import UserSerializer
from .serializers import UserPreferencesSerializer
from .recommendation_algorithm import generate_recommendations
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        # Ensure user has a profile
        UserProfile.objects.get_or_create(user=user)
        return user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# class UserPreferencesAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserPreferencesSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         user_preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
#         return user_preferences

# class BrowsingHistoryAPIView(generics.ListCreateAPIView):
#     serializer_class = BrowsingHistorySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return BrowsingHistory.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class RecommendationsAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user_preferences = UserPreferences.objects.get(user=self.request.user)
#         browsing_history = BrowsingHistory.objects.filter(user=self.request.user)
        
#         # Generate recommendations based on user preferences and browsing history
#         recommended_items = generate_recommendations(user_preferences, browsing_history)
        
#         # Save recommendations in the database
#         recommendations = []
#         for item in recommended_items:
#             recommendation = Recommendation(
#                 user=self.request.user,
#                 item_id=item['item_id'],
#                 recommended_at=timezone.now(),
#                 score=item['score']
#             )
#             recommendation.save()
#             recommendations.append(recommendation)

#         serializer = RecommendationSerializer(recommendations, many=True)
#         return Response(serializer.data)

# class RecommendationsAPIView(generics.ListAPIView):
#     serializer_class = UserPreferencesSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user_preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
#         # For now, return the user preferences as the recommendation
#         return [user_preferences]

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

class RecommendationsAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
        recommendations = generate_recommendations(user_preferences)
        return Response({'recommendations': recommendations})

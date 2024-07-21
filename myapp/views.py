from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import (
    State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, 
    Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor, CustomUser,
    Banner, SavedFilter
)
from .serializers import (
    StateSerializer, DepartmentSerializer, OrganisationSerializer, SchemeSerializer, 
    BeneficiarySerializer, SchemeBeneficiarySerializer, BenefitSerializer, 
    CriteriaSerializer, ProcedureSerializer, DocumentSerializer, 
    SchemeDocumentSerializer, SponsorSerializer, SchemeSponsorSerializer, UserRegistrationSerializer,
    SaveSchemeSerializer, PersonalDetailSerializer, ProfessionalDetailSerializer, LoginSerializer, BannerSerializer, SavedFilterSerializer
)

from rest_framework.exceptions import NotFound
from .filters import CustomOrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken

class SchemePagination(PageNumberPagination):
    page_size_query_param = 'limit'


class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer 
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'state_name']
    ordering = ['-created_at']

class StateSchemesListAPIView(generics.ListAPIView):
    serializer_class = SchemeSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['introduced_on', 'title']
    ordering = ['-introduced_on']
    pagination_class = SchemePagination

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        if state_id:
            return Scheme.objects.filter(department__state_id=state_id)
        return Scheme.objects.none() 
    
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
    pagination_class = SchemePagination

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

from rest_framework import generics, permissions
from django.contrib.auth.models import User
# from .models import UserProfile


# from .serializers import UserSerializer
# from .serializers import UserPreferencesSerializer
from .recommendation_algorithm import generate_recommendations
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

# class UserProfileAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         user = self.request.user
#         # Ensure user has a profile
#         UserProfile.objects.get_or_create(user=user)
#         return user

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)


# class RecommendationsAPIView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return UserPreferences.objects.filter(user=self.request.user)

#     def get(self, request, *args, **kwargs):
#         user_preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
#         recommendations = generate_recommendations(user_preferences)
#         return Response({'recommendations': recommendations})

# Views from origin/main branch
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserRegistrationSerializer(user).data,
                "message": "User created successfully",
                "username": user.username
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PersonalDetailUpdateView(generics.UpdateAPIView):
    serializer_class = PersonalDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfessionalDetailUpdateView(generics.UpdateAPIView):
    serializer_class = ProfessionalDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user




class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=HTTP_200_OK)
        except KeyError:
            return Response({"error": "Refresh token not provided."}, status=HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={"message": "This is a protected view."}, status=HTTP_200_OK)


class SchemeSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            schemes = Scheme.objects.filter(title__icontains=query)
            serializer = SchemeSerializer(schemes, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response({"detail": "Query parameter 'q' is required."}, status=HTTP_400_BAD_REQUEST)



class SaveSchemeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user = request.user
        scheme_id = request.data.get('scheme_id', None)

        if scheme_id is None:
            return Response({"detail": "Scheme ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the scheme to the user's saved_schemes
        user.saved_schemes.add(scheme_id)
        user.save()

        return Response({'status': 'scheme saved'}, status=status.HTTP_200_OK)
    
class UserSavedSchemesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        saved_schemes = user.saved_schemes.all()
        serializer = SchemeSerializer(saved_schemes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UnsaveSchemeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        scheme_ids = request.data.get('scheme_ids', [])

        if not isinstance(scheme_ids, list):
            return Response({'error': 'scheme_ids must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        removed_schemes = []
        for scheme_id in scheme_ids:
            try:
                scheme = Scheme.objects.get(id=scheme_id)
                if scheme in user.saved_schemes.all():
                    user.saved_schemes.remove(scheme)
                    removed_schemes.append(scheme)
                else:
                    print(f"Scheme with id {scheme_id} is not saved by user {user.username}")
            except Scheme.DoesNotExist:
                print(f"Scheme with id {scheme_id} does not exist")
                return Response({'error': f'Scheme with id {scheme_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        print(f"User {user.username} unsaved schemes: {[scheme.id for scheme in removed_schemes]}")
        return Response({'status': 'Schemes unsaved successfully', 'removed_schemes': SchemeSerializer(removed_schemes, many=True).data}, status=status.HTTP_200_OK)
    
# BANNER VIEW BELOW
    
class BannerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def post(self, request, *args, **kwargs):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BannerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class SavedFilterListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedFilterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedFilter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedFilterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedFilterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedFilter.objects.filter(user=self.request.user)
    

# choices views below
    

class GenderChoicesView(APIView):
    def get(self, request):
        return Response(CustomUser._meta.get_field('gender').choices, status=status.HTTP_200_OK)

class StateChoicesView(APIView):
    def get(self, request):
        return Response(CustomUser._meta.get_field('state_of_residence').choices, status=status.HTTP_200_OK)

class EducationChoicesView(APIView):
    def get(self, request):
        return Response(CustomUser._meta.get_field('education').choices, status=status.HTTP_200_OK)

class CategoryChoicesView(APIView):
    def get(self, request):
        return Response(CustomUser._meta.get_field('category').choices, status=status.HTTP_200_OK)



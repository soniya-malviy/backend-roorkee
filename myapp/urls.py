from django.urls import path
from . import views

urlpatterns = [
    path('states/', views.StateListAPIView.as_view(), name='state-list'),
    path('departments/', views.DepartmentListAPIView.as_view(), name='department-list'),
    path('organisations/', views.OrganisationListAPIView.as_view(), name='organisation-list'),
    path('schemes/', views.SchemeListAPIView.as_view(), name='scheme-list'),
    path('schemes/<int:pk>/', views.SchemeDetailAPIView.as_view(), name='scheme-detail'),
    path('beneficiaries/', views.BeneficiaryListAPIView.as_view(), name='beneficiary-list'),
    path('scheme-beneficiaries/', views.SchemeBeneficiaryListAPIView.as_view(), name='scheme-beneficiary-list'),
    path('benefits/', views.BenefitListAPIView.as_view(), name='benefit-list'),
    path('criteria/', views.CriteriaListAPIView.as_view(), name='criteria-list'),
    path('procedures/', views.ProcedureListAPIView.as_view(), name='procedure-list'),
    path('documents/', views.DocumentListAPIView.as_view(), name='document-list'),
    path('scheme-documents/', views.SchemeDocumentListAPIView.as_view(), name='scheme-document-list'),
    path('sponsors/', views.SponsorListAPIView.as_view(), name='sponsor-list'),
    path('scheme-sponsors/', views.SchemeSponsorListAPIView.as_view(), name='scheme-sponsor-list'),
]


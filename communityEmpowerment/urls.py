from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views


from .views import (
    StateListAPIView,
    StateDetailAPIView,
    DepartmentListAPIView,
    OrganisationListAPIView,
    SchemeListAPIView,
    SchemeDetailAPIView,
    BeneficiaryListAPIView,
    SchemeBeneficiaryListAPIView,
    CriteriaListAPIView,
    ProcedureListAPIView,
    DocumentListAPIView,
    SchemeDocumentListAPIView,
    SponsorListAPIView,
    SchemeSponsorListAPIView,
    StateDepartmentsListAPIView,
    DepartmentSchemesListAPIView,
    SchemeBeneficiariesListAPIView,
    SchemeCriteriaListAPIView,
    SchemeProceduresListAPIView,
    SchemeDocumentsListAPIView,
    SchemeSponsorsListAPIView,
    StateSchemesListAPIView,
    UserRegistrationAPIView,
    LoginView,
    LogoutView,
    ProtectedView,
    SchemeSearchView,
    SaveSchemeView,
    UserSavedSchemesView,
    UserProfileView,
    UnsaveSchemeView,
    BannerListCreateAPIView,
    BannerDetailAPIView,
    SavedFilterDetailView,
    SavedFilterListCreateView,
    GenderChoicesView,
    StateChoicesView,
    CategoryChoicesView,
    verify_email,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PreferenceView,
    ScholarshipSchemesListView,
    JobSchemesListView,
    SchemeBenefitListAPIView,
    SchemesByStatesAPIView,
    SchemesByStateAndDepartmentAPIView,
    SchemesByMultipleStatesAndDepartmentsAPIView,
    CurrentUserDetailView,
    ResendVerificationEmailView,
    # EmploymentChoicesView,
    UserSavedSchemesFilterView,
    SchemeReportViewSet,
    WebsiteFeedbackViewSet,
    RecommendSchemesAPIView,
    HybridRecommendationView,
    SaveSchemeInteractionView,
    ViewSchemeInteractionView,
    SchemeFeedbackCreateView,
    SchemeFeedbackListView,
    TrackEventView,
    AllProfileFieldsView,
    LayoutItemViewSet,
)


urlpatterns = [
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("states/", StateListAPIView.as_view(), name="state-list"),
    path("states/<int:pk>/", StateDetailAPIView.as_view(), name="state-detail"),
    path("departments/", DepartmentListAPIView.as_view(), name="department-list"),
    path("organisations/", OrganisationListAPIView.as_view(), name="organisation-list"),
    path("schemes/", SchemeListAPIView.as_view(), name="scheme-list"),
    path("schemes/<int:pk>/", SchemeDetailAPIView.as_view(), name="scheme-detail"),
    path(
        "schemes/scholarship/",
        ScholarshipSchemesListView.as_view(),
        name="scholarship-schemes",
    ),
    path("schemes/job/", JobSchemesListView.as_view(), name="job-schemes"),
    path("beneficiaries/", BeneficiaryListAPIView.as_view(), name="beneficiary-list"),
    path(
        "scheme-beneficiaries/",
        SchemeBeneficiaryListAPIView.as_view(),
        name="scheme-beneficiary-list",
    ),
    # path('benefits/', BenefitListAPIView.as_view(), name='benefit-list'),
    path("criteria/", CriteriaListAPIView.as_view(), name="criteria-list"),
    path("procedures/", ProcedureListAPIView.as_view(), name="procedure-list"),
    path("documents/", DocumentListAPIView.as_view(), name="document-list"),
    path(
        "scheme-documents/",
        SchemeDocumentListAPIView.as_view(),
        name="scheme-document-list",
    ),
    path("sponsors/", SponsorListAPIView.as_view(), name="sponsor-list"),
    path(
        "scheme-sponsors/",
        SchemeSponsorListAPIView.as_view(),
        name="scheme-sponsor-list",
    ),
    path(
        "states/<int:state_id>/departments/",
        StateDepartmentsListAPIView.as_view(),
        name="state-departments-list",
    ),  # Add the new URL pattern
    path(
        "departments/<int:department_id>/schemes/",
        DepartmentSchemesListAPIView.as_view(),
        name="department-schemes-list",
    ),  # Add the new URL pattern
    path(
        "schemes/<int:scheme_id>/beneficiaries/",
        SchemeBeneficiariesListAPIView.as_view(),
        name="scheme-beneficiaries-list",
    ),  # Add the new URL pattern
    path(
        "schemes/<int:scheme_id>/criteria/",
        SchemeCriteriaListAPIView.as_view(),
        name="scheme-criteria-list",
    ),  # Add the new URL pattern
    path(
        "schemes/<int:scheme_id>/procedures/",
        SchemeProceduresListAPIView.as_view(),
        name="scheme-procedures-list",
    ),  # Add the new URL pattern
    path(
        "schemes/<int:scheme_id>/documents/",
        SchemeDocumentsListAPIView.as_view(),
        name="scheme-documents-list",
    ),  # Add the new URL pattern
    path(
        "schemes/<int:scheme_id>/sponsors/",
        SchemeSponsorsListAPIView.as_view(),
        name="scheme-sponsors-list",
    ),  # Add the new URL pattern
    path(
        "states/<int:state_id>/schemes/",
        StateSchemesListAPIView.as_view(),
        name="state-schemes-list",
    ),
    path("user/profile/", UserProfileView.as_view(), name="user-profile"),
    path("user/preferences/", PreferenceView.as_view(), name="user-preferences"),
    # path('recommendations/', RecommendationsAPIView.as_view(), name='recommendations'),
    path("register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path("verify-email/<uidb64>/<token>/", verify_email, name="verify_email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("schemes/search/", SchemeSearchView.as_view(), name="scheme-search"),
    path("save_scheme/", SaveSchemeView.as_view(), name="save_scheme"),
    path("unsave_scheme/", UnsaveSchemeView.as_view(), name="unsave-scheme"),
    path(
        "user/saved_schemes/", UserSavedSchemesView.as_view(), name="user-saved-schemes"
    ),
    path("banners/", BannerListCreateAPIView.as_view(), name="banner-list-create"),
    path("banners/<int:pk>/", BannerDetailAPIView.as_view(), name="banner-detail"),
    path(
        "saved_filters/",
        SavedFilterListCreateView.as_view(),
        name="saved_filter_list_create",
    ),
    path(
        "saved_filters/<int:pk>/",
        SavedFilterDetailView.as_view(),
        name="saved_filter_detail",
    ),
    path("choices/gender/", GenderChoicesView.as_view(), name="gender-choices"),
    path("choices/state/", StateChoicesView.as_view(), name="state-choices"),
    # path('choices/education/', EducationChoicesView.as_view(), name='education-choices'),
    path("choices/category/", CategoryChoicesView.as_view(), name="category-choices"),
    # path('choices/employment/', EmploymentChoicesView.as_view(), name='employment-choices'),
    # path('choices/disability/', DisabilityChoicesView.as_view(), name='disability-choices'),
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "schemes/<int:scheme_id>/benefits/",
        SchemeBenefitListAPIView.as_view(),
        name="scheme-benefits",
    ),
    path(
        "schemes/by-states/", SchemesByStatesAPIView.as_view(), name="schemes-by-states"
    ),
    path(
        "schemes/by-state-and-department/",
        SchemesByStateAndDepartmentAPIView.as_view(),
        name="schemes-by-state-and-department",
    ),
    path(
        "schemes/multi-state-departments/",
        SchemesByMultipleStatesAndDepartmentsAPIView.as_view(),
        name="schemes-by-multiple-state-and-department",
    ),
    path("user/me/", CurrentUserDetailView.as_view(), name="current-user-detail"),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path(
        "saved-schemes/filter/",
        UserSavedSchemesFilterView.as_view(),
        name="user-saved-schemes-filter",
    ),
    path(
        "feedback/scheme-reports/",
        SchemeReportViewSet.as_view({"post": "create", "get": "list"}),
        name="scheme-reports",
    ),
    path(
        "feedback/scheme-reports/<int:pk>/",
        SchemeReportViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="scheme-report-detail",
    ),
    path(
        "feedback/website-feedback/",
        WebsiteFeedbackViewSet.as_view({"post": "create", "get": "list"}),
        name="website-feedback",
    ),
    path(
        "feedback/website-feedback/<int:pk>/",
        WebsiteFeedbackViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="website-feedback-detail",
    ),
    path(
        "scheme/<int:scheme_id>/recommendations/",
        RecommendSchemesAPIView.as_view(),
        name="scheme_recommendations",
    ),
    path(
        "recommendations/",
        HybridRecommendationView.as_view(),
        name="hybrid-recommendations",
    ),
    path(
        "schemes/<int:scheme_id>/save/",
        SaveSchemeInteractionView.as_view(),
        name="save-scheme",
    ),
    path(
        "schemes/<int:scheme_id>/view/",
        ViewSchemeInteractionView.as_view(),
        name="view-scheme-interaction",
    ),
    path(
        "schemes/<int:scheme_id>/feedback/",
        SchemeFeedbackListView.as_view(),
        name="scheme-feedback-list",
    ),
    path(
        "feedback/create/",
        SchemeFeedbackCreateView.as_view(),
        name="scheme-feedback-create",
    ),
    path("track-event/", TrackEventView.as_view(), name="track_event"),
    path("dynamic-fields/", AllProfileFieldsView.as_view(), name="all_dynamic_fields"),
    path(
        "layout-items/",
        LayoutItemViewSet.as_view({"get": "list"}),
        name="layout-items-list",
    ),
    path(
        "layout-items/update-order/",
        LayoutItemViewSet.as_view({"post": "update_order"}),
        name="layout-items-update",
    ),
]

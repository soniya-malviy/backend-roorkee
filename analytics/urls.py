from django.urls import path
from .views import AnalyticsLoginView, analytics_dashboard

urlpatterns = [
    path("login/", AnalyticsLoginView.as_view(), name="analytics-login"),
    path("", analytics_dashboard, name="analytics-dashboard"),
]

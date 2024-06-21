from django.urls import path
from .views import SchemeAPIView, CriteriaAPIView, SponsorAPIView, SchemeDetailAPIView

urlpatterns = [
    path('schemes/', SchemeAPIView.as_view(), name='scheme'),
    path('schemes/<int:pk>/', SchemeDetailAPIView.as_view(), name='scheme-detail'),
    path('criteria/', CriteriaAPIView.as_view(), name='criteria'),
    path('sponsors/', SponsorAPIView.as_view(), name='sponsor'),
]

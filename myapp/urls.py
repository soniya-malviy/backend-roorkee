from django.urls import path
from .views import SchemeAPIView, CriteriaAPIView, SponsorAPIView

urlpatterns = [
    path('schemes/', SchemeAPIView.as_view(), name='scheme'),
    path('criteria/', CriteriaAPIView.as_view(), name='criteria'),
    path('sponsors/', SponsorAPIView.as_view(), name='sponsor'),
]

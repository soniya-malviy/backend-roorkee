from django.urls import path
from .views import SchemeAPIView

urlpatterns = [
    path('schemes/', SchemeAPIView.as_view(), name='scheme'),
]

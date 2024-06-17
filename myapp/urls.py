from django.urls import path
from .views import SchemeAPIView

urlpatterns = [
    path('', SchemeAPIView.as_view(), name='scheme'),
]

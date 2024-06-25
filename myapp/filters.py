from rest_framework.filters import OrderingFilter

class CustomOrderingFilter(OrderingFilter):
    ordering_param = 'sorting'

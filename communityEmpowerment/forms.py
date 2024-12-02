from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'gender', 'age', 'occupation', 'income', 'education', 'employment_status', 'government_employee', 'category', 'minority', 'state_of_residence', 'disability', 'bpl_card_holder', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'gender', 'age', 'occupation', 'income', 'education', 'employment_status', 'government_employee', 'category', 'minority', 'state_of_residence', 'disability', 'bpl_card_holder', 'is_staff', 'is_superuser')

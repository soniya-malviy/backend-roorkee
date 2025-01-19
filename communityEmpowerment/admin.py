from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary,
    Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, ProfileField, ProfileFieldChoice, ProfileFieldValue, CustomUser,
    SchemeSponsor, CustomUser, Banner, Tag, SchemeReport, WebsiteFeedback, SchemeFeedback,
)
# from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.site_header = "Community Empowerment Portal Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to your Admin Panel"

admin.site.register(State)
admin.site.register(Tag)
admin.site.register(Department)
admin.site.register(Organisation)
admin.site.register(SchemeBeneficiary)
admin.site.register(Benefit)
admin.site.register(Criteria)
admin.site.register(Procedure)
admin.site.register(SchemeDocument)
admin.site.register(SchemeSponsor)

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
#         ),
#     )
#     readonly_fields = ('date_joined',)
#     search_fields = ('username', 'email')
#     ordering = ('username',)

# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin):
    list_display = ['title', 'is_active']
    search_fields = ['title']

class SchemeResource(resources.ModelResource):
    class Meta:
        model = Scheme
        fields = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')
        export_order = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')

@admin.register(Scheme)
class SchemeAdmin(ImportExportModelAdmin):
    resource_class = SchemeResource
    list_display = ('title', 'department', 'introduced_on', 'valid_upto', 'funding_pattern')
    search_fields = ('title', 'description')
    list_filter = ('department', 'introduced_on', 'valid_upto', 'funding_pattern')

@admin.register(SchemeReport)
class SchemeReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'scheme_id', 'created_at'] 
    list_filter = ['created_at'] 

@admin.register(WebsiteFeedback)
class WebsiteFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'created_at'] 
    list_filter = ['created_at']

@admin.register(SchemeFeedback)
class SchemeFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheme', 'feedback', 'rating', 'created_at')
    search_fields = ('user__username', 'scheme__title', 'feedback')
    list_filter = ('created_at', 'rating')
    
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('category', 'name', 'is_active')
#     list_filter = ('category', 'is_active')  # Filter by category
#     search_fields = ('name',)
    
class ProfileFieldChoiceInline(admin.TabularInline):
    model = ProfileFieldChoice
    extra = 1


@admin.register(ProfileField)
class ProfileFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_required', 'is_active', 'placeholder')
    list_filter = ('field_type', 'is_active')
    inlines = [ProfileFieldChoiceInline]


@admin.register(ProfileFieldValue)
class ProfileFieldValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'value')
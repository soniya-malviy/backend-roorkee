from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group, Permission
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
#     list_filter = ('is_staff', 'is_active','groups')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','user_permissions', 'groups')}),
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



admin.site.register(Permission)

    
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('category', 'name', 'is_active')
#     list_filter = ('category', 'is_active')  # Filter by category
#     search_fields = ('name',)
    
class ProfileFieldChoiceInline(admin.TabularInline):
    model = ProfileFieldChoice
    extra = 0
    fields = ('value', 'is_active')
    readonly_fields = ('value',)
    can_delete = False
    def has_add_permission(self, request, obj=None):
        """Prevent adding new choices inline."""
        return False


@admin.register(ProfileField)
class ProfileFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_active','position',)
    list_filter = ['is_active', 'field_type']
    list_editable = ['is_active', 'position']
    readonly_fields = ['name', 'field_type', 'placeholder', 'min_value', 'max_value']
    inlines = [ProfileFieldChoiceInline]
    def has_add_permission(self, request):
        """Disallow adding new fields."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deleting fields."""
        return False

@admin.register(ProfileFieldValue)
class ProfileFieldValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'value')

class ProfileFieldInline(admin.TabularInline):
    model = ProfileFieldValue
    extra = 0
    readonly_fields = ('field', 'value') 

    def has_add_permission(self, request, obj):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_email_verified')
    list_filter = ('is_active', 'is_staff', 'is_email_verified')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ['name']}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ['last_login']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    inlines = [ProfileFieldInline]



admin.site.register(CustomUser, CustomUserAdmin)
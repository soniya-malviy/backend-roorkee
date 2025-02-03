from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_celery_beat.models import (ClockedSchedule, CrontabSchedule, 
IntervalSchedule, PeriodicTask, SolarSchedule)
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken, OutstandingToken)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, Permission

from .models import (
    State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, 
    Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, ProfileField, ProfileFieldChoice, ProfileFieldValue, CustomUser, SchemeSponsor, Banner, Tag, SchemeReport, WebsiteFeedback, SchemeFeedback
)



# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = "Community Empowerment Portal Admin Panel"
    site_title = "Admin Portal"
    index_title = "Welcome to your Admin Panel"

    def get_app_list(self, request,app_label="None"):
        app_dict = self._build_app_dict(request)
        app_list = [
            {
                'name': 'Access Management',
                'app_label': 'auth',
                'models': [
                    {'name': 'Users', 'object_name': 'CustomUser', 'admin_url': '/admin/communityEmpowerment/customuser/'},
                    {'name': 'Groups', 'object_name': 'Group', 'admin_url': '/admin/auth/group/'},
                    {'name': 'Permissions', 'object_name': 'Permission', 'admin_url': '/admin/auth/permission/'},
                ]
            },
            {
                'name': 'Layouts',
                'app_label': 'layouts',
                'models': [
                    {'name': 'Profile Fields', 'object_name': 'ProfileField', 'admin_url': '/admin/communityEmpowerment/profilefield/'},
                    {'name': 'Profile Field Values', 'object_name': 'ProfileFieldValue', 'admin_url': '/admin/communityEmpowerment/profilefieldvalue/'},
                ]
            },
            {
                'name': 'All Schemes',
                'app_label': 'schemes',
                'models': [
                    {'name': 'Schemes', 'object_name': 'Scheme', 'admin_url': '/admin/communityEmpowerment/scheme/'},
                    {'name': 'Benefits', 'object_name': 'Benefit', 'admin_url': '/admin/communityEmpowerment/benefit/'},
                    {'name': 'Criteria', 'object_name': 'Criteria', 'admin_url': '/admin/communityEmpowerment/criteria/'},
                    {'name': 'Departments', 'object_name': 'Department', 'admin_url': '/admin/communityEmpowerment/department/'},
                    {'name': 'Organizations', 'object_name': 'Organisation', 'admin_url': '/admin/communityEmpowerment/organisation/'},
                    {'name': 'Procedures', 'object_name': 'Procedure', 'admin_url': '/admin/communityEmpowerment/procedure/'},
                    {'name': 'Scheme Beneficiaries', 'object_name': 'SchemeBeneficiary', 'admin_url': '/admin/communityEmpowerment/schemebeneficiary/'},
                    {'name': 'Scheme Documents', 'object_name': 'SchemeDocument', 'admin_url': '/admin/communityEmpowerment/schemedocument/'},
                    {'name': 'Scheme Sponsors', 'object_name': 'SchemeSponsor', 'admin_url': '/admin/communityEmpowerment/schemesponsor/'},
                    {'name': 'States', 'object_name': 'State', 'admin_url': '/admin/communityEmpowerment/state/'},
                    {'name': 'Tags', 'object_name': 'Tag', 'admin_url': '/admin/communityEmpowerment/tag/'},
                ]
            },
            {
                'name': 'Feedback & Reports',
                'app_label': 'feedback',
                'models': [
                    {'name': 'Scheme Feedbacks', 'object_name': 'SchemeFeedback', 'admin_url': '/admin/communityEmpowerment/schemefeedback/'},
                    {'name': 'Scheme Reports', 'object_name': 'SchemeReport', 'admin_url': '/admin/communityEmpowerment/schemereport/'},
                    {'name': 'Website Feedbacks', 'object_name': 'WebsiteFeedback', 'admin_url': '/admin/communityEmpowerment/websitefeedback/'},
                ]
            },
            {
                'name': 'Assets',
                'app_label': 'assets',
                'models': [
                    {'name': 'Banners', 'object_name': 'Banner', 'admin_url': '/admin/communityEmpowerment/banner/'},
                ]
            },
            {
                'name': 'Periodic Tasks',
                'app_label': 'Periodic Tasks',
                'models': [
                    {'name': 'Clocked', 'object_name': 'Clocked', 'admin_url': '/admin/django_celery_beat/clockedschedule/'},
                    {'name': 'Crontabs', 'object_name': 'Crontabs', 'admin_url': '/admin/django_celery_beat/crontabschedule/'},
                    {'name': 'Intervals', 'object_name': 'Intervals', 'admin_url': '/admin/django_celery_beat/intervalschedule/'},
                    {'name': 'Periodic tasks', 'object_name': 'Periodic tasks', 'admin_url': '/admin/django_celery_beat/periodictask/'},
                    {'name': 'Solar events', 'object_name': 'Solar events', 'admin_url': '/admin/django_celery_beat/solarschedule/'}
                ]
            },
            {
                'name': 'Token Blacklist',
                'app_label': 'Token Blacklist',
                'models': [
                    {'name': 'Blacklisted tokens', 'object_name': 'Blacklisted tokens', 'admin_url': '/admin/token_blacklist/blacklistedtoken/'},
                    {'name': 'Outstanding tokens', 'object_name': 'Outstanding tokens', 'admin_url': '/admin/token_blacklist/outstandingtoken/'}
                ]
            },
        ]

        # Sort the models inside each app by 'name'
        for app in app_list:
            app['models'] = sorted(app['models'], key=lambda model: model['name'])

        # Sort the app list by 'name'
        sorted_app_list = sorted(app_list, key=lambda app: app['name'])

        return sorted_app_list
        
# Create custom admin instance
admin_site = CustomAdminSite(name='admin')

class CustomGroupAdmin(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name','permissions')}),
    )
    list_display = ('name',) 
    search_fields = ('name',) 
    list_filter = ('name',) 

admin_site.register(Group, CustomGroupAdmin)




class BannerAdmin(ImportExportModelAdmin):
    list_display = ['title', 'is_active']
    search_fields = ['title']
admin_site.register(Banner)

class SchemeResource(resources.ModelResource):
    class Meta:
        model = Scheme
        fields = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')
        export_order = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')


class SchemeAdmin(ImportExportModelAdmin):
    resource_class = SchemeResource
    list_display = ('title', 'department', 'introduced_on', 'valid_upto', 'funding_pattern')
    search_fields = ('title', 'description')
    list_filter = ('department', 'introduced_on', 'valid_upto', 'funding_pattern')
admin_site.register(Scheme)

class SchemeReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'scheme_id', 'created_at'] 
    list_filter = ['created_at'] 
admin_site.register(SchemeReport)

class WebsiteFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'created_at'] 
    list_filter = ['created_at']
admin_site.register(WebsiteFeedback)

class SchemeFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheme', 'feedback', 'rating', 'created_at')
    search_fields = ('user__username', 'scheme__title', 'feedback')
    list_filter = ('created_at', 'rating')
admin_site.register(SchemeFeedback)


admin_site.register(Permission)
    
class ProfileFieldChoiceInline(admin.TabularInline):
    model = ProfileFieldChoice
    extra = 0
    fields = ('value', 'is_active')
    readonly_fields = ('value',)
    can_delete = False
    def has_add_permission(self, request, obj=None):
        """Prevent adding new choices inline."""
        return False

admin_site.register(ProfileField)

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


class ProfileFieldValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'value')

admin_site.register(ProfileFieldValue)

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
    list_filter = ('is_active', 'is_staff', 'is_email_verified','groups')
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



admin_site.register(CustomUser, CustomUserAdmin)


admin_site.register(State)
admin_site.register(Tag)
admin_site.register(Department)
admin_site.register(Organisation)
admin_site.register(SchemeBeneficiary)
admin_site.register(Benefit)
admin_site.register(Criteria)
admin_site.register(Procedure)
admin_site.register(SchemeDocument)
admin_site.register(SchemeSponsor)

admin_site.register(ClockedSchedule)
admin_site.register(CrontabSchedule)
admin_site.register(IntervalSchedule)
admin_site.register(PeriodicTask)
admin_site.register(SolarSchedule)

admin_site.register(BlacklistedToken)
admin_site.register(OutstandingToken)

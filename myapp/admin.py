from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Scheme, Criteria, Sponsor, SchemeDetail

admin.site.register(Scheme)
admin.site.register(SchemeDetail)
admin.site.register(Criteria)
admin.site.register(Sponsor)

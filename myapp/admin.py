from django.contrib import admin
from .models import State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, SchemeSponsor

admin.site.register(State)
admin.site.register(Department)
admin.site.register(Organisation)
admin.site.register(Scheme)
admin.site.register(Beneficiary)
admin.site.register(SchemeBeneficiary)
admin.site.register(Benefit)
admin.site.register(Criteria)
admin.site.register(Procedure)
admin.site.register(Document)
admin.site.register(SchemeDocument)
admin.site.register(Sponsor)
admin.site.register(SchemeSponsor)

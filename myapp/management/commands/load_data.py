# import json
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure

# class Command(BaseCommand):
#     help = 'Load data from JSON file into database'

#     def handle(self, *args, **kwargs):
#         with open('myapp/combined_schemes_data.json', 'r') as file:
#             data = json.load(file)
#             self.load_data(data)
        
#         self.stdout.write(self.style.SUCCESS('Successfully loaded data into database'))

                        
#     def load_data(self, data):
#         for state_data in data['states']:
#             state, created = State.objects.get_or_create(
#                 state_name=state_data['state_name']
#             )

#             for department_data in state_data['departments']:
#                 department, created = Department.objects.get_or_create(
#                     state=state,
#                     department_name=department_data['department_name']
#                 )

#                 for organisation_data in department_data['organisations']:
#                     organisation, created = Organisation.objects.get_or_create(
#                         department=department,
#                         organisation_name=organisation_data['organisation_name']
#                     )

#                     for scheme_data in organisation_data['schemes']:
#                         scheme, created = Scheme.objects.get_or_create(
#                             title=scheme_data['title'],
#                             department=department,
#                             defaults={
#                                 'introduced_on': scheme_data.get('introduced_on'),
#                                 'valid_upto': scheme_data.get('valid_upto'),
#                                 'funding_pattern': scheme_data.get('funding_pattern', 'State'),
#                                 'description': scheme_data.get('description'),
#                                 'scheme_link': scheme_data.get('scheme_link')
#                             }
#                         )
#                         if not created:
#                             scheme.introduced_on = scheme_data.get('introduced_on')
#                             scheme.valid_upto = scheme_data.get('valid_upto')
#                             scheme.funding_pattern = scheme_data.get('funding_pattern', 'State')
#                             scheme.description = scheme_data.get('description')
#                             scheme.scheme_link = scheme_data.get('scheme_link')
#                             scheme.save()

#                         for beneficiary_data in scheme_data['beneficiaries']:
#                             beneficiary, created = Beneficiary.objects.get_or_create(
#                                 beneficiary_type=beneficiary_data['beneficiary_type']
#                             )
#                             SchemeBeneficiary.objects.get_or_create(
#                                 scheme=scheme,
#                                 beneficiary=beneficiary
#                             )

#                         for document_data in scheme_data['documents']:
#                             document, created = Document.objects.get_or_create(
#                                 document_name=document_data['document_name']
#                             )
#                             SchemeDocument.objects.get_or_create(
#                                 scheme=scheme,
#                                 document=document
#                             )

#                         for sponsor_data in scheme_data['sponsors']:
#                             sponsor, created = Sponsor.objects.get_or_create(
#                                 sponsor_type=sponsor_data['sponsor_type']
#                             )
#                             SchemeSponsor.objects.get_or_create(
#                                 scheme=scheme,
#                                 sponsor=sponsor
#                             )

#                         for criteria_data in scheme_data['criteria']:
#                             Criteria.objects.update_or_create(
#                                 scheme=scheme,
#                                 description=criteria_data['description'],
#                                 defaults={
#                                     'value': criteria_data.get('value')
#                                 }
#                             )

#                         for procedure_data in scheme_data['procedures']:
#                             Procedure.objects.update_or_create(
#                                 scheme=scheme,
#                                 step_description=procedure_data['step_description']
#                             )

# import json
# from django.core.management.base import BaseCommand
# from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure

# class Command(BaseCommand):
#     help = 'Load data from JSON file into database'

#     def handle(self, *args, **kwargs):
#         with open('myapp/combined_schemes_data.json', 'r') as file:
#             data = json.load(file)
#             self.load_data(data)
        
#         self.stdout.write(self.style.SUCCESS('Successfully loaded data into database'))

#     def load_data(self, data):
#         for state_data in data['states']:
#             state, created = State.objects.get_or_create(
#                 state_name=state_data['state_name']
#             )
#             print(f"Processing State: {state_data['state_name']}")

#             for department_data in state_data['departments']:
#                 department, created = Department.objects.get_or_create(
#                     state=state,
#                     department_name=department_data['department_name']
#                 )
#                 print(f"Processing Department: {department_data['department_name']}")

#                 for organisation_data in department_data['organisations']:
#                     organisation, created = Organisation.objects.get_or_create(
#                         department=department,
#                         organisation_name=organisation_data['organisation_name']
#                     )
#                     print(f"Processing Organisation: {organisation_data['organisation_name']}")

#                     for scheme_data in organisation_data['schemes']:
#                         scheme, created = Scheme.objects.get_or_create(
#                             title=scheme_data['title'],
#                             department=department,
#                             defaults={
#                                 'introduced_on': scheme_data.get('introduced_on'),
#                                 'valid_upto': scheme_data.get('valid_upto'),
#                                 'funding_pattern': scheme_data.get('funding_pattern', 'State'),
#                                 'description': scheme_data.get('description'),
#                                 'scheme_link': scheme_data.get('scheme_link')
#                             }
#                         )
#                         if not created:
#                             scheme.introduced_on = scheme_data.get('introduced_on')
#                             scheme.valid_upto = scheme_data.get('valid_upto')
#                             scheme.funding_pattern = scheme_data.get('funding_pattern', 'State')
#                             scheme.description = scheme_data.get('description')
#                             scheme.scheme_link = scheme_data.get('scheme_link')
#                             scheme.save()

#                         print(f"Processing Scheme: {scheme_data['title']}")

#                         for beneficiary_data in scheme_data.get('beneficiaries', []):
#                             beneficiary, created = Beneficiary.objects.get_or_create(
#                                 beneficiary_type=beneficiary_data['beneficiary_type']
#                             )
#                             SchemeBeneficiary.objects.get_or_create(
#                                 scheme=scheme,
#                                 beneficiary=beneficiary
#                             )

#                         documents = scheme_data.get('documents', [])
#                         if documents:
#                             for document_data in documents:
#                                 document_name = document_data.get('document_name', 'Unknown Document')
#                                 document_type = document_data.get('document_type', 'Unknown Type')
#                                 document, created = Document.objects.get_or_create(
#                                     document_name=document_name,
#                                     defaults={'document_type': document_type}
#                                 )
#                                 SchemeDocument.objects.get_or_create(
#                                     scheme=scheme,
#                                     document=document
#                                 )
#                         else:
#                             print(f"No documents for scheme: {scheme_data['title']}")

#                         for sponsor_data in scheme_data.get('sponsors', []):
#                             sponsor, created = Sponsor.objects.get_or_create(
#                                 sponsor_type=sponsor_data['sponsor_type']
#                             )
#                             SchemeSponsor.objects.get_or_create(
#                                 scheme=scheme,
#                                 sponsor=sponsor
#                             )

#                         for criteria_data in scheme_data.get('criteria', []):
#                             Criteria.objects.update_or_create(
#                                 scheme=scheme,
#                                 description=criteria_data['description'],
#                                 defaults={'value': criteria_data.get('value')}
#                             )

#                         for procedure_data in scheme_data.get('procedures', []):
#                             Procedure.objects.update_or_create(
#                                 scheme=scheme,
#                                 step_description=procedure_data['step_description']
#                             )




# import json
# from django.utils.dateparse import parse_datetime
# from django.core.management.base import BaseCommand
# from myapp.models import (
#     State, Department, Organisation, Scheme, Beneficiary, 
#     SchemeBeneficiary, Document, SchemeDocument, Sponsor, SchemeSponsor, Criteria, Procedure
# )

# class Command(BaseCommand):
#     help = 'Load combined_schemes_data.json into the database'

#     def handle(self, *args, **kwargs):
#         with open('myapp/combined_schemes_data.json', 'r') as file:
#             data = json.load(file)
        
#         for state_data in data['states']:
#             state, created = State.objects.get_or_create(
#                 state_name=state_data['state_name']
#             )

#             for dept_data in state_data['departments']:
#                 department, created = Department.objects.get_or_create(
#                     state=state,
#                     department_name=dept_data['department_name']
#                 )

#                 for org_data in dept_data['organisations']:
#                     organisation, created = Organisation.objects.get_or_create(
#                         department=department,
#                         organisation_name=org_data['organisation_name']
#                     )

#                     for scheme_data in org_data['schemes']:
#                         scheme, created = Scheme.objects.get_or_create(
#                             title=scheme_data['title'],
#                             department=department,
#                             defaults={
#                                 'introduced_on': parse_datetime(scheme_data['introduced_on']),
#                                 'valid_upto': parse_datetime(scheme_data['valid_upto']),
#                                 'funding_pattern': scheme_data['funding_pattern'],
#                                 'description': scheme_data['description'],
#                                 'scheme_link': scheme_data['scheme_link']
#                             }
#                         )

#                         for beneficiary_data in scheme_data['beneficiaries']:
#                             beneficiary, created = Beneficiary.objects.get_or_create(
#                                 beneficiary_type=beneficiary_data['beneficiary_type']
#                             )
#                             SchemeBeneficiary.objects.get_or_create(
#                                 scheme=scheme,
#                                 beneficiary=beneficiary
#                             )

#                         for document_data in scheme_data['documents']:
#                             document, created = Document.objects.get_or_create(
#                                 document_name=document_data['document_type']
#                             )
#                             SchemeDocument.objects.get_or_create(
#                                 scheme=scheme,
#                                 document=document
#                             )

#                         for sponsor_data in scheme_data['sponsors']:
#                             sponsor, created = Sponsor.objects.get_or_create(
#                                 sponsor_type=sponsor_data['sponsor_type']
#                             )
#                             SchemeSponsor.objects.get_or_create(
#                                 scheme=scheme,
#                                 sponsor=sponsor
#                             )

#                         for criteria_data in scheme_data['criteria']:
#                             Criteria.objects.get_or_create(
#                                 scheme=scheme,
#                                 description=criteria_data['description'],
#                                 value=criteria_data.get('value', '')
#                             )

#                         for procedure_data in scheme_data['procedures']:
#                             Procedure.objects.get_or_create(
#                                 scheme=scheme,
#                                 step_description=procedure_data['step_description']
#                             )

#         self.stdout.write(self.style.SUCCESS('Successfully loaded data into the database.'))


import json
from django.core.management.base import BaseCommand
from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure

class Command(BaseCommand):
    help = 'Load data from JSON file into database'

    def handle(self, *args, **kwargs):
        with open('myapp/combined_schemes_data.json', 'r') as file:
            data = json.load(file)
            self.load_data(data)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded data into database'))

    def load_data(self, data):
        for state_data in data['states']:
            state, created = State.objects.get_or_create(
                state_name=state_data['state_name']
            )

            for department_data in state_data['departments']:
                department, created = Department.objects.get_or_create(
                    state=state,
                    department_name=department_data['department_name']
                )

                for organisation_data in department_data['organisations']:
                    organisation, created = Organisation.objects.get_or_create(
                        department=department,
                        organisation_name=organisation_data['organisation_name']
                    )

                    for scheme_data in organisation_data['schemes']:
                        scheme, created = Scheme.objects.get_or_create(
                            title=scheme_data['title'],
                            department=department,
                            defaults={
                                'introduced_on': scheme_data.get('introduced_on'),
                                'valid_upto': scheme_data.get('valid_upto'),
                                'funding_pattern': scheme_data.get('funding_pattern', 'State'),
                                'description': scheme_data.get('description'),
                                'scheme_link': scheme_data.get('scheme_link')
                            }
                        )
                        if not created:
                            scheme.introduced_on = scheme_data.get('introduced_on')
                            scheme.valid_upto = scheme_data.get('valid_upto')
                            scheme.funding_pattern = scheme_data.get('funding_pattern', 'State')
                            scheme.description = scheme_data.get('description')
                            scheme.scheme_link = scheme_data.get('scheme_link')
                            scheme.save()

                        for beneficiary_data in scheme_data['beneficiaries']:
                            beneficiary, created = Beneficiary.objects.get_or_create(
                                beneficiary_type=beneficiary_data['beneficiary_type']
                            )
                            SchemeBeneficiary.objects.get_or_create(
                                scheme=scheme,
                                beneficiary=beneficiary
                            )

                        for document_data in scheme_data['documents']:
                            document, created = Document.objects.get_or_create(
                                document_name=document_data['document_name']
                            )
                            SchemeDocument.objects.get_or_create(
                                scheme=scheme,
                                document=document
                            )

                        for sponsor_data in scheme_data['sponsors']:
                            sponsor, created = Sponsor.objects.get_or_create(
                                sponsor_type=sponsor_data['sponsor_type']
                            )
                            SchemeSponsor.objects.get_or_create(
                                scheme=scheme,
                                sponsor=sponsor
                            )

                        for criteria_data in scheme_data['criteria']:
                            criteria, created = Criteria.objects.filter(
                                scheme=scheme,
                                description=criteria_data['description']
                            ).first(), False

                            if criteria:
                                criteria.value = criteria_data.get('value')
                                criteria.save()
                            else:
                                criteria = Criteria.objects.create(
                                    scheme=scheme,
                                    description=criteria_data['description'],
                                    value=criteria_data.get('value')
                                )

                        for procedure_data in scheme_data['procedures']:
                            Procedure.objects.update_or_create(
                                scheme=scheme,
                                step_description=procedure_data['step_description']
                            )

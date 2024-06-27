import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure

class Command(BaseCommand):
    help = 'Load data from JSON file into database'

    def handle(self, *args, **kwargs):
        with open('myapp/schemes.json', 'r') as file:
            data = json.load(file)
            self.load_data(data)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded data into database'))

    def load_data(self, data):
        for state_data in data['states']:
            state = State.objects.create(
                state_name=state_data['state_name']
            )
            
            for department_data in state_data['departments']:
                department = Department.objects.create(
                    state=state,
                    department_name=department_data['department_name']
                )
                
                for organisation_data in department_data['organisations']:
                    organisation = Organisation.objects.create(
                        department=department,
                        organisation_name=organisation_data['organisation_name']
                    )
                    
                    for scheme_data in organisation_data['schemes']:
                        scheme = Scheme.objects.create(
                            title=scheme_data['title'],
                            department=department,
                            introduced_on=scheme_data.get('introduced_on'),
                            valid_upto=scheme_data.get('valid_upto'),
                            funding_pattern=scheme_data.get('funding_pattern', 'State'),
                            description=scheme_data.get('description'),
                            scheme_link=scheme_data.get('scheme_link')
                        )
                        
                        for beneficiary_data in scheme_data['beneficiaries']:
                            beneficiary, created = Beneficiary.objects.get_or_create(
                                beneficiary_type=beneficiary_data['beneficiary_type']
                            )
                            SchemeBeneficiary.objects.create(
                                scheme=scheme,
                                beneficiary=beneficiary
                            )
                        
                        for document_data in scheme_data['documents']:
                            document, created = Document.objects.get_or_create(
                                document_name=document_data['document_name']
                            )
                            SchemeDocument.objects.create(
                                scheme=scheme,
                                document=document
                            )
                        
                        for sponsor_data in scheme_data['sponsors']:
                            sponsor, created = Sponsor.objects.get_or_create(
                                sponsor_type=sponsor_data['sponsor_type']
                            )
                            SchemeSponsor.objects.create(
                                scheme=scheme,
                                sponsor=sponsor
                            )
                        
                        for criteria_data in scheme_data['criteria']:
                            Criteria.objects.create(
                                scheme=scheme,
                                description=criteria_data['description'],
                                value=criteria_data.get('value')
                            )
                        
                        for procedure_data in scheme_data['procedures']:
                            Procedure.objects.create(
                                scheme=scheme,
                                step_description=procedure_data['step_description']
                            )

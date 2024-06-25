
# myapp/management/commands/import_data.py
import json
from django.core.management.base import BaseCommand
from myapp.models import State, Department, Scheme, Beneficiary, Sponsor, Procedure

class Command(BaseCommand):
    help = 'Import JSON data into the database'

    def handle(self, *args, **kwargs):
        with open('myapp/schemes.json', 'r') as file:
            data = json.load(file)
            for item in data:
                state_name = item['department']['state']['state_name']
                state, created = State.objects.get_or_create(state_name=state_name)

                department_name = item['department']['department_name']
                department, created = Department.objects.get_or_create(state=state, department_name=department_name)

                scheme = Scheme.objects.create(
                    title=item['title'],
                    department=department,
                    introduced_on=item.get('introduced_on'),
                    valid_upto=item.get('valid_upto'),
                    funding_pattern=item['funding_pattern'],
                    description=item['description'],
                    scheme_link=item['scheme_link']
                )

                for beneficiary_data in item['beneficiaries']:
                    beneficiary_type = beneficiary_data['beneficiary_type']
                    beneficiary, created = Beneficiary.objects.get_or_create(beneficiary_type=beneficiary_type)
                    scheme.beneficiaries.add(beneficiary)

                for sponsor_data in item['sponsors']:
                    sponsor_type = sponsor_data['sponsor_type']
                    sponsor, created = Sponsor.objects.get_or_create(sponsor_type=sponsor_type)
                    scheme.sponsors.add(sponsor)

                for procedure_data in item['procedures']:
                    Procedure.objects.create(
                        scheme=scheme,
                        step_description=procedure_data['step_description']
                    )

           

            self.stdout.write(self.style.SUCCESS('Successfully imported data'))

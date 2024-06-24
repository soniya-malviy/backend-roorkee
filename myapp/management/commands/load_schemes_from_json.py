import json
from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import Scheme
from myapp.models import SchemeDetail

class Command(BaseCommand):
    help = 'Load scheme data from JSON into database'

    def handle(self, *args, **kwargs):
        with open('myapp/schemes.json', 'r') as file:
            schemes = json.load(file)

        for scheme_data in schemes:
            try:
               

                scheme, created = Scheme.objects.update_or_create(
                    scheme_id=scheme_data['scheme_id'],
                    defaults={
                        'department': scheme_data['department'],
                        'scheme_name': scheme_data['scheme_name'],
                        'description': scheme_data['description'],
                        'beneficiaries': scheme_data['beneficiaries'],
                        'benefits': scheme_data['benefits'],
                        'how_to_avail': scheme_data['how_to_avail'],
                        'sponsors': scheme_data['sponsors'],
                        'lower_age': scheme_data['lower_age'],
                        'upper_age': scheme_data['upper_age'],
        

                        'category': scheme_data['category'],
                        'objective': scheme_data['objective'],
                        'funding_pattern': scheme_data['funding_pattern'],
                        'application_process': scheme_data['application_process'],
                        'contact_office': scheme_data['contact_office'],
                        'scheme_link': scheme_data['scheme_link'],
                        'required_documents': scheme_data['required_documents'],
                    }
                )
                scheme_detail, created = SchemeDetail.objects.update_or_create(
                    scheme=scheme,  # Associate with the corresponding Scheme instance
                    defaults={
                        'beneficiaries': scheme_data['beneficiaries'],
                        'benefits': scheme_data['benefits'],
                        'how_to_avail': scheme_data['how_to_avail'],
                        'category': scheme_data['category'],
                        'objective': scheme_data['objective'],
                        'funding_pattern': scheme_data['funding_pattern'],
                        'application_process': scheme_data['application_process'],
                        'contact_office': scheme_data['contact_office'],
                        'scheme_link': scheme_data['scheme_link'],
                        'required_documents': scheme_data['required_documents'],
                       
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added scheme: {scheme.scheme_name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated scheme: {scheme.scheme_name}'))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f'Invalid date format in scheme data: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving scheme: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded scheme data'))


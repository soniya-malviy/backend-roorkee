import json
from django.core.management.base import BaseCommand
from myapp.models import State, Department, Scheme, Beneficiary, Benefit, Criteria, Procedure, Document, Sponsor, SchemeSponsor, SchemeDocument
import subprocess
import os

class Command(BaseCommand):
    help = 'Scrape schemes data, send to Gemini API, and save to the database'

    def handle(self, *args, **kwargs):
        # Define the paths to the scripts
        puppeteer_script_path = os.path.join(os.path.dirname(__file__), '../../../scripts/puppeteer_script.js')
        gemini_api_script_path = os.path.join(os.path.dirname(__file__), 'process_gemini_api.py')
        gemini_api_output_path = os.path.join(os.path.dirname(__file__), 'gemini_processed_data.json')

        # Run the Puppeteer script
        subprocess.run(["node", puppeteer_script_path])

        # Run the Gemini API script
        subprocess.run(["python", gemini_api_script_path])

        # Load the processed data from the Gemini API output file
        with open(gemini_api_output_path) as f:
            processed_data = json.load(f)

        # Save the processed data to the database
        for data in processed_data:
            state, created = State.objects.get_or_create(state_name="Meghalaya")
            if not created:
                state = State.objects.filter(state_name="Meghalaya").first()
            
            department, _ = Department.objects.get_or_create(state=state, department_name=data['department'])
            
            scheme, created = Scheme.objects.get_or_create(
                title=data['scheme_name'],
                department=department,
                defaults={
                    'description': data['description'],
                    'scheme_link': data['scheme_link'],
                    'introduced_on': data['introduced_on'],
                    'funding_pattern': data['funding']
                }
            )

            # Add other related data like beneficiaries, sponsors, etc.
            if data['scheme_beneficiary']:
                beneficiary, _ = Beneficiary.objects.get_or_create(beneficiary_type=data['scheme_beneficiary'])
                scheme.beneficiaries.add(beneficiary)

            if data['sponsors']:
                sponsor, _ = Sponsor.objects.get_or_create(sponsor_type=data['sponsors'])
                SchemeSponsor.objects.get_or_create(scheme=scheme, sponsor=sponsor)

            # Handle scheme benefits
            if data['scheme_benefits']:
                benefit, _ = Benefit.objects.get_or_create(benefit_type=data['scheme_benefits'])
                scheme.benefits.add(benefit)

            # Handle criteria
            if data.get('criteria'):
                for crit in data['criteria']:
                    Criteria.objects.get_or_create(
                        scheme=scheme,
                        description=crit.get('description'),
                        defaults={'value': crit.get('value')}
                    )

            # Handle procedures
            if data.get('procedures'):
                for proc in data['procedures']:
                    Procedure.objects.get_or_create(
                        scheme=scheme,
                        step_description=proc.get('step_description')
                    )

            # Handle documents
            if data.get('documents'):
                for doc in data['documents']:
                    document, _ = Document.objects.get_or_create(document_name=doc)
                    SchemeDocument.objects.get_or_create(scheme=scheme, document=document)

        self.stdout.write(self.style.SUCCESS('Successfully scraped, processed, and saved schemes data'))
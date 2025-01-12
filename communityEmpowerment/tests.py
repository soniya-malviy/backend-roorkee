from django.test import TestCase
from django.utils.timezone import now
from .models import State, Department, Organisation, Scheme, Tag, Beneficiary, Benefit, Sponsor, Document

class StateModelTest(TestCase):
    def test_create_state(self):
        state = State.objects.create(state_name="Uttar Pradesh")
        self.assertEqual(state.state_name, "Uttar Pradesh")
        self.assertIsNotNone(state.created_at)

class DepartmentModelTest(TestCase):
    def test_department_group_classification(self):
        state = State.objects.create(state_name="Maharashtra")
        department = Department.objects.create(state=state, department_name="Health and Family Welfare")
        self.assertEqual(department.get_group(), "Health")

class OrganisationModelTest(TestCase):
    def test_create_organisation(self):
        state = State.objects.create(state_name="Karnataka")
        department = Department.objects.create(state=state, department_name="Education Department")
        organisation = Organisation.objects.create(department=department, organisation_name="State Education Board")
        self.assertEqual(organisation.organisation_name, "State Education Board")
        self.assertEqual(organisation.department.department_name, "Education Department")

class SchemeModelTest(TestCase):
    def test_create_scheme(self):
        state = State.objects.create(state_name="Tamil Nadu")
        department = Department.objects.create(state=state, department_name="Agriculture Department")
        scheme = Scheme.objects.create(
            title="Free Fertilizer Distribution",
            department=department,
            description="A scheme to provide free fertilizers to farmers.",
        )
        self.assertEqual(scheme.title, "Free Fertilizer Distribution")
        self.assertEqual(scheme.department.department_name, "Agriculture Department")
        self.assertIn("farmers", scheme.description)

class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Agriculture")
        self.assertEqual(tag.name, "Agriculture")

class BeneficiaryModelTest(TestCase):
    def test_create_beneficiary(self):
        beneficiary = Beneficiary.objects.create(beneficiary_type="Farmers")
        self.assertEqual(beneficiary.beneficiary_type, "Farmers")

class BenefitModelTest(TestCase):
    def test_create_benefit(self):
        benefit = Benefit.objects.create(benefit_type="Subsidy", description="50% subsidy on seeds")
        self.assertEqual(benefit.benefit_type, "Subsidy")
        self.assertEqual(benefit.description, "50% subsidy on seeds")

class SponsorModelTest(TestCase):
    def test_create_sponsor(self):
        sponsor = Sponsor.objects.create(sponsor_type="Government")
        self.assertEqual(sponsor.sponsor_type, "Government")

class DocumentModelTest(TestCase):
    def test_create_document(self):
        document = Document.objects.create(document_name="Aadhar Card", requirements="Valid Aadhar Number")
        self.assertEqual(document.document_name, "Aadhar Card")
        self.assertEqual(document.requirements, "Valid Aadhar Number")

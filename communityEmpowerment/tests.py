from django.test import TestCase
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from .models import State, Department, Organisation, Scheme, Tag, Beneficiary, Benefit, Sponsor, Document

class StateModelTest(TestCase):
    def test_create_state(self):
        state = State.objects.create(state_name="Uttar Pradesh")
        self.assertEqual(state.state_name, "Uttar Pradesh")
        self.assertIsNotNone(state.created_at)

    def test_empty_state_name(self):
        with self.assertRaises(ValidationError):
            state = State(state_name="")
            state.full_clean()  # Triggers validation
            state.save()

    def test_duplicate_state_name(self):
        State.objects.create(state_name="Uttar Pradesh")
        duplicate_state = State.objects.create(state_name="Uttar Pradesh")
        self.assertEqual(duplicate_state.state_name, "Uttar Pradesh")  # If duplicates are allowed

    def test_whitespace_in_state_name(self):
        state = State.objects.create(state_name="  Bihar  ")
        self.assertEqual(state.state_name, "Bihar")  # Ensure whitespace is stripped

    def test_state_name_exceeds_max_length(self):
        long_name = "A" * 256  # 256 characters
        with self.assertRaises(ValidationError):
            state = State(state_name=long_name)
            state.full_clean()

    def test_null_state_name(self):
        with self.assertRaises(ValueError):  # Django raises ValueError for null fields
            State.objects.create(state_name=None)

    def test_duplicate_state_name(self):
        State.objects.create(state_name="Karnataka")
        with self.assertRaises(ValidationError):  # If uniqueness is enforced
            state = State(state_name="Karnataka")
            state.full_clean()

    def test_numeric_characters_in_state_name(self):
        with self.assertRaises(ValidationError):
            state = State(state_name="State123")
            state.full_clean()
            state.save()

    def test_unicode_state_name(self):
        state = State.objects.create(state_name="मध्य प्रदेश")  # Hindi for Madhya Pradesh
        self.assertEqual(state.state_name, "मध्य प्रदेश")

    def test_empty_state_table(self):
        states = State.objects.all()
        self.assertEqual(states.count(), 0)  # No states should exist initially

    def test_long_name_with_whitespace(self):
        long_name_with_spaces = " " + "A" + "a" * 253 + " "
        state = State.objects.create(state_name=long_name_with_spaces)
        self.assertEqual(state.state_name, "A"+"a" * 253)  # Whitespace trimmed, name still valid

    def test_name_normalization(self):
        state = State.objects.create(state_name="uTtAr PrAdEsH")
        self.assertEqual(state.state_name, "Uttar Pradesh")  # Check for normalized casing


    def test_bulk_create_states(self):
        states = [
            State(state_name="Rajasthan"),
            State(state_name="Assam"),
            State(state_name="Odisha"),
        ]
        State.objects.bulk_create(states)
        self.assertEqual(State.objects.count(), 3)

    def test_reserved_keyword_as_state_name(self):
        state = State.objects.create(state_name="Select")
        self.assertEqual(state.state_name, "Select")





class DepartmentModelTest(TestCase):
    def test_department_group_classification(self):
        state = State.objects.create(state_name="Maharashtra")
        department = Department.objects.create(state=state, department_name="Health and Family Welfare")
        self.assertEqual(department.get_group(), "Health")

    def test_department_without_state(self):
        with self.assertRaises(ValueError):  # Assuming `state` is required
            Department.objects.create(department_name="Finance")

    def test_empty_department_name(self):
        state = State.objects.create(state_name="Maharashtra")
        with self.assertRaises(ValidationError):
            department = Department(state=state, department_name="")
            department.full_clean()

    def test_long_department_name(self):
        state = State.objects.create(state_name="Maharashtra")
        long_name = "A" * 300  # Assuming max_length is 255
        with self.assertRaises(ValidationError):
            department = Department(state=state, department_name=long_name)
            department.full_clean()

    def test_invalid_department_name(self):
        state = State.objects.create(state_name="Maharashtra")
        with self.assertRaises(ValidationError):
            department = Department(state=state, department_name="Health@123")
            department.full_clean()

    




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

    def test_empty_scheme_title(self):
        state = State.objects.create(state_name="Tamil Nadu")
        department = Department.objects.create(state=state, department_name="Agriculture Department")
        with self.assertRaises(ValidationError):
            scheme = Scheme.objects.create(title="", department=department, description="Free fertilizers for farmers.")
            scheme.full_clean()

    def test_invalid_characters_in_scheme_description(self):
        state = State.objects.create(state_name="Tamil Nadu")
        department = Department.objects.create(state=state, department_name="Agriculture Department")
        scheme = Scheme.objects.create(title="Free Fertilizer Distribution", department=department, description="This scheme is 100% free!!")
        self.assertIn("100% free", scheme.description)

    def test_scheme_without_department(self):
        with self.assertRaises(ValueError):
            Scheme.objects.create(title="Free Fertilizer Distribution", description="A scheme to provide free fertilizers to farmers.")




class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Agriculture")
        self.assertEqual(tag.name, "Agriculture")

    def test_empty_tag_name(self):
        with self.assertRaises(ValidationError):
            tag = Tag.objects.create(name="")
            tag.full_clean()

    def test_long_tag_name(self):
        long_name = "A" * 300  # Assuming max_length is 255
        with self.assertRaises(ValidationError):
            tag = Tag.objects.create(name=long_name)
            tag.full_clean()


class BeneficiaryModelTest(TestCase):
    def test_create_beneficiary(self):
        beneficiary = Beneficiary.objects.create(beneficiary_type="Farmers")
        self.assertEqual(beneficiary.beneficiary_type, "Farmers")

    def test_empty_beneficiary_type(self):
        with self.assertRaises(ValidationError):
            beneficiary = Beneficiary.objects.create(beneficiary_type="")
            beneficiary.full_clean()

    def test_invalid_beneficiary_type(self):
        with self.assertRaises(ValidationError):
            beneficiary = Beneficiary.objects.create(beneficiary_type="Farmers@123")
            beneficiary.full_clean()



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

    def test_long_document_name(self):
        long_name = "A" * 300  # Assuming max_length is 255
        with self.assertRaises(ValidationError):
            document = Document.objects.create(document_name=long_name, requirements="Valid Aadhar Number")
            document.full_clean()


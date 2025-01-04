import json
from datetime import datetime, timezone
import re
import os
from django.core.management.base import BaseCommand
from datetime import datetime
import pytz
base_file_path = os.path.join(os.path.dirname(__file__), '..','scrapedData')

class Command(BaseCommand):
    help = 'Converts and combines data into a JSON file'

    def handle(self, *args, **kwargs):
        # Your logic for combining data goes here
        with open('combined_schemes_data.json', 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)
        self.stdout.write(self.style.SUCCESS('Combined data has been successfully saved to combined_schemes_data.json'))

def remove_leading_numbers(title):
    # Use a regular expression to remove leading numbers followed by a dot and whitespace
    return re.sub(r'^\d+\.\s*', '', title)
# Helper function to convert date format
def convert_date_format(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None
    return None

# Helper function to determine tags based on scheme title and description
def determine_tags(title, description):
    tags = []
    text = f"{title} {description}".lower()
    if "scholarship" in text:
        tags.append("scholarship")
    if "job" in text or "employment" in text:
        tags.append("job")
    return tags

def clean_field(field):
    if isinstance(field, str):
        return field.replace("\\n", "").replace("\\", "").strip()
    elif isinstance(field, list):
        return [clean_field(item) for item in field]
    elif isinstance(field, dict):
        return {key: clean_field(value) for key, value in field.items()}
    return field 

def transform_and_add_meghalaya_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Meghalaya"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_arunachal_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Arunachal Pradesh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_assam_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Assam"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_chandigarh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Chandigarh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_chhattisgarh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Chhattisgarh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_dadra_and_nagar_haveli_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Dadra and Nagar Haveli"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_delhi_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Delhi"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_gujrat_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Gujrat"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_haryana_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Haryana"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_jammu_and_kashmir_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Jammu and Kashmir"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_kerala_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Kerala"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_ladakh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Ladakh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_madhya_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Madhya Pradesh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_maharastra_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Maharastra"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_manipur_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Manipur"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_odissa_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Odissa"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_puducherry_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Puducherry"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_punjab_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Punjab"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_sikkim_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Sikkim"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_telangana_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Telangana"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_uttarakhand_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Uttarakhand"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title"))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Tamil Nadu data
        # END HERE
def transform_and_add_tamilnadu_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Tamil Nadu"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("Concerned Department").strip()
        organisation_name = item.get("Organisation Name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": organisation_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = item.get("Title / Name").strip()
        description = item.get("Description").strip()
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced On")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsored By"),
            "description": description,
            "scheme_link": item.get("URL"),
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiaries",[])}
            ] if item.get("beneficiaries",[]) else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type": item.get("Sponsored By")}
            ],
            "criteria": [
                {"description": item.get("How To Avail"), "value": ""}
            ] if item.get("How To Avail") else [],
            "procedures": [
                {"step_description": item.get("How To Avail")}
            ] if item.get("How To Avail") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Puducherry data



def transform_and_add_uttar_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Uttar Pradesh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = "उत्तर प्रदेश सरकार"
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        if not item.get("title",""):
            continue
        title = remove_leading_numbers(item.get("title",""))
        scheme_link = item.get("scheme_link")
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": convert_date_format(item.get("valid_upto")),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": scheme_link,
            
            "beneficiaries": [
                {"beneficiary_type": beneficiary} for beneficiary in item.get("beneficiaries", [])
            ],
            "sponsors": [
                {"sponsor_type": sponsor} for sponsor in item.get("sponsors", [])
            ],
            "criteria": [
                {"description": criterion, "value": ""} for criterion in item.get("criteria", [])
            ],
            "procedures": [
                {"step_description": step} for step in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description),
            "benefits": [
                {"benefit_type": benefit} for benefit in item.get("benefits", [])
            ],
            "criteria": [
                {"description": eligibility} for eligibility in item.get("eligibility", [])
            ],
            "application_process": [
                {"step_description": step} for step in item.get("application_process", [])
            ],
            "documents": [
                {"document_name": requirement} for requirement in item.get("requirements", [])
            ]
        }
        organisation["schemes"].append(scheme)

def transform_and_add_himachal_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Himachal Pradesh"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = "other"
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("name").strip())
        description = item.get("objective")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced on: ")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsors: "),
            "description": description,
            "scheme_link": item.get("applyOnlineLink"),
            "beneficiaries": [
                {"beneficiary_type": item.get("Scheme Beneficiaries: ").strip()}
            ] if item.get("Scheme Beneficiaries: ") else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type": item.get("Sponsors: ")}
            ],
            "criteria": [
                {"description": item.get("eligibility")}
                ],
            "procedures": [
                {"step_description": item.get("process")}
                ],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)



def transform_and_add_goa_data(original_data, combined_data):
    state_name = "Goa"

    for item in original_data:
        item = clean_field(item)
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("schemeUrl"),
            "pdf_url": item.get("pdfUrl"),
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": item.get("tags"),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
        }
        organisation["schemes"].append(scheme)


def transform_and_add_jharkhand_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = "Jharkhand"
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title",""))
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "pdf_url": item.get("pdfUrl"),
            "beneficiaries": [
                beneficiary_type["beneficiary_type"] for beneficiary_type in item.get("beneficiaries",[])
            ],
            "documents": item.get("documents",[]),
            "sponsors": [
                sponsor_type["sponsor_type"] for sponsor_type in item.get("sponsors",[])
            ],
            "criteria": [
                criteria_description["description"] for criteria_description in item.get("criteria",[])
            ],
            "procedures": [
                step_description["step_description"] for step_description in item.get("procedures",[])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_rajasthan_data(original_data, combined_data):
    state_name = "Rajasthan"

    for item in original_data:
        item = clean_field(item)
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("scheme_url"),  
            "pdf_url": item.get("pdfUrl"),  
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": item.get("tags"),  
            "statistical_summary": []  
        }
        organisation["schemes"].append(scheme)

def transform_and_add_tripura_data(original_data, combined_data):
    state_name = "Tripura"

    for item in original_data:
        item = clean_field(item)
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("schemeUrl"),
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": determine_tags(title, description),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
        }
        organisation["schemes"].append(scheme)





def transform_and_add_andhra_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = 'Andhra Pradesh'
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = ''
        organisation_name = ''
        state = next((s for s in combined_data['states'] 
            if s['state_name'] == state_name),None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)
        
        department = next((d for d in state['departments']
            if d["department_name"] == department_name ), None)
        
        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": organisation_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)
        organisation = department["organisations"][0]
        title = item.get("title").strip()
        description = item.get("description").strip()
        scheme = {
            "id" : item.get("id", ""),
            "title": title,
            "introduced_on":"2024-06-25T12:00:00Z",
            "valid_upto": '2024-12-31T23:59:59Z',
            "funding_pattern":"",
            "description": description,
            "scheme_link": item.get('scheme_url',''),
            "beneficiaries":  [
                {"beneficiary_type": item.get("beneficiaries",[])}
            ] if item.get("beneficiaries",[]) else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type":  ""}
            ],
            "criteria": [
                {"description": item.get("How To Avail"), "value": ""}
            ] if item.get("How To Avail") else [],
            "procedures": [
                {"step_description": item.get("How To Avail")}
            ] if item.get("How To Avail") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)
        



def transform_and_add_arunachal_pradesh_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = 'Arunachal Pradesh'
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = ''
        organisation_name = ''
        state = next((s for s in combined_data['states'] 
            if s['state_name'] == state_name),None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)
        
        department = next((d for d in state['departments']
            if d["department_name"] == department_name ), None)
        
        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": organisation_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)
        organisation = department["organisations"][0]
        title = item.get("title").strip()
        description = item.get("objective")
        if item.get('benefits'):
            for it in item.get('benefits'):
                description += it +'\n'
        scheme = {
            "id" : item.get("id", ""),
            "title": title,
            "introduced_on":"2024-06-25T12:00:00Z",
            "valid_upto": '2024-12-31T23:59:59Z',
            "funding_pattern":"",
            "description": description,
            "scheme_link": item.get('schemeUrl',''),
            "beneficiaries":  [
                {"beneficiary_type": item.get("beneficiaries",[])}
            ] if item.get("beneficiaries",[]) else [],
            "documents": item.get('documents',[]),
            "sponsors": [
                {"sponsor_type":  ""}
            ],
            "criteria": [
                {"description": item.get("How To Avail"), "value": ""}
            ] if item.get("How To Avail") else [],
            "procedures": [
                {"step_description": item.get("How To Avail")}
            ] if item.get("How To Avail") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)



def transform_and_add_andaman_nicobar_data(original_data, combined_data):
    for item in original_data:
        item = clean_field(item)
        state_name = 'Andaman and Nicobar'
        ist = pytz.timezone('Asia/Kolkata')
        created_at = datetime.now(ist).replace(microsecond=0).isoformat()
        department_name = ''
        organisation_name = ''
        state = next((s for s in combined_data['states'] 
            if s['state_name'] == state_name),None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)
        
        department = next((d for d in state['departments']
            if d["department_name"] == department_name ), None)
        
        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": organisation_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)
        organisation = department["organisations"][0]
        title = item.get("title").strip()
        description = item.get("description").strip()
        description +='\n'+ item.get('benefits') if item.get('benefits') else ''

        scheme = {
            "id" : item.get("id", ""),
            "title": title,
            "introduced_on":"2024-06-25T12:00:00Z",
            "valid_upto": '2025-12-31T23:59:59Z',
            "funding_pattern":"",
            "description": description,
            "scheme_link": item.get('scheme_url',''),
            "beneficiaries":  [
                {"beneficiary_type": item.get("beneficiaries",[])}
            ] if item.get("beneficiary") else [],
            "documents": item.get('documents',[]),
            "sponsors": [
                {"sponsor_type":  ""}
            ],
            "criteria": item.get('criteria',[]),
            "procedures": [
                {"step_description": item.get("How To Avail")}
            ] if item.get("How To Avail") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)



# Read data from JSON files
with open(base_file_path+"/meghalaya.json", "r") as file:
    meghalaya_data = json.load(file)

with open(base_file_path+"/tamilnadu.json", "r") as file:
    tamilnadu_data = json.load(file)

with open(base_file_path+"/puducherry.json", "r") as file:
    puducherry_data = json.load(file)

with open(base_file_path+"/jammukashmir.json", "r") as file:
    jammukashmir_data = json.load(file)


with open(base_file_path+"/gujrat.json", "r") as file:
    gujarat_data = json.load(file)

with open(base_file_path+"/maharastra.json", "r") as file:
    maharashtra_data = json.load(file)

with open(base_file_path+"/up/up_youth_welfare.json", "r") as file:
    up_data = json.load(file)

with open(base_file_path+"/himachalPradesh.json", "r") as file:
    himachal_data = json.load(file)

with open(base_file_path+"/madhya_pradesh.json", "r") as file:
    madhyaPradesh_data = json.load(file)

with open(base_file_path+"/kerala.json", "r") as file:
    kerala_data = json.load(file)

with open(base_file_path+"/manipur.json", "r") as file:
    manipur_data = json.load(file)

with open(base_file_path+"/goa.json", "r") as file:
    goa_data = json.load(file)

with open(base_file_path+"/jharkhand.json", "r") as file:
    jharkhand_data = json.load(file)

with open(base_file_path+"/tripura.json", "r") as file:
    tripura_data = json.load(file)

with open(base_file_path+"/sikkim.json", "r") as file:
    sikkim_data = json.load(file)

with open(base_file_path+"/telangana.json", "r") as file:
    telangana_data = json.load(file)

with open(base_file_path+"/uttarakhand.json", "r") as file:
    uttarakhand_data = json.load(file)

with open(base_file_path+"/delhi.json", "r") as file:
    delhi_data = json.load(file)

with open(base_file_path+"/ladakh.json", "r") as file:
    ladakh_data = json.load(file)

with open(base_file_path+"/andhra.json", "r") as file:
    andhra_pradesh_data = json.load(file)

with open(base_file_path+"/assam.json", "r") as file:
    assam_data = json.load(file)

with open(base_file_path+"/haryana.json", "r") as file:
    haryana_data = json.load(file)

with open(base_file_path+'/punjab.json','r') as file:
    punjab_data = json.load(file)

with open(base_file_path+"/odisha.json", "r") as file:
    odisha_data = json.load(file)

with open(base_file_path+"/arunachalPradesh.json", "r") as file:
    arunachal_pradesh_data = json.load(file)

with open(base_file_path+"/dadar_nagar_haveli.json", "r") as file:
    dadar_nagar_haveli_data = json.load(file)

with open(base_file_path+"/nicobar.json", "r") as file:
    nicobar_data = json.load(file)

with open(base_file_path+"/chandigarh.json", "r") as file:
    chandigarh_data = json.load(file)

with open(base_file_path+"/chhattisgarh.json", "r") as file:
    chhattisgarh_data = json.load(file)

# Initialize the combined data structure
combined_data = {
    "states": []
}


# Transform and add data to the combined structure
transform_and_add_meghalaya_data(meghalaya_data, combined_data)
transform_and_add_tamilnadu_data(tamilnadu_data, combined_data)
transform_and_add_puducherry_data(puducherry_data, combined_data)
transform_and_add_jammu_and_kashmir_data(jammukashmir_data, combined_data)
transform_and_add_gujrat_data(gujarat_data, combined_data)
transform_and_add_maharastra_data(maharashtra_data, combined_data)
transform_and_add_uttar_pradesh_data(up_data,combined_data)
transform_and_add_himachal_pradesh_data(himachal_data,combined_data)
transform_and_add_madhya_pradesh_data(madhyaPradesh_data,combined_data)
transform_and_add_kerala_data(kerala_data,combined_data)
transform_and_add_manipur_data(manipur_data,combined_data)
transform_and_add_goa_data(goa_data,combined_data)
transform_and_add_jharkhand_data(jharkhand_data,combined_data)
transform_and_add_tripura_data(tripura_data,combined_data)
transform_and_add_sikkim_data(sikkim_data,combined_data)
transform_and_add_telangana_data(telangana_data,combined_data)
transform_and_add_uttarakhand_data(uttarakhand_data,combined_data)
transform_and_add_delhi_data(delhi_data,combined_data)
transform_and_add_ladakh_data(ladakh_data,combined_data)
transform_and_add_andhra_pradesh_data(andhra_pradesh_data,combined_data)
transform_and_add_assam_data(assam_data, combined_data)
transform_and_add_haryana_data(haryana_data, combined_data)
transform_and_add_punjab_data(punjab_data, combined_data)
transform_and_add_odissa_data(odisha_data, combined_data)
transform_and_add_arunachal_pradesh_data(arunachal_pradesh_data,combined_data)
transform_and_add_dadra_and_nagar_haveli_data(dadar_nagar_haveli_data,combined_data)
transform_and_add_andaman_nicobar_data(nicobar_data,combined_data)
transform_and_add_chandigarh_data(chandigarh_data, combined_data)
transform_and_add_chhattisgarh_data(chhattisgarh_data, combined_data)

# Save the combined data to a new JSON file
with open(base_file_path+"/combined_schemes_data.json", "w") as file:
    json.dump(combined_data, file,ensure_ascii=False, indent=4)

# print("Combined data has been successfully saved to combined_schemes_data.json")
# print("Combined data has been successfully saved to combined_schemes_data.json")
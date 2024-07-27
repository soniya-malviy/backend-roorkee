import json
from datetime import datetime

base_file_path = "/Users/gangadgaryadav/iitroorkeebackend/backend-roorkee/myapp/management/scrapedData"

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
    # Add more conditions for different types of schemes
    return tags

def transform_and_add_meghalaya_data(original_data, combined_data):
    for item in original_data:
        state_name = "Meghalaya"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("Department: ").strip()
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
        title = item.get("Title: ").strip()
        description = item.get("Description: ").strip()
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced on: ")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsors: ").strip(),
            "description": description,
            "scheme_link": item.get("Scheme Link: ").strip(),
            "beneficiaries": [
                {"beneficiary_type": item.get("Scheme Beneficiaries: ").strip()}
            ] if item.get("Scheme Beneficiaries: ") else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type": item.get("Sponsors: ").strip()}
            ],
            "criteria": [
                {"description": item.get("How to Avail: ").strip(), "value": ""}
            ] if item.get("How to Avail: ") else [],
            "procedures": [
                {"step_description": item.get("How to Avail: ").strip()}
            ] if item.get("How to Avail: ") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Tamil Nadu data
def transform_and_add_tamilnadu_data(original_data, combined_data):
    for item in original_data:
        state_name = "Tamil Nadu"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("Concerned Department")
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
        title = item.get("Title / Name")
        description = item.get("Description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced On")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsored By"),
            "description": description,
            "scheme_link": item.get("URL"),
            "beneficiaries": [
                {"beneficiary_type": item.get("Beneficiaries")}
            ] if item.get("Beneficiaries") else [],
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
def transform_and_add_puducherry_data(original_data, combined_data):
    for item in original_data:
        state_name = "Puducherry"
        created_at = "2024-06-25T12:00:00Z"
        department_name = "Adi Dravidar Welfare Department"
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
        title = item.get("title")
        description = " ".join(item["details"].get("Objective", []))
        scheme = {
            "title": title,
            "introduced_on": "2024-06-25T12:00:00Z",
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": "State",
            "description": description,
            "scheme_link": item.get("link"),
            "beneficiaries": [
                {"beneficiary_type": "SC/ST/OEBC"}
            ],
            "documents": [
                {"document_name": doc} for doc in item["details"].get("Required Documents / Enclosures with Application", [])
            ],
            "sponsors": [
                {"sponsor_type": "State"}
            ],
            "criteria": [
                {"description": eligibility, "value": ""} for eligibility in item["details"].get("Eligibility", [])
            ],
            "procedures": [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Jammu and Kashmir data
def transform_and_add_jammukashmir_data(original_data, combined_data):
    for program in original_data:
        state_name = "Jammu and Kashmir"
        created_at = "2024-06-25T12:00:00Z"
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department_name = program.get("title")
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
        for item in program.get("schemes", []):
            title = item.get("name")
            description = item["details"].get("Description of the Scheme", "")
            scheme = {
                "title": title,
                "introduced_on": "2024-06-25T12:00:00Z",
                "valid_upto": "2024-12-31T23:59:59Z",
                "funding_pattern": "Central and State",
                "description": description,
                "scheme_link": item.get("url"),
                "beneficiaries": [
                    {"beneficiary_type": item["criteria"].get("Category")}
                ] if item.get("criteria") else [],
                "documents": [],
                "sponsors": [
                    {"sponsor_type": "Central and State"}
                ],
                "criteria": [
                    {"description": key + ": " + value} for key, value in item["criteria"].items()
                ] if item.get("criteria") else [],
                "procedures": [
                    {"step_description": item["details"].get("Procedure", "")}
                ] if item.get("details") else [],
                "tags": determine_tags(title, description)
            }
            organisation["schemes"].append(scheme)

def transform_and_add_gujarat_data(original_data, combined_data):
    for item in original_data:
        state_name = "Gujarat"
        created_at = "2024-06-25T12:00:00Z"
        department_name = "Scheduled Caste Welfare Department"
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
        title = item.get("title")
        description = item["details"].get("Scheme Name")
        scheme = {
            "title": title,
            "introduced_on": "2024-06-25T12:00:00Z",
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": "State",
            "description": description,
            "scheme_link": item["details"].get("Assistance Details", "").split("\n(Portal: ")[-1][:-1],

            "beneficiaries": [
                {"beneficiary_type": "SC"}
            ],
            "documents": [
                {"document_name": "Pre-defined Application Form", "description": item["details"].get("Pre-defined Application Form")}
            ],
            "sponsors": [
                {"sponsor_type": "State"}
            ],
            "criteria": [
                {"description": item["details"].get("Eligibility Criteria :"), "value": ""}
            ],
            "procedures": [
                {"step_description": item["details"].get("Assistance Details", "").split("\n")[0]}
            ],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)
    

def transform_and_add_maharashtra_data(original_data, combined_data):
    state_name = "Maharashtra"
    created_at = "2024-06-25T12:00:00Z"

    for item in original_data:
        title = item["details"].get("Name of the Scheme", "").strip()
        scheme_id = item.get("id", "")

        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department_name = item["details"].get("Category of Scheme", "").strip()
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
        description = item["details"].get("Scheme Objective", "").strip()

        scheme = {
            "title": title,
            "introduced_on": None if item["details"].get("Introduced On", "").strip() == "" else item["details"]["Introduced On"].strip(),
            "valid_upto": None if item["details"].get("Valid Upto", "").strip() == "" else item["details"]["Valid Upto"].strip(),
            "funding_pattern": item["details"].get("Funding by", "").strip(),
            "description": description,
            "scheme_link": "",  # This data is not provided in the example, adjust as needed
            "beneficiaries": [
                {"beneficiary_type": item["details"].get("Beneficiary Category", "").strip()}
            ],
            "documents": [],  # You may need to adjust this based on available data
            "sponsors": [],  # This data is not provided in the example, adjust as needed
            "criteria": [
                {"description": item["details"].get("Eligibility Criteria", ""), 
                 "value": ""}
            ],
            "procedures": [
                {"step_description": item["details"].get("Application Process", "").strip()}
            ],
            "tags": determine_tags(title, description),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
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

with open(base_file_path+"/gujratschemes.json", "r") as file:
    gujarat_data = json.load(file)

with open(base_file_path+"/maharastra.json", "r") as file:
    maharashtra_data = json.load(file)

# Initialize the combined data structure
combined_data = {
    "states": []
}

# Transform and add data to the combined structure
transform_and_add_meghalaya_data(meghalaya_data, combined_data)
transform_and_add_tamilnadu_data(tamilnadu_data, combined_data)
transform_and_add_puducherry_data(puducherry_data, combined_data)
transform_and_add_jammukashmir_data(jammukashmir_data, combined_data)
transform_and_add_gujarat_data(gujarat_data, combined_data)
transform_and_add_maharashtra_data(maharashtra_data, combined_data)



# Save the combined data to a new JSON file
with open(base_file_path+"/combined_schemes_data.json", "w") as file:
    json.dump(combined_data, file, indent=4)

print("Combined data has been successfully saved to combined_schemes_data.json")
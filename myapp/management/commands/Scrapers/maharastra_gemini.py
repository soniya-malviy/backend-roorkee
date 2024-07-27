import os
import json
import google.generativeai as genai
from typing_extensions import TypedDict



os.environ['GENAI_API_KEY'] = 'AIzaSyAETMREYpywQDt-DVe6jcy-XhSWnYYUaVE'

genai.configure(api_key=os.environ['GENAI_API_KEY'])




# TRYING TO WRITE OWN ACTUAL SCHEMA

file_path = "/Users/gangadgaryadav/iitroorkeebackend/backend-roorkee/myapp/management/scrapedData/maharastra.json"



class Age_limit(TypedDict):
    lower_age: int
    upper_age: int

class Income_limit(TypedDict):
    rural: int
    urban: int
    general: int

class Education(TypedDict):
    min_standard: str
    max_standard: str
    school_type: str


class Criteria(TypedDict):
    age_limit: Age_limit
    income_limit: Income_limit
    education: Education
    community: list[str]
    bpl_card_holder: bool

def add_to_database(
    criteria: list[Criteria],
    tags: list[str]
    
    
):
    pass
    

# END HERE

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools = [add_to_database])




with open(file_path, 'r') as file:
    data = json.load(file)

eligibility_criteria_list = [scheme['details'].get('Eligibility Criteria') for scheme in data]


for scheme in data:
    description = scheme['details'].get('Eligibility Criteria')
    title = scheme['details'].get('Benefits Provided')
    

    try:
        result = model.generate_content(f"""
        {description} {title}

        Please add the Criteria from this description to the database make sure to add lower age and upper age.
        and analyse above data  based on that add tags which can distinguish schemes for scholarship schemes add scholarship tag and for job related schemes add job tag and for rest of the scheme add general scheme
        """,

        )
        fc = result.candidates[0].content.parts[0].function_call

        final_data = json.dumps(type(fc).to_dict(fc), indent=4)
        convert_data = json.loads(final_data)
        # print(final_data["args"])
        final_converted_data = convert_data.get("args",{})
        scheme['details']['Eligibility Criteria'] = final_converted_data["criteria"]
        scheme['tags'] = final_converted_data["tags"]


        # scheme['details']['Eligibility Criteria'] = criteria_json
    except:
        try:
            result = model.generate_content(f"""
            {description}

            Please add the Criteria from this description to the database make sure to add lower age and upper age.
            and analyse this title name {title} based on that add tags it can be job openings, scholarship or anything which distinguish schemes
            """,

            )
            fc = result.candidates[0].content.parts[0].function_call

            final_data = json.dumps(type(fc).to_dict(fc), indent=4)
            convert_data = json.loads(final_data)
            # print(final_data["args"])
            final_converted_data = convert_data.get("args",{})
            scheme['details']['Eligibility Criteria'] = final_converted_data["criteria"]
            scheme['tags'] = final_converted_data["tags"]
        except Exception as e:
            print("Error",e)
            print(description)

with open(file_path, 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

    
    
    
        
        
    
    
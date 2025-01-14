import os
import json
from pdfParser import process_with_api_key_rotation

api_keys = [
     "AIzaSyCx6SfkUW-OV4H_9eDXI6EaLcRxnNXNc8k",
    "AIzaSyAtMYT6cBvYXUbBoomMlPRhvh4ff2Y5LBY",
    "AIzaSyBuE7BohUwPRYWfzMVIO-QhAOMHPxsFPLI",
    "AIzaSyCx6SfkUW-OV4H_9eDXI6EaLcRxnNXNc8k",
    # os.getenv("API_KEY_4"),
    # os.getenv("API_KEY_5"),
    # os.getenv("API_KEY_6"),
    
]


def structure_schemes(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        schemeData = json.load(file)
    if not os.path.exists(output_file_path):
        with open(output_file_path, 'w', encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    for schemes in schemeData:
        result = process_with_api_key_rotation(schemes, api_keys)
        if result and result.candidates:
                try:
                    fc = result.candidates[0].content.parts[0].function_call
                    final_data = json.dumps(type(fc).to_dict(fc), indent=4)
                    convert_data = json.loads(final_data)
                    final_converted_data = convert_data.get("args", {})
                    final_converted_data = final_converted_data.get("scheme_details")
                    if final_converted_data:
                        final_converted_data["id"] = schemes.get("id")
                        print("ye data", final_converted_data)
                        with open(output_file_path, 'r+', encoding="utf-8") as f:
                            existing_data = json.load(f)  # Load existing data
                            existing_data.append(final_converted_data)  # Append new data
                            f.seek(0)  # Reset file pointer to the start
                            json.dump(existing_data, f, ensure_ascii=False, indent=4)  # Write updated data
                            f.truncate()

                except Exception as e:
                     print("yaha aya thaaaa: ",e)

states_and_ut = [
    "punjab",
    "andhraPradesh",
    "gujarat",
    "haryana",
    "Uttar Pradesh",
    "assam",
    "maharashtra",
    "manipur",
    "meghalaya",
    "kerala",
    "tamilnadu",
    "jammuAndKashmir",
    "puducherry",
    "odisha",
    "himachalPradesh",
    "madhyaPradesh",
    "uttarakhand",
    "sikkim",
    "telangana",
    "chhattisgarh",
    "arunachalpradesh",
    "delhi",
    "ladakh",
    "dadraAndNagarHaveli",
    "nagaland",
    "chandigarh",
    "andamanAndNicobar"
]

for state_name in states_and_ut:
    base_file_path = os.path.join(os.path.dirname(__file__),'..', '..', 'scrapedData',f'{state_name}.json')
    input_file_path = os.path.abspath(base_file_path)
    output_file_path = os.path.join(os.path.dirname(__file__),'..', '..', 'structuredData', f'{state_name}_structured_results.json')
    structure_schemes(input_file_path, output_file_path)







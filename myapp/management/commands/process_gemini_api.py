import os
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

file_path = './mappedSchemesData.json'

# Attempt to read the file in binary mode and then decode
data = None

try:
    with open(file_path, 'rb') as f:
        content = f.read()
        data = json.loads(content.decode('utf-8', errors='replace'))  # Replace undecodable characters
except UnicodeDecodeError:
    print("Error: Could not decode JSON file.")
    exit()
except FileNotFoundError:
    print("Error: File not found.")
    exit()

if data is None:
    print("Error: Could not read JSON file.")
    exit()

# Check if the data is a non-empty list
if isinstance(data, list) and len(data) > 0:
    raw_json = data
else:
    print("Error: JSON data does not contain a list or is empty.")
    exit()

# Define the template for the formatted data
formatted_data_template = {
    "states": [
        {
            "state_name": "Tamil Nadu",
            "created_at": "2024-06-25T12:00:00Z",
            "departments": [
                {
                    "department_name": "Department of Education",
                    "created_at": "2024-06-25T12:00:00Z",
                    "organisations": [
                        {
                            "organisation_name": "Educational Board",
                            "created_at": "2024-06-25T12:00:00Z",
                            "schemes": []
                        }
                    ]
                }
            ]
        }
    ]
}

# Set the API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the Generative AI model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to process a chunk of raw JSON data
def process_chunk(chunk):
    formatted_data = formatted_data_template.copy()

    # Prepare the prompt
    prompt = f"""
    Given a JSON array {json.dumps(chunk)}, referred to as rawjson, and a JSON object {json.dumps(formatted_data)}, referred to as formattedjson, your task is to populate the values in formattedjson based on the data in rawjson for each JSON object individually. Return the resulting JSON object in the formattedjson JSON format. Ensure that the output consists solely of JSON and nothing else. Consider the state as Tamil Nadu.
    """

    # Generate the content
    response = model.generate_content(prompt)

    # Check if response contains valid content
    if not response or not response.candidates:
        print("Error: No valid response received from the model.")
        return None

    # Extract the JSON text
    response_text = response.text

    # Strip the backticks and newline characters
    response_text = response_text.strip("```json\n").strip("```")

    # Parse the response
    response_json = None
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode the response as JSON. {e}")
        print(response_text)
        return None

    return response_json

# Process raw JSON data in chunks
chunk_size = 10  # Adjust the chunk size as needed
processed_chunks = []

for i in range(0, len(raw_json), chunk_size):
    chunk = raw_json[i:i + chunk_size]
    result = process_chunk(chunk)
    if result:
        processed_chunks.append(result)

# Combine the processed chunks into a single JSON object
final_result = formatted_data_template.copy()

for chunk in processed_chunks:
    final_result['states'][0]['departments'][0]['organisations'][0]['schemes'].extend(
        chunk['states'][0]['departments'][0]['organisations'][0]['schemes']
    )

# Save the final result to a new JSON file
output_file_path = './formattedSchemesData.json'
try:
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)
    print(f"Data successfully saved to {output_file_path}")
except Exception as e:
    print(f"Error: Could not save data to file. {e}")
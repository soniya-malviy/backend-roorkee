import requests
import io
import pdfplumber
from docx import Document
import pypandoc
import os
import json
from structureGemini import process_and_structure_document
import time
from google.api_core.exceptions import ResourceExhausted
from google.api_core.exceptions import DeadlineExceeded
from trackScheme import (
    calculate_hash,
    load_previous_state,
    save_current_state,
    identify_changes,
)
import os
from dotenv import load_dotenv


load_dotenv()
base_file_path = os.path.join(os.path.dirname(__file__),'..','goaScraper','goa_pdf_link2.json')
absolute_file_path = os.path.abspath(base_file_path)
output_file = os.path.join(os.path.dirname(__file__),'..','goaScraper', 'structured_results.json')
state_file = 'scheme_state.json'

api_keys = [
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
    os.getenv("API_KEY_4"),
    os.getenv("API_KEY_5"),
    os.getenv("API_KEY_6"),
    os.getenv("API_KEY_7")
]




# print("ye dekhna:",absolute_file_path)

with open(absolute_file_path, "r") as file:
    goaPdfText = json.load(file)

def parse_pdf(pdf_url):
    pdfText = ''
    response = requests.get(pdf_url, stream=True)
    response.raise_for_status()

    pdf_buffer = io.BytesIO(response.content)

    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            pdfText += text
    return pdfText


def parse_docx(docx_url):
    """ Parse DOCX file from URL and extract text """
    docxText = ''
    response = requests.get(docx_url, stream=True)
    response.raise_for_status()

    docx_buffer = io.BytesIO(response.content)
    doc = Document(docx_buffer)

    # Extract text from paragraphs
    for para in doc.paragraphs:
        docxText += para.text + "\n"
    return docxText

def parse_doc(doc_url):
    docText = ''
    response = requests.get(doc_url,stream=True)
    response.raise_for_status()

    docText = pypandoc.convert_file(io.BytesIO(response.content), 'plain')
    return docText

def parse_document(url):
    # print("ye url",url)
    
    file_extension = url.split('.')[-1].lower()


    if file_extension == 'pdf':
        return parse_pdf(url)

    elif file_extension == 'docx':
        return parse_docx(url)


    elif file_extension == 'doc':
        return parse_doc(url)

    else:
        return parse_pdf(url)


def process_with_api_key_rotation(extractedSchemeText, api_keys, retries=5):
    for api_key in api_keys:
        # print(f"Trying API key: {api_key}")
        for attempt in range(retries):
            try:
                result = process_and_structure_document(extractedSchemeText, api_key)
                return result

            except ResourceExhausted as e:
                # print(f"Attempt {attempt + 1} with API key {api_key} failed: {str(e)}")
                if attempt < retries - 1:
                    backoff_time = 2 ** attempt
                    # print(f"Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                else:
                    # print(f"API key {api_key} exhausted, moving to the next key.")
                    break
            except DeadlineExceeded as e:
                print(f"Attempt {attempt + 1} with API key {api_key} failed due to DeadlineExceeded: {str(e)}")
                if attempt < retries - 1:
                    backoff_time = 2 ** attempt
                    # print(f"Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                else:
                    # print(f"API key {api_key} exhausted, moving to the next key.")
                    break

            except Exception as e:
                # print(f"Attempt {attempt + 1} with API key {api_key} failed due to an unexpected error: {str(e)}")
                if attempt < retries - 1:
                    backoff_time = 2 ** attempt
                    # print(f"Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                else:
                    # print(f"API key {api_key} exhausted, moving to the next key.")
                    break
    # print("All API keys exhausted, unable to process the document.")
    return None


def main():
    previous_state = load_previous_state(state_file)

    new_schemes, updated_schemes = identify_changes(goaPdfText, previous_state)
    schemes_to_process = new_schemes + updated_schemes

    final_results = []

    for scheme in schemes_to_process:
        if scheme["pdfUrl"] is not None:
            extractedSchemeText = parse_document(scheme["pdfUrl"])
        else:
            # print("None pdf")
            continue

        if extractedSchemeText:
            result = process_with_api_key_rotation(extractedSchemeText, api_keys)

            if result and result.candidates:
                try:
                    fc = result.candidates[0].content.parts[0].function_call
                    final_data = json.dumps(type(fc).to_dict(fc), indent=4)
                    convert_data = json.loads(final_data)
                    final_converted_data = convert_data.get("args", {})
                    final_converted_data = final_converted_data.get("scheme_details")

                    if final_converted_data is None or not isinstance(final_converted_data, dict):
                        # print(f"Invalid final_converted_data for scheme: {scheme['pdfUrl']}")
                        scheme_info = {
                            "title": scheme["title"],
                            "pdfUrl": scheme["pdfUrl"],
                            "schemeUrl": scheme.get("schemeUrl", "N/A")  # Default to "N/A" if schemeUrl is missing
                        }
                    else:
                        final_converted_data["schemeUrl"] = scheme.get("schemeUrl", "N/A")

                        if not final_converted_data.get("title") or final_converted_data.get("title") == "null" or '\\u' in final_converted_data.get("title", "") or '\\' in final_converted_data.get("title", ""):
                            scheme_info = {
                                "title": scheme["title"],
                                "pdfUrl": scheme["pdfUrl"],
                                "schemeUrl": scheme.get("schemeUrl", "N/A") 
                            }
                        elif not final_converted_data.get("description"):
                            scheme_info = {
                                "title": scheme["title"],
                                "pdfUrl": scheme["pdfUrl"],
                                "schemeUrl": scheme.get("schemeUrl", "N/A")
                            }
                        elif '\\' in final_converted_data.get("description", "") or '\\u' in final_converted_data.get("description", ""):
                            scheme_info = {
                                "title": scheme["title"],
                                "pdfUrl": scheme["pdfUrl"],
                                "schemeUrl": scheme.get("schemeUrl", "N/A")
                            }
                        else:
                            # Check if any description in the 'criteria' contains '\\' or '\ut'
                            criteria_descriptions = final_converted_data.get("criteria", [])
                            for criteria in criteria_descriptions:
                                if criteria.get("description", "").find("\\") != -1 or criteria.get("description", "").find("\\u") != -1:
                                    # print(f"Invalid description in criteria for scheme: {scheme['pdfUrl']}")
                                    scheme_info = {
                                        "title": scheme["title"],
                                        "pdfUrl": scheme["pdfUrl"],
                                        "schemeUrl": scheme.get("schemeUrl", "N/A")
                                    }
                                    break
                            else:
                                # Otherwise, append the final converted data
                                scheme_info = final_converted_data
                    
                    with open(output_file, 'a', encoding='utf-8') as f:
                        if os.stat(output_file).st_size == 0:
                            f.write("[\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                        else:
                            # f.seek(f.tell() - 1, os.SEEK_SET)  
                            f.write(",\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                            
                        
                    # print(f"Processed and appended scheme: {scheme['pdfUrl']}")
                except IndexError as e:
                    # print(f"Error processing the result for {scheme['pdfUrl']}: {e}")
                    scheme_info = {
                            "title": scheme["title"],
                            "pdfUrl": scheme["pdfUrl"],
                            "schemeUrl": scheme.get("schemeUrl", "N/A")
                        }
                    with open(output_file, 'a', encoding='utf-8') as f:
                        if os.stat(output_file).st_size == 0:
                            f.write("[\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                        else:
                            # f.seek(f.tell() - 1, os.SEEK_SET)  
                            f.write(",\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
            else:
                # print(f"Failed to process the scheme: {scheme['pdfUrl']}")
                scheme_info = {
                            "title": scheme["title"],
                            "pdfUrl": scheme["pdfUrl"],
                            "schemeUrl": scheme.get("schemeUrl", "N/A")
                        }
                with open(output_file, 'a', encoding='utf-8') as f:
                        if os.stat(output_file).st_size == 0:
                            f.write("[\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                        else:
                            # f.seek(f.tell() - 1, os.SEEK_SET)  
                            f.write(",\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
        else:
            # print(f"Failed to extract text from the document: {scheme['pdfUrl']}")
            scheme_info = {
                            "title": scheme["title"],
                            "pdfUrl": scheme["pdfUrl"],
                            "schemeUrl": scheme.get("schemeUrl", "N/A")
                        }
            with open(output_file, 'a', encoding='utf-8') as f:
                        if os.stat(output_file).st_size == 0:
                            f.write("[\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                        else:
                            # f.seek(f.tell() - 1, os.SEEK_SET)  
                            f.write(",\n")
                            json.dump(scheme_info, f, indent=4, ensure_ascii=False)
                            
    with open(output_file, 'a') as f:
        f.write("\n]")
    current_state = {scheme["id"]: calculate_hash(scheme) for scheme in goaPdfText}
    save_current_state(state_file, current_state)

if __name__ == "__main__":
    main()


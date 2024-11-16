import re
import json
from googletrans import Translator

translator = Translator()

def clean_text(text):
    # Remove excessive whitespace, line breaks, and unnecessary characters
    text = re.sub(r'\n+', '\n', text.strip())
    text = re.sub(r'\s{2,}', ' ', text)
    return text

def translate_text(text, src='auto', dest='en'):
    try:
        translation = translator.translate(text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def process_plain_text(filepath):
    structured_data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split text by sections based on newlines and possible headers
    sections = re.split(r'\n\s*\n', content)  # Split on empty lines or multiple newlines

    for section in sections:
        if len(section.strip()) > 20:  # Filter out very short sections
            section = clean_text(section)

            # Detect if the section is in Hindi and translate if needed
            if re.search(r'[ऀ-ॿ]', section):  # Check for Hindi characters
                section = translate_text(section)

            # Add each cleaned and translated section to structured data
            structured_data.append({
                "content": section
            })

    # Save to JSON format
    with open('processed_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

    print("Processing complete. Data saved to processed_data.json")
# Use the function
process_plain_text('data_generation/raw.txt')

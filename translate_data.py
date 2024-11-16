import json
import re
from googletrans import Translator

translator = Translator()

def detect_and_translate_hindi(text, src='auto', dest='en'):
    """
    Detects Hindi text and translates it to English.
    Handles cases where translation returns None or raises errors.
    """
    if not text:  # Skip if text is None or empty
        return text

    # Check if Hindi characters are present
    if re.search(r'[ऀ-ॿ]', text):
        try:
            translation = translator.translate(text, src=src, dest=dest)
            return translation.text if translation.text else text  # Fallback to original text if None
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    return text

def translate_hindi_in_json(input_file_path, output_file_path):
    # Load the existing JSON data
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Translate any Hindi content in each entry
    for entry in data:
        if "content" in entry:
            entry["content"] = detect_and_translate_hindi(entry["content"])

    # Save the updated data to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Translation complete. Translated data saved to {output_file_path}.")

# Run the function with the path to your input and output JSON files
translate_hindi_in_json('processed_data.json', 'translated_data.json')

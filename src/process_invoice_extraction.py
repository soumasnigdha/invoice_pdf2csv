from src.data_extraction import extract_info_with_gemini
from src.pdf_to_img import convert_pdf_to_images
from src.flatten_invoice import flatten_invoice_data
import os
import json
import csv

def process_invoices(prompt, input_dir, output_dir, output_csv_file):
    """
    Initiates all the files to process the invoices and save the CSV file.
    """
    extracted_results = {}
    all_flattened_data = []
    all_headers = set()
    image_paths = []
    for filename in os.listdir(input_dir):
        # Check if it's a file and ends with .pdf
        if os.path.isfile(os.path.join(input_dir, filename)) and filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"--- Processing {pdf_path} with Gemini ---")
        
        image_paths = convert_pdf_to_images(pdf_path, output_dir)

        gemini_response = extract_info_with_gemini(image_paths, prompt)
        if gemini_response:
            print("Gemini's Raw Response:\n", gemini_response)
            print(gemini_response)

            # Initialize json_string with the stripped raw response to clean up outer whitespace/newlines
            json_string = gemini_response.strip()

            # Check for and remove the leading Markdown code block indicator
            if json_string.startswith("```json"):
                json_string = json_string[len("```json"):].strip() # Remove prefix and strip
        
            # Check for and remove the trailing Markdown code block indicator
            if json_string.endswith("```"):
                json_string = json_string[:-len("```")].strip() # Remove suffix and strip
            
            # Add a final strip just in case, for any lingering whitespace/newlines
            json_string = json_string.strip()
      

            try:
                parsed_data = json.loads(json_string)
                print("\nParsed JSON Data (now processing for CSV):")
                print(json.dumps(parsed_data, indent=2)) 

                # Flatten the data for CSV
                flattened_rows = flatten_invoice_data(parsed_data)
                all_flattened_data.extend(flattened_rows)
                    
                # Collect all headers
                for row in flattened_rows:
                    all_headers.update(row.keys())

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from Gemini response for {pdf_path}: {e}")
                print(f"Attempted to parse this (cleaned) string:\n---START---\n{json_string}\n---END---")
        else:
            print(f"No response from Gemini for {pdf_path}")
 
    # After processing all PDFs, write to CSV
    if all_flattened_data:
        # Sort headers for consistent column order
        sorted_headers = sorted(list(all_headers))
    
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted_headers)
            writer.writeheader()
            for row in all_flattened_data:
                writer.writerow(row)
        print(f"\n--- Successfully extracted data to {output_csv_file} ---")
        return True
    else:
        print("\n--- No data extracted to write to CSV ---")
        return False

   
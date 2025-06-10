from pdf2image import convert_from_path
import os
POPPLET_BIN_PATH = None

def convert_pdf_to_images(pdf_path, output_folder="output"):
    """Converts each page of a PDF into a JPEG image."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to a list of PIL Image objects
    try:
        images = convert_from_path(pdf_path, poppler_path=POPPLET_BIN_PATH)
    except Exception as e:
        print(f"Error converting PDF to image. Check Poppler installation and poppler_path: {e}")
        print(f"Attempted Poppler Path: {POPPLET_BIN_PATH}")
        return []
    
    image_paths = []
    for i, image in enumerate(images):
        image_name = f"{os.path.basename(pdf_path).replace('.pdf', '')}_page_{i+1}.jpg"
        image_path = os.path.join(output_folder, image_name)
        image.save(image_path, "JPEG")
        image_paths.append(image_path)
    return image_paths

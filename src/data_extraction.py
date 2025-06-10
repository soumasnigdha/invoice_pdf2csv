import google.generativeai as genai
from PIL import Image
import os
from src.pdf_to_img import convert_pdf_to_images


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def extract_info_with_gemini(image_paths, prompt_text):
    """
    Sends images and a prompt to the Gemini Vision model to extract information.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Prepare the content for the model: list of prompt text and Image objects
    contents = [prompt_text]
    for img_path in image_paths:
        contents.append(Image.open(img_path))

    try:
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return None



# Invoice Data Extractor

This project provides a Streamlit web application that leverages the Gemini Vision model to extract structured data from PDF invoices and exports the extracted information into a clean, flattened CSV format.

## Features

-   **PDF Upload:** Easily upload multiple PDF invoice files.
-   **AI-Powered Extraction:** Utilizes Google's Gemini Vision model to accurately parse invoice details, including:
    -   Seller Information (Name, GSTIN)
    -   Invoice Details (Number, Order ID, Dates)
    -   Billing and Shipping Addresses
    -   Itemized Product Details (Product Name, FSN, HSN/SAC, Quantity, Amounts, Taxes)
    -   Shipping and Handling Charges
    -   Grand Total
-   **Data Flattening:** Converts complex nested JSON output from the AI into a flat structure suitable for CSV, with one row per product item.
-   **CSV Export:** Download the extracted data as a well-organized CSV file.
-   **CSV Preview:** View the first few rows of the generated CSV directly in the application.
-   **Automatic Cleanup:** Cleans up temporary input and output directories on application exit.

## How it Works

1.  **PDF to Images:** The application first converts each page of the uploaded PDF invoices into JPEG images using `pdf2image`.
2.  **Gemini Vision Extraction:** These images, along with a detailed prompt, are sent to the Gemini Vision model. [cite_start]The model is instructed to extract specific invoice fields and return them in a structured JSON format.
3.  **JSON Parsing & Cleaning:** The raw JSON response from Gemini is cleaned and parsed to handle potential markdown formatting.
4.  **Data Flattening:** The `flatten_invoice.py` script transforms the nested JSON data into a flat list of dictionaries. This process ensures that each product item gets its own row in the final CSV, while retaining all relevant invoice-level details. [cite_start]Special handling is included to filter out "Shipping And Handling Charges" or "Shipping And Packaging Charges" as separate product items.
5.  **CSV Generation:** The flattened data is then written to a CSV file, with headers sorted for consistency.
6.  **Streamlit Interface:** A user-friendly Streamlit interface allows for easy file uploads, initiation of the extraction process, and downloading/previewing of the results.

## Setup and Installation

### Prerequisites

* Python 3.8+
* Google Cloud Project with access to the Gemini API.
* An API Key for the Gemini API.
* Poppler: A PDF rendering library. This is a system-level dependency.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd invoice-data-extractor
    ```

2.  **Set up a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Poppler:**

    * **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt-get update
        sudo apt-get install poppler-utils
        ```
    * **macOS (using Homebrew):**
        ```bash
        brew install poppler
        ```
    * **Windows:**
        1.  Download the Poppler for Windows binaries from a reliable source (e.g., [Poppler for Windows](https://blog.alivate.com.au/poppler-windows/)).
        2.  Extract the downloaded archive to a directory (e.g., `C:\poppler`).
        3.  Add the `bin` subdirectory (e.g., `C:\poppler\bin`) to your system's `PATH` environment variable.
        4.  Alternatively, you can set the `POPPLET_BIN_PATH` variable in `src/pdf_to_img.py` to the path of your Poppler `bin` directory. For example:
            ```python
            POPPLET_BIN_PATH = r"C:\poppler\bin" # Use raw string for backslashes
            ```

5.  **Configure Gemini API Key:**

    Set your Google API key as an environment variable named `GOOGLE_API_KEY`.
    You can create a `.env` file in the root directory of your project with the following content:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    And then load it in your `app.py` (though the provided code implicitly assumes it's set in the environment).

## Running the Application

1.  Ensure you have followed all installation and setup steps, especially for Poppler and your Gemini API key.
2.  Navigate to the root directory of the project in your terminal.
3.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
4.  Your browser will automatically open to the Streamlit app (usually at `http://localhost:8501`).

## Usage

1.  **Upload PDFs:** On the Streamlit interface, use the "Upload Invoice PDFs" button to select your invoice files.
2.  **Process Invoices:** Click the "Process Invoices" button. The application will convert PDFs to images, send them to Gemini for extraction, and flatten the data. A spinner will indicate that processing is underway.
3.  **Download Results:** Once processing is complete, a "Download Extracted Invoices CSV" button will appear. Click it to download your CSV file.
4.  **CSV Preview:** A preview of the first 10 rows of the generated CSV will be displayed below the download button.

## Important Notes

* **File Size & Quantity:** The application has a default limit of 20 PDF uploads, each not exceeding 1MB. These limits can be adjusted in `app.py` if needed.
* **Gemini API Quotas:** Be mindful of your Gemini API usage limits.
* **Accuracy:** While the Gemini Vision model is powerful, the accuracy of extraction can vary based on the quality and complexity of the invoice document.
* **Error Handling:** The application includes basic error handling for JSON decoding and file operations.

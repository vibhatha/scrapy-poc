import os
from pdf2docx import Converter
from docx2python import docx2python


DOCX_DIRECTORY = "docx"

def extract_pdf_text(pdf_file):
    """
    Extracts the text content from a PDF file.

    Args:
        pdf_file (str): The path to the PDF file.

    Returns:
        docx2python.DocxContent or None: The extracted text content as a DocxContent object,
            or None if an error occurred during the conversion.
    """
    
    print("Converting PDF to text...","PDF file: ", os.path.basename(pdf_file))
    cv = Converter(pdf_file)
    docx_file = pdf_file.replace(".pdf",".docx")
    docx_file = os.path.join(os.getcwd(), DOCX_DIRECTORY, os.path.basename(docx_file))

    # Check if the directory exists
    if not os.path.exists(DOCX_DIRECTORY):
        # If it doesn't exist, create it
        os.makedirs(DOCX_DIRECTORY)

    try:
        if not os.path.exists(docx_file):
            cv.convert(docx_file)

        docx_content = docx2python(docx_file)
        return docx_content
    
    except Exception as e:
        print(f"Error occurred during PDF to text conversion: {e}")
        return None
        
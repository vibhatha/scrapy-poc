import os
from extract_ministers_departments import extract_ministers_departments
from write_to_csv import write_to_csv
from crawl_pdfs import download_all_pdfs
from get_pdf_names import get_pdf_names


WEBSITE_URL = "http://www.cabinetoffice.gov.lk/cab/index.php?option=com_content&view=article&id=54&Itemid=93&lang=en"
PDF_DIRECTORY = "pdfs"
CSV_DIRECTORY = "extracted"

if __name__ == "__main__":
    try:
        download_all_pdfs(WEBSITE_URL, PDF_DIRECTORY)
        pdf_file_names = get_pdf_names(PDF_DIRECTORY)

        for pdf_file_name in pdf_file_names:
            # extract ministers and corresponding departments
            pdf_location = os.path.join(os.getcwd(), PDF_DIRECTORY, pdf_file_name)
            try:
                extracted_data = extract_ministers_departments(pdf_location)
                # writing to csv
                write_to_csv(extracted_data, pdf_file_name, CSV_DIRECTORY)
                extracted_data.clear()
            except Exception as e:
                print(f"Error processing PDF '{pdf_file_name}': {str(e)}")
                
    except Exception as e:
        print(f"Error occurred during PDF download: {str(e)}")

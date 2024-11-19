import csv
import re
import os

def write_to_csv(extracted_data, pdf_file_name, write_directory):
    """
    Write the extracted data to a CSV file.

    Args:
        extracted_data (dict): A dictionary containing the extracted data.
        pdf_file_name (str): The name of the PDF file.
        write_directory (str): The directory to write the CSV file.

    Returns:
        None
    """
    
    """Write the extracted data to a csv file"""
    write_directory = os.path.join(os.getcwd(), write_directory)

    x = re.findall('[0-9]+', pdf_file_name)
    # Check if the directory exists
    if not os.path.exists(write_directory):
        # If it doesn't exist, create it
        os.makedirs(write_directory)

    csv_name = f'gazette-{x[0]}-{x[1]}-{x[2]}.csv'
    csv_path = os.path.join(write_directory, csv_name)
    
    with open(csv_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        for ministry in extracted_data:
            for department in extracted_data[ministry]:
                row = [ministry, department]
                if "Departments, statutory institutions and public corporations" in department:
                    continue
                writer.writerow(row)
                
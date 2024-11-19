from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
import requests

def download_pdf(url, save_directory):
    """
    Downloads a PDF file from the given URL and saves it in the specified directory.

    Args:
        url (str): The URL of the PDF file to download.
        save_directory (str): The directory where the downloaded PDF file will be saved.
    """
    response = requests.get(url)
    file_name = os.path.join(save_directory, url.split("/")[-1])

    try:
        response.raise_for_status()  # Raises an exception for non-200 status codes
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"PDF downloaded successfully from {url}")

    except requests.HTTPError as e:
        print(f"Error downloading PDF from {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading PDF from {url}: {e}")
    finally:
        response.close()


def get_pdf_links(url):
    """
    Retrieves the links to PDF files from the given URL.

    Args:
        url (str): The URL from which to retrieve the PDF links.

    Returns:
        list: A list of PDF links.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []
    language = "E"
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith(str(language + '.pdf')):
            pdf_links.append(href)
    return pdf_links

def download_all_pdfs(url, save_directory):
    """
    Downloads all the PDF files from the given URL and saves them in the specified directory.

    Args:
        url (str): The URL from which to download the PDFs.
        save_directory (str): The directory where the downloaded PDFs will be saved.
    """
    save_directory = os.path.join(os.getcwd(), save_directory)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    domain_name = urlparse(url).scheme + "://" + urlparse(url).netloc
    
    pdf_links = get_pdf_links(url)
    print(f"Found {len(pdf_links)} PDFs to download.")

    for link in pdf_links:
        pdf_url = link if link.startswith('http') else domain_name + link
        print(f"Downloading {pdf_url}...")
        try: 
            download_pdf(pdf_url, save_directory)
        except Exception as e:
            print(f"Error downloading {pdf_url}: {e}")
    
    print("All PDFs downloaded successfully!")

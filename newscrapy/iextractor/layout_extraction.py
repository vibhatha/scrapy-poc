from openai import OpenAI
import asyncio
import json
import os
import glob


async def process_image(client, image_url, image_name):
    try:
        # Prepare system and user prompts
        system_prompt = "You are an assistant that extracts structured data from images."
        user_prompt = (
            "Please extract the table information in this image. First extract the minister responsible as 'Minister Responsible'."
            "Next extract lists of the 'Subjects and Functions', 'Departments, statutory institutions and public corporations', and 'Laws, acts and ordinances to be implemented' for each minister. "
            "Return the result in JSON format. Please only return the JSON data and nothing else."
            "Please don't include ```json``` like things, just written plain text in json format."
            """
            Formatting Guidelines:

            We need a single format for each file not various formats. And that format is as follows:
            Don't create arrays of the following data structure. Just return the data in the following format strictly:
            {
                "Minister Responsible": "string",
                "Subjects and Functions": ["string", "string"],
                "Departments": ["string", "string"],
                "Laws": ["string", "string"]
            }
            """
        )

        # Call the OpenAI API with image URL
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure you're using a vision-capable model
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ]
                }
            ]
        )

        # Print the response to understand its structure
        print("=" * 100)
        print(response)
        print("=" * 100)

        # Access the response content correctly
        chat_completion = response.choices[0].message.content
        
        # Save the chat completion to a file named after the image
        with open(f"staged_response/{image_name}_response.json", "w") as file:
            file.write(chat_completion)

    except Exception as e:
        print(f"Error processing image: {e}")
        raise e

# Function to process a list of image URLs
async def make_api_calls_and_save_responses(client, image_urls):
    for image_url in image_urls:
        image_name = os.path.basename(image_url).split('.')[0]  # Extract image name
        print(f"Processing image: {image_url}")
        await process_image(client, image_url, image_name)

def read_responses_and_combine_data(image_urls):
    combined_data = {}
    for image_url in image_urls:
        image_name = os.path.basename(image_url).split('.')[0]
        try:
            with open(f"{image_name}_response.json", "r") as file:
                chat_completion = file.read()

            # Parse the JSON response
            extracted_data = json.loads(chat_completion)

            print(extracted_data)

            # Combine the extracted data into a single JSON object
            for entry in extracted_data:
                minister = entry.get("Minister Responsible")
                if not minister:
                    continue

                if minister in combined_data:
                    # Merge the content for the same minister
                    combined_data[minister]["Subjects and Functions"].extend(entry.get("Subjects and Functions", []))
                    combined_data[minister]["Departments"].extend(entry.get("Departments", []))
                    combined_data[minister]["Laws"].extend(entry.get("Laws", []))
                else:
                    # Add new entry for the minister
                    combined_data[minister] = {
                        "Subjects and Functions": entry.get("Subjects and Functions", []),
                        "Departments": entry.get("Departments", []),
                        "Laws": entry.get("Laws", [])
                    }

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading or decoding JSON for image {image_url}: {e}")

    # Write the combined data to a JSON file
    with open("combined_extracted_data.json", "w") as file:
        json.dump(combined_data, file, indent=4)
    print("Combined data has been saved to combined_extracted_data.json")


def aggregate_json_files(file_pattern):
    # Initialize a dictionary to hold all the aggregated data
    aggregated_data = {}

    # Get all files that match the pattern (e.g., "data/*.json")
    json_files = sorted(glob.glob(file_pattern))

    for file_path in json_files:
        with open(file_path, 'r') as file:
            # Load JSON data from the file
            print("Processing ", file_path)
            data = json.load(file)

            # Process each entry in the file and aggregate by minister
            minister = data.get("Minister Responsible")
            if not minister:
                continue  # Skip files without a "Minister Responsible" field
            
            # Ensure we have a list initialized for each minister in aggregated_data
            if minister not in aggregated_data:
                aggregated_data[minister] = {"Subjects and Functions": [], "Departments": [], "Laws": []}

            # Check if the data contains a list of entries or individual values
            if isinstance(data, dict) and "Subjects and Functions" in data:
                # Handle a single object with 'Subjects and Functions', 'Departments', and 'Laws'
                aggregated_data[minister]["Subjects and Functions"].extend(data.get("Subjects and Functions", []))
                aggregated_data[minister]["Departments"].extend(data.get("Departments", []))
                aggregated_data[minister]["Laws"].extend(data.get("Laws", []))
            elif isinstance(data, list):
                # Handle a list of entries (objects) with these keys
                for entry in data:
                    aggregated_data[minister]["Subjects and Functions"].append(entry.get("Subjects and Functions"))
                    aggregated_data[minister]["Departments"].append(entry.get("Departments"))
                    aggregated_data[minister]["Laws"].extend(entry.get("Laws", []))
    return aggregated_data

def save_aggregated_data(aggregated_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(aggregated_data, file, indent=4)

async def process_images(client, image_urls):
    await make_api_calls_and_save_responses(client, image_urls)
    aggregated_data = aggregate_json_files("staged_response/*.json")
    save_aggregated_data(aggregated_data, "aggregated_data.json")
    print("Aggregated data has been saved to aggregated_data.json")

# Main function to initialize the OpenAI client and process images
async def main():
    client = OpenAI()

    # List of image URLs to process
    # Base URL path
    base_url = "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i"

    # Generate image URLs from 1 to 67, skipping 9
    image_urls = [f"{base_url}{i}.jpg" for i in range(1, 68) if i != 9]



    # Process each image
    await process_images(client, image_urls)



# Run the main function
asyncio.run(main())

import openai
import asyncio

# Define the function to process multiple images in a single query
async def process_multiple_images_in_single_query(client, image_urls):
    try:
        # System and user prompts
        system_prompt = "You are an assistant that extracts structured data from multiple images."
        user_prompt = """
        Guidelines:

        There are multiple images, and each image contains information about a minister or more. You
        need to learn about all these images and extract the information about the ministers, their subjects and functions, departments, and laws.
        The information must be read as it is. Don't summarize things. Please don't use etc or others like words. Extract all the information.

        I want to know the ministers, their subjects and functions, departments, and laws for each minister.
        Please extract the information from each of the images below. For each image, extract:
        - 'Minister Responsible'
        - Lists of 'Subjects and Functions', typically located in Column I
        - List 'Departments', typically located in Column II
        - List 'Laws', typically located in Column III
        Return the data in a readable format.
        """

        user_prompt = """
        What are the ministers found in the all the images? There will always be at least one minister in each image. Use this information to find the minister(s):
        - The minister begins with a number (example 1. Minister of Defence)
        - The minister is in the format "Minister of ..."
        - The minister is in bold
        - The minister is not found inside any table or columns

        You need to understand that the information for a minister can be in multiple images. So, you need to find all the images that contain information about a minister.
        Return to me a numbered list of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column return 'No subjects and functions' or 'No departments, statutory institutions and public corporations' or 'No laws, acts and ordinances to be implemented' respectively.
        """

        user_prompt = """
        The objective is to extract the information about each minister. The provided images contain information about ministers. 
        First identify the ministers. 
        For each minister there is a table and it has 3 columns, can you please extract each column with its heading and its content for each minister in a readable format with proper numbering, etc. 

        First identify the ministers. 
        Then clearly identify the pages required for each minister. 
        Then see the table format for each minister where, 

        Column I: Subjects and Functions
        Column II: Departments, Statutory Institutions and Public Corporations
        Column III: Laws, Acts and Ordinances to be Implemented

        Note that each minister content can be in multiple images. 

        Please refine the results using the following guideline.

        Please don't summarize things, put etc, or ... 
        Don't mix things from other columns
        """

        # Append each image URL to the user prompt
        for i, image_url in enumerate(image_urls, 1):
            user_prompt += f"{i}. {image_url}\n"

        # Send the query to OpenAI API with all images in one request
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure you're using a vision-capable model
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt}
                    ] + [
                        {"type": "image_url", "image_url": {"url": url}} for url in image_urls
                    ]
                }
            ]
        )

        # Access and print the response content
        chat_completion = response.choices[0].message.content
        print(chat_completion)

        # Save response to a file if needed
        with open("aggregated_response.txt", "w") as file:
            file.write(chat_completion)

    except Exception as e:
        print(f"Error processing images: {e}")
        raise e

# Main function to handle multiple images
async def main():
    client = openai.OpenAI()  # Initialize OpenAI client with your API key

    # List of image URLs to process in a single query
    image_urls = [
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i1.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i2.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i3.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i4.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i5.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i6.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i7.png",
        "https://github.com/vibhatha/scrapy-poc/raw/main/newscrapy/images/i8.png",
    ]

    # Process all images in a single query
    await process_multiple_images_in_single_query(client, image_urls)

# Run the main function
asyncio.run(main())

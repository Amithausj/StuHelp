import requests
from bs4 import BeautifulSoup

# Function to scrape the ITC pages
def get_itc_pages():
    base_url = "https://mgt.sjp.ac.lk/itc/"
    response = requests.get(base_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Successfully retrieved the page!")
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the text content of all paragraphs or divs
    # Update based on the structure of the website
    content = soup.find_all(['p', 'div'])  # Modify this based on which elements contain useful information

    if not content:
        print("No content found!")
    
    # Returning all the paragraph/div texts as a list
    return [element.get_text() for element in content]

# Function to search for an answer in the scraped data
def search_pages_for_answer(query, pages):
    query = query.lower()  # Case insensitive search
    answer = None

    # Check each page for the query
    for page in pages:
        if query in page.lower():  # Look for the query in the text (case insensitive)
            answer = page.strip()  # Return the first matching text
            break

    if not answer:
        return "Sorry, I couldn't find an answer to your question."

    return answer

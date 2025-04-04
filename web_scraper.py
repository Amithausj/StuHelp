import requests
from bs4 import BeautifulSoup
import re
import logging
import openai

# Setup logging for error handling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_openai_answer(query):
    """Fetch answer from OpenAI API (ChatGPT)"""
    try:
        # Make a request to OpenAI's GPT model (using GPT-3 or GPT-4 depending on your key)
        response = openai.Completion.create(
            model="text-davinci-003",  # Or use gpt-4 if available and preferred
            prompt=query,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        
        # Extract the response from the OpenAI API result
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        logger.error(f"Error fetching answer from OpenAI: {e}")
        return "❌ Sorry, there was an error retrieving the answer from OpenAI."

def get_itc_pages(base_url="https://mgt.sjp.ac.lk/itc/"):
    """Fetch the links from the ITC website"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(base_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        if href.startswith(base_url) or href.startswith("/itc/"):
            full_url = href if href.startswith("http") else base_url + href.replace("/itc/", "")
            links.add(full_url)
    logger.info(f"Found {len(links)} links on the site.")
    return list(links)

def search_pages_for_answer(query, urls):
    """Search the ITC pages for a matching answer"""
    for url in urls:
        try:
            logger.info(f"Searching on page: {url}")
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            if re.search(query, text, re.IGNORECASE):
                snippet = text[:500]
                logger.info(f"Answer found at {url}")
                return f"🔍 Answer found at: {url}\n\n{text[:500]}..."
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            continue
    return "❌ Sorry, I couldn't find any answer related to your question on the ITC site."

# Example usage:
if __name__ == "__main__":
    # Option 1: Use OpenAI API to answer a query
    user_query = "What is Business Information Systems?"  # Replace with actual query
    answer_from_openai = get_openai_answer(user_query)
    print(f"OpenAI Answer: {answer_from_openai}")

    # Option 2: Scrape ITC website for an answer
    links = get_itc_pages()
    query = "business information systems"  # Replace with the user's query
    answer_from_scraping = search_pages_for_answer(query, links)
    print(f"Scraped Answer: {answer_from_scraping}")

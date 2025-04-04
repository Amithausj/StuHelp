import requests
from bs4 import BeautifulSoup
import re

def get_itc_pages(base_url="https://mgt.sjp.ac.lk/itc/"):
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(base_url, verify=False)  # 👈 disable SSL verification
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        if href.startswith(base_url) or href.startswith("/itc/"):
            full_url = href if href.startswith("http") else base_url + href.replace("/itc/", "")
            links.add(full_url)
    return list(links)


def search_pages_for_answer(query, urls):
    """Search the ITC pages for a matching answer"""
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            if re.search(query, text, re.IGNORECASE):
                snippet = text[:500]
                return f"🔍 Answer found at: {url}\n\n{text[:500]}..."
        except:
            continue
    return "❌ Sorry, I couldn't find any answer related to your question on the ITC site."

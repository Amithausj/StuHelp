import streamlit as st
from web_scraper import get_itc_pages, search_pages_for_answer

# Function to interact with the user and give an answer
def chatbot(query):
    pages = get_itc_pages()  # Scrape the pages once
    
    if not pages:
        st.write("There was an error scraping the website or no content found.")
        return
    
    # Search for the answer to the query
    answer = search_pages_for_answer(query, pages)
    st.write(f"Answer: {answer}")

# Streamlit UI setup
st.title("Department of IT Chatbot")
query = st.text_input("Ask a question about the Department of IT or BSc in Business Information Systems:")

if query:
    chatbot(query)

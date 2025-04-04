import streamlit as st
from web_scraper import get_itc_pages, search_pages_for_answer

st.set_page_config(page_title="ITC Student Chatbot", layout="centered")
st.title("💬 ITC Student Chatbot")
st.markdown("Ask me anything about the Department of IT or the BSc in Business Information Systems degree!")

# Load ITC site links
@st.cache_data
def load_pages():
    return get_itc_pages()

pages = load_pages()

# Chat input
query = st.text_input("Your Question:", "")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Searching ITC site..."):
            answer = search_pages_for_answer(query, pages)
            st.success(answer)
    else:
        st.warning("Please enter a question to search.")

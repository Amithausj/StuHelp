import streamlit as st
import openai
from web_scraper import get_itc_pages, search_pages_for_answer

# Setup OpenAI API key
openai.api_key = "your-openai-api-key"  # Replace with your actual OpenAI API key

# Streamlit UI
st.title("Student Help Chatbot")
st.write("Ask your question related to the Department of IT or Business Information Systems!")

user_query = st.text_input("Enter your question:")

if user_query:
    with st.spinner('Fetching answer...'):
        # Get pages from ITC website
        pages = get_itc_pages()
        answer = search_pages_for_answer(user_query, pages)

        # Display the answer from search or OpenAI
        if answer == "❌ Sorry, I couldn't find any answer related to your question on the ITC site.":
            try:
                # Fallback to OpenAI if no answer found on ITC site
                response = openai.Completion.create(
                    engine="text-davinci-003",  # or other engines if needed
                    prompt=user_query,
                    max_tokens=150
                )
                openai_answer = response.choices[0].text.strip()
                st.write(f"🔍 OpenAI Answer: {openai_answer}")
            except Exception as e:
                st.error(f"An error occurred with OpenAI: {e}")
        else:
            st.write(f"🔍 ITC Site Answer: {answer}")

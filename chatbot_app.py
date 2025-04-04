import openai
import streamlit as st

# Set up your OpenAI API key
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
        return f"Error fetching answer from OpenAI: {e}"

# Streamlit app interface
def chatbot_interface():
    st.title("IT Department Chatbot")

    # Input box for user query
    user_query = st.text_input("Ask me anything related to the IT Department or the BSc in Business Information Systems Degree:")

    # Button to get the answer
    if st.button("Get Answer"):
        if user_query:
            # Fetch the answer from OpenAI API
            answer = get_openai_answer(user_query)
            st.write(f"**Answer**: {answer}")
        else:
            st.write("Please enter a question.")

# Run the chatbot
if __name__ == "__main__":
    chatbot_interface()

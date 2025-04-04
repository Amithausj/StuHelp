import streamlit as st
import pandas as pd
import os

# File path for storing chat history
HISTORY_FILE = "chat_history.csv"

# Load research data from CSV
@st.cache_data
def load_research_data():
    return pd.read_csv('research_data.csv')

# Search function
def search_research(query, df):
    query = query.lower()
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
    return filtered_df

# Load chat history from file
def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    else:
        return pd.DataFrame(columns=["Query", "Title", "Keywords", "Year", "Student", "Supervisor"])

# Save chat history to file
def save_chat_history(chat_history):
    chat_history.to_csv(HISTORY_FILE, index=False)

# Set page config
st.set_page_config(page_title="Research Chatbot", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color: darkblue;'>Department of Information Technology, FMSC, USJ</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>📚 Research Chatbot</h2>", unsafe_allow_html=True)

# Load data
df = load_research_data()

# Load chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# --- UI Layout ---
st.markdown("### 🔍 Ask about research topics:")
user_query = st.text_input("Enter your question:")

if st.button("Search"):
    if user_query:
        results = search_research(user_query, df)
        
        if results.empty:
            st.error("❌ No matching research found.")
            new_entry = pd.DataFrame([[user_query, "No Results", "", "", "", ""]], 
                                     columns=["Query", "Title", "Keywords", "Year", "Student", "Supervisor"])
        else:
            results.insert(0, "Query", user_query)
            new_entry = results

        # Append new results to history and save
        st.session_state.chat_history = pd.concat([new_entry, st.session_state.chat_history], ignore_index=True)
        save_chat_history(st.session_state.chat_history)

# --- Display Chat History in Table Format ---
st.markdown("---")
st.markdown("### 🗂️ Chat History")
if not st.session_state.chat_history.empty:
    st.dataframe(st.session_state.chat_history)
else:
    st.info("Chat history is empty. Start searching!")

# --- Clear History Button ---
if st.button("Clear History"):
    # Clear session state and history file
    st.session_state.chat_history = pd.DataFrame(columns=["Query", "Title", "Keywords", "Year", "Student", "Supervisor"])
    save_chat_history(st.session_state.chat_history)
    st.success("Chat history has been cleared!")

# Footer
st.markdown("<hr><p style='text-align: center;'>© 2025 : Department of Information Technology, FMSC, USJ</p>", unsafe_allow_html=True)

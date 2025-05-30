# This script preprocesses local PDF files, extracts text, cleans it, and saves the combined text to a file.
#later we use this combined_text.txt file to ask questions to the Gemini model
# app.py - Streamlit application for Västtrafik PartilleBot
import streamlit as st
import time
import pandas as pd
import os
from gemini_api import ask_gemini  

# ---------------------- CONFIGURATION ----------------------
st.set_page_config(
    page_title="Västtrafik PartilleBot",
    page_icon="🚌",
    layout="centered"
)

# ---------------------- STYLING ----------------------p
# This will style the input box, buttons, and headers
#Color scheme: Blue (#003DA5) and light background (#f0f6ff)
# This CSS will apply a blue theme to the input box, buttons, and headers
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border: 2px solid #003DA5;
        border-radius: 8px;
        color: #003DA5;
    }
    .stButton > button {
        border-radius: 8px;
        background-color: #003DA5;
        color: white;
        font-weight: bold;
        padding: 0.5em 1em;
    }
    .stButton > button:hover {
        background-color: #005BAC;
        color: white;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #003DA5;
    }
    .stSidebar {
        background-color: #f0f6ff;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- LOAD CONTEXT ----------------------
# Load the preprocessed text from combined_text.txt

@st.cache_data
def load_combined_text():
    with open("combined_text.txt", "r", encoding="utf-8") as f:
        return f.read()

if "context" not in st.session_state:
    st.session_state["context"] = load_combined_text()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ---------------------- SIDEBAR INFO ----------------------

st.sidebar.title("ℹ️ About")
st.sidebar.info("""
**Västtrafik PartilleBot** helps you with questions about:
- 🚌 Local buses in Partille
- ⏰ Timings, stops & information  
📍 Based on Västtrafik documents  
🧠 Powered by Gemini API  
""")

# ---------------------- HEADER ----------------------

st.title("🚌 Västtrafik PartilleBot")
st.subheader("Ask me about Partille bus timings and transport information!")
st.divider()

# ---------------------- USER INPUT ----------------------
question = st.text_input("❓ Ask your question here:")

if st.button("🔍 Search"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("💡 Gemini is thinking..."):
            start = time.time()
            answer = ask_gemini(st.session_state["context"], question)
            end = time.time()

        # Store Q&A in session history
        st.session_state["chat_history"].append((question, answer))

        # Show Answer
        st.success("✅ Here's the answer:")
        st.markdown(f"{answer}")
        st.caption(f"⏱️ Response time: {end - start:.2f} seconds")

        # Feedback section
        with st.expander("💬 Give Feedback on this Answer"):
            feedback = st.radio("Was this answer helpful?", ["👍 Yes", "👎 No"], key=f"feedback_{question}")
            if st.button("📨 Submit Feedback", key=f"submit_{question}"):
                def save_feedback(question, answer, feedback):
                    df = pd.DataFrame([{
                        "question": question,
                        "answer": answer,
                        "feedback": feedback
                    }])
                    if os.path.exists("feedback.csv"):
                        df.to_csv("feedback.csv", mode='a', header=False, index=False)
                    else:
                        df.to_csv("feedback.csv", mode='w', header=True, index=False)
                save_feedback(question, answer, feedback)
                st.success("🙌 Thanks for your feedback!")


import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    st.error("⚠️ Please set the GROQ_API_KEY environment variable before running.")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# =======================
# Streamlit UI
# =======================
st.title("🧠 Personal AI Agent (Groq + DuckDuckGo + PDF)")

option = st.sidebar.selectbox(
    "Choose Function",
    [
        "Summarize Passage",
        "Word Meaning with Examples",
        "Write Essay",
        "Solve Math/Aptitude/Reasoning",
        "Banking Exam Q&A",
        "Current Affairs & General Awareness",
        "PDF Summarizer & Q&A",
    ],
)

# =======================
# Helper Functions
# =======================


def groq_query(prompt_text, max_tokens=300, model="llama-3.3-70b-versatile"):
    """Send query to Groq API and return response text."""
    messages = [
        {"role": "system", "content": "You are a capable assistant."},
        {"role": "user", "content": prompt_text},
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_completion_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def search_ddg(query, max_results=3):
    """Search DuckDuckGo and return results list."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)
    return results


# =======================
# Features
# =======================

if option == "Summarize Passage":
    passage = st.text_area("Enter passage to summarize")
    if st.button("Summarize"):
        summary = groq_query(f"Summarize the following passage in brief:\n{passage}")
        st.write(summary)

elif option == "Word Meaning with Examples":
    word = st.text_input("Enter a word")
    if st.button("Get Meaning"):
        meaning = groq_query(
            f"Provide meaning of the word '{word}' with suitable examples in English and Hindi."
        )
        st.write(meaning)

elif option == "Write Essay":
    topic = st.text_input("Enter essay topic")
    if st.button("Write Essay"):
        essay = groq_query(f"Write a 150 words essay on the topic: {topic}.")
        st.write(essay)

elif option == "Solve Math/Aptitude/Reasoning":
    question = st.text_area("Enter your math/aptitude/reasoning question")
    if st.button("Solve"):
        answer = groq_query(f"Solve and provide answer: {question}")
        st.write(answer)
    if st.button("Explain"):
        explanation = groq_query(f"Explain the solution step-by-step for: {question}")
        st.write(explanation)

elif option == "Banking Exam Q&A":
    topic = st.text_input("Enter banking exam topic (e.g., SBI PO, IBPS PO)")
    if st.button("Get Q&A"):
        qna = groq_query(
            f"Provide multiple practice questions and answers for banking exams on the topic: {topic}."
        )
        st.write(qna)

elif option == "Current Affairs & General Awareness":
    query = st.text_input("Type topic or question related to current affairs")
    if st.button("Fetch Current Affairs"):
        results = search_ddg(query, max_results=3)
        st.write("### 🌍 Latest info from web:")
        for res in results:
            st.markdown(f"- [{res['title']}]({res['href']})  \n{res['body']}")

elif option == "PDF Summarizer & Q&A":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in pdf_reader.pages:
            txt = page.extract_text()
            if txt:
                full_text += txt + "\n"

        st.write("📄 Extracted text preview:")
        st.write(full_text[:1000] + "..." if len(full_text) > 1000 else full_text)

        if st.button("Summarize PDF"):
            pdf_summary = groq_query(
                f"Summarize the following PDF text content:\n{full_text}"
            )
            st.write(pdf_summary)

        user_q = st.text_input("Ask a question about this PDF")
        if st.button("Ask PDF"):
            answer = groq_query(
                f"Answer the following question based on PDF:\n\nPDF: {full_text}\n\nQ: {user_q}"
            )
            st.write(answer)

# =======================
# Footer
# =======================
st.sidebar.markdown("---")
st.sidebar.markdown(
    "🚀 Powered by **Groq API (Llama 3)** + **DuckDuckGo Search** + **Streamlit**"
)

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import tempfile

load_dotenv()

def main():
    st.set_page_config(page_title="📊 Pergunte ao seu CSV")
    st.header("🔍 RAG com CSV e Gemini")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("🔑 Chave da API do Gemini não encontrada! Configure no .env")
        return

    csv_file = st.file_uploader("📂 Faça o upload de um arquivo CSV", type="csv")

    if csv_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(csv_file.getbuffer())
            temp_file_path = temp_file.name

        llm = GoogleGenerativeAI(model="gemini-1.5-pro-002", google_api_key=google_api_key)
        agent = create_csv_agent(llm, temp_file_path, verbose=True, allow_dangerous_code=True)

        user_question = st.text_input("💬 Faça uma pergunta sobre seu CSV:")

        if user_question:
            with st.spinner("🔎 Buscando resposta..."):
                resposta = agent.run(f"Responda em português: {user_question}")
                st.write("✅ Resposta:")
                st.write(resposta)

if __name__ == "__main__":
    main()
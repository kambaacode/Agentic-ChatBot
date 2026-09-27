import os
import streamlit as st

from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_control_inputs):
        self.user_controls = user_control_inputs

    def get_llm(self):
        try:
            GROQ_API_KEY = self.user_controls["GROQ_API_KEY"]
            selected_groq_model = self.user_controls["selected_groq_model"]
            if not GROQ_API_KEY:
                st.error("Please enter Groq api key")

            llm = ChatGroq(api_key= GROQ_API_KEY, model= selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occured with Exception: {e}")

        return llm
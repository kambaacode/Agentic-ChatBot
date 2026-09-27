import os

import requests
import streamlit as st

from src.ui.config import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    # ------------------------------------------------------------------
    # Page shell
    # ------------------------------------------------------------------
    def load_streamlit_ui(self):
        st.set_page_config(
            page_title=self.config.get_page_title(),
            page_icon="🕸️",
            layout="wide",
        )
        self._inject_css()

        st.markdown(
            f"<h1 class='app-title'>🕸️ {self.config.get_page_title()}</h1>",
            unsafe_allow_html=True,
        )
        st.caption("Configure your model and use case in the sidebar to get started.")
        st.divider()

        with st.sidebar:
            st.markdown("### ⚙️ Configuration")
            st.divider()

            self._render_llm_section()
            st.divider()
            self._render_usecase_section()

            st.divider()
            self._render_footer()

        return self.user_controls

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------
    def _render_llm_section(self):
        st.markdown("**🧠 Model provider**")
        llm_options = self.config.get_llm_options()
        selected_llm = st.selectbox(
            "Select LLM",
            llm_options,
            label_visibility="collapsed",
            help="Choose which provider serves the chat model.",
        )
        self.user_controls["selected_llm"] = selected_llm

        if selected_llm == "Groq":
            self._render_groq_controls()
        elif selected_llm == "Ollama":
            self._render_ollama_controls()

    def _render_groq_controls(self):
        with st.container(border=True):
            groq_model_options = self.config.get_groq_model_options()
            self.user_controls["selected_groq_model"] = st.selectbox(
                "Model", groq_model_options, help="Groq-hosted model to use for this session."
            )

            groq_api_key = st.text_input(
                "API key",
                type="password",
                placeholder="gsk_...",
                help="Your key is kept only in this browser session, never written to disk.",
            )
            self.user_controls["GROQ_API_KEY"] = groq_api_key
            st.session_state["GROQ_API_KEY"] = groq_api_key

            if not groq_api_key:
                st.warning("⚠️ Enter your Groq API key to proceed.", icon="⚠️")
            else:
                st.success("Groq API key set.", icon="✅")

    def _render_ollama_controls(self):
        with st.container(border=True):
            ollama_model_options = self.config.get_ollama_model_options()
            self.user_controls["selected_ollama_model"] = st.selectbox(
                "Model", ollama_model_options, help="Model must already be pulled locally (`ollama pull <model>`)."
            )

            base_url = st.text_input(
                "Ollama server URL",
                value=st.session_state.get("OLLAMA_BASE_URL", "http://localhost:11434"),
                help="Use http://localhost:11434 if Streamlit and Ollama run on the same "
                     "machine, or the laptop's IP/tunnel address if not.",
            )
            self.user_controls["OLLAMA_BASE_URL"] = base_url
            st.session_state["OLLAMA_BASE_URL"] = base_url

            self._render_ollama_status(base_url)

    def _render_ollama_status(self, base_url: str):
        reachable = self._is_ollama_reachable(base_url)
        if reachable:
            st.success(f"Connected to Ollama at `{base_url}`.", icon="✅")
        else:
            st.error(
                f"Can't reach Ollama at `{base_url}`. Is `ollama serve` running, "
                "and reachable from here?",
                icon="🚫",
            )

    def _render_usecase_section(self):
        st.markdown("**🎯 Use case**")
        usecase_options = self.config.get_usecase_options()
        self.user_controls["selected_usecase"] = st.selectbox(
            "Select Usecase", usecase_options, label_visibility="collapsed"
        )

    def _render_footer(self):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col2:
            st.link_button(
                "📘 LangGraph docs",
                "https://langchain-ai.github.io/langgraph/",
                use_container_width=True,
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _is_ollama_reachable(base_url: str) -> bool:
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def _inject_css():
        st.markdown(
            """
            <style>
            .app-title { margin-bottom: 0rem; }
            section[data-testid="stSidebar"] div.stButton button {
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
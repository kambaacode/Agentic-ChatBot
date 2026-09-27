import requests
import streamlit as st

from langchain_ollama import ChatOllama


class OllamaLLM:
    def __init__(self, user_control_inputs, base_url: str = "http://localhost:11434"):
        """
        base_url:
            - "http://localhost:11434" if Streamlit and Ollama run on the SAME machine.
            - "http://<laptop-ip-or-tunnel>:11434" if Streamlit runs elsewhere and
              needs to reach Ollama on your laptop over the network/tunnel.
        """
        self.user_controls = user_control_inputs
        self.base_url = base_url

    def _is_ollama_reachable(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_llm(self):
        try:
            selected_ollama_model = self.user_controls["selected_ollama_model"]

            if not self._is_ollama_reachable():
                st.error(
                    f"Can't reach Ollama at {self.base_url}. "
                    "Make sure Ollama is running (`ollama serve`) and, if Streamlit "
                    "is on a different machine, that OLLAMA_HOST=0.0.0.0 is set and "
                    "the address/port is reachable from here."
                )
                st.stop()

            llm = ChatOllama(base_url=self.base_url, model=selected_ollama_model)

        except Exception as e:
            raise ValueError(f"Error occurred with Exception: {e}")

        return llm
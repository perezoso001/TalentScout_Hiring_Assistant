from huggingface_hub import InferenceClient
import streamlit as st

# Use HF_TOKEN in Streamlit secrets
hf_token = st.secrets["HF_TOKEN"]

# Reliable free model that works on Inference Providers
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",  # ← This one is guaranteed to work free
    token=hf_token
)

# Fallback options (uncomment if you want to try):
# model="Qwen/Qwen2.5-7B-Instruct"
# model="HuggingFaceTB/SmolLM2-1.7B-Instruct"


def get_llm_response(messages: list[dict]) -> str:
    """
    Send full message history to the LLM and return response.
    """
    try:
        response = client.chat.completions.create(
            messages=messages,        # Full history including system prompt
            max_tokens=600,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Friendly fallback so app doesn't crash
        return f"Sorry, the language model is temporarily unavailable. Please try again. (Error: {str(e)})"
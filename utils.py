from huggingface_hub import InferenceClient
import streamlit as st

# Use the secret name consistently (you can choose one – I'll use "HF_TOKEN")
# In Streamlit Cloud secrets, add: HF_TOKEN = hf_your_token_here
hf_token = st.secrets["HF_TOKEN"]

# Initialize the client with a fully FREE and reliable model
client = InferenceClient(
    model="microsoft/Phi-3.5-mini-instruct",  # 100% free, fast, and excellent for chat
    token=hf_token
)

# Alternative free models you can swap in (uncomment one if you prefer):
# model="Qwen/Qwen2.5-7B-Instruct"           # Very strong, multilingual
# model="mistralai/Mistral-7B-Instruct-v0.3" # Classic reliable choice
# model="google/gemma-2-9b-it"               # Also free and capable


def get_llm_response(messages: list[dict]) -> str:
    """
    Send messages to the LLM and return the assistant's response.
    messages: list of dicts with 'role' and 'content' (system, user, assistant)
    """
    try:
        response = client.chat.completions.create(
            messages=messages,       # Pass the full message history directly
            max_tokens=600,          # Good length for technical answers
            temperature=0.3,         # Low for consistent, professional responses
            # stop=["</s>"]          # Optional: some models use this
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Graceful fallback – important for demo stability
        st.error("LLM temporarily unavailable. Please try again.")
        return f"Sorry, I couldn't connect to the language model right now. (Error: {str(e)})"
from huggingface_hub import InferenceClient
import streamlit as st

# Load token from secrets
hf_token = st.secrets["HF_TOKEN"]

# Free, fast, and fully supported chat model on HF Inference API
client = InferenceClient(
    model="google/gemma-2-2b-it",  # ← This works reliably for chat completion (free tier)
    token=hf_token
)

# Other free alternatives if you want to try (uncomment one):
# model="HuggingFaceTB/SmolLM2-1.7B-Instruct"  # Very small & fast
# model="Qwen/Qwen2-7B-Instruct"              # If available on your account


def get_llm_response(messages: list[dict]) -> str:
    """
    Send full conversation history to the LLM and get response.
    """
    try:
        response = client.chat.completions.create(
            messages=messages,
            max_tokens=800,          # Enough for detailed questions
            temperature=0.3,         # Consistent responses
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Better error message for demo
        return f"Sorry, the model is busy or unavailable right now. Please try again in a moment. (Technical: {str(e)[:100]})"
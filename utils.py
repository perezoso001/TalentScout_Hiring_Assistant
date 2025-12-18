from huggingface_hub import InferenceClient
import streamlit as st

hf_api_key = st.secrets["huggingface_api_key"]

# No need for provider= – it picks the best one automatically!
client = InferenceClient(token=hf_api_key)

def get_llm_response(messages):
    # Extract system and user parts (flan-t5 style was simple, but now we use real chat!)
    system_content = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
    user_content = next((msg["content"] for msg in messages if msg["role"] == "user"), "")

    # Make proper chat messages list
    chat_messages = []
    if system_content:
        chat_messages.append({"role": "system", "content": system_content})
    chat_messages.append({"role": "user", "content": user_content})

    # Use the awesome chat mode (way smarter than old text_generation!)
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",  # Super smart & free to try!
        # Other good free ones: "mistralai/Mistral-7B-Instruct-v0.3" or "Qwen/Qwen2.5-7B-Instruct"
        messages=chat_messages,
        max_tokens=500,  # Longer answers
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
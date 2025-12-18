import streamlit as st
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT
from utils import get_llm_response

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

st.title("🤖 TalentScout Hiring Assistant")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! 👋 I'm TalentScout. I'll help with your initial screening. Let's start. What is your full name?"}
    ]

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

# Display chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your response here...")

EXIT_WORDS = ["exit", "quit", "bye", "stop"]

if user_input:
    if user_input.lower() in EXIT_WORDS:
        st.chat_message("assistant").write(
            "Thank you for your time! 🎉 Our team will review your profile and get back to you soon."
        )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Determine next step
    collected = st.session_state.candidate_data

    if "name" not in collected:
        collected["name"] = user_input
        reply = "Thanks! What's your email address?"

    elif "email" not in collected:
        collected["email"] = user_input
        reply = "Great. Please share your phone number."

    elif "phone" not in collected:
        collected["phone"] = user_input
        reply = "How many years of experience do you have?"

    elif "experience" not in collected:
        collected["experience"] = user_input
        reply = "Which position are you applying for?"

    elif "position" not in collected:
        collected["position"] = user_input
        reply = "Where are you currently located?"

    elif "location" not in collected:
        collected["location"] = user_input
        reply = "Please list your tech stack (languages, frameworks, databases, tools)."

    elif "tech_stack" not in collected:
        collected["tech_stack"] = user_input

        prompt = TECH_QUESTION_PROMPT.format(tech_stack=user_input)
        llm_response = get_llm_response([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])

        reply = f"Thanks! Here are your technical questions:\n\n{llm_response}\n\nYou may type 'exit' when done."

    else:
        reply = "Thank you! Our team will reach out if there's a next step. 😊"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

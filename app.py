import streamlit as st
import re
from utils import get_llm_response
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT

# ------------------- Validation Helpers -------------------
def is_valid_email(email: str) -> bool:
    if not email or not email.strip():
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email.strip()) is not None

def is_valid_phone(phone: str) -> bool:
    if not phone or not phone.strip():
        return False
    # Allows digits, spaces, +, -, (), typical international formats
    pattern = r'^[\d\s\+\-\(\)]{7,20}$'
    return re.match(pattern, phone.strip()) is not None

def is_valid_experience(exp: str) -> bool:
    if not exp or not exp.strip():
        return False
    try:
        years = float(exp.strip())
        return 0 <= years <= 50
    except ValueError:
        return False

def is_non_empty(text: str) -> bool:
    return bool(text and text.strip())

# ------------------- Session State Initialization -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

if "current_step" not in st.session_state:
    st.session_state.current_step = "name"  # Start here

# Exit keywords
EXIT_WORDS = ["exit", "quit", "bye", "stop", "done"]

# ------------------- Title & Greeting -------------------
st.title("TalentScout Hiring Assistant 🤖")
st.markdown("I'm here to screen you for tech positions. I'll collect your info and ask some technical questions. Let's begin!")

# Display initial greeting if conversation is empty
if not st.session_state.messages:
    greeting = "Hello! What's your full name?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------- User Input -------------------
if user_input := st.chat_input("Your response..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for exit first
    if any(word in user_input.lower() for word in EXIT_WORDS):
        response = "Thank you for your time! Our team will review your profile and get back to you soon. Goodbye! 👋"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.stop()  # End the app gracefully

    # Check for restart
    if user_input.lower().strip() == "restart":
        st.session_state.current_step = "name"
        st.session_state.candidate_data = {}
        response = "Conversation restarted! What's your full name?"
    else:
        current_step = st.session_state.current_step

        # ------------------- Step-by-Step Validation & Progression -------------------
        if current_step == "name":
            if is_non_empty(user_input):
                st.session_state.candidate_data["name"] = user_input.strip()
                response = "Nice to meet you! What's your email address?"
                st.session_state.current_step = "email"
            else:
                response = "I didn't catch that. Could you please tell me your full name?"

        elif current_step == "email":
            if is_valid_email(user_input):
                st.session_state.candidate_data["email"] = user_input.strip()
                response = "Got it! What's your phone number? (e.g., +123 456 7890)"
                st.session_state.current_step = "phone"
            else:
                response = "That doesn't look like a valid email. Could you please provide a correct email address?"

        elif current_step == "phone":
            if is_valid_phone(user_input):
                st.session_state.candidate_data["phone"] = user_input.strip()
                response = "Thanks! How many years of professional experience do you have?"
                st.session_state.current_step = "experience"
            else:
                response = "Hmm, that phone number seems invalid. Please try again (e.g., +91 98765 43210)."

        elif current_step == "experience":
            if is_valid_experience(user_input):
                st.session_state.candidate_data["experience"] = user_input.strip()
                response = "Great! What position(s) are you interested in? (e.g., Full Stack Developer)"
                st.session_state.current_step = "position"
            else:
                response = "Please enter a valid number (e.g., 3 or 5.5). How many years of experience do you have?"

        elif current_step == "position":
            if is_non_empty(user_input):
                st.session_state.candidate_data["position"] = user_input.strip()
                response = "Where are you currently located? (City, Country)"
                st.session_state.current_step = "location"
            else:
                response = "I didn't get that. What position(s) are you applying for?"

        elif current_step == "location":
            if is_non_empty(user_input):
                st.session_state.candidate_data["location"] = user_input.strip()
                response = "Perfect! What is your tech stack? List languages, frameworks, databases, tools, etc. (e.g., Python, Django, React, PostgreSQL)"
                st.session_state.current_step = "tech_stack"
            else:
                response = "Please tell me your current location (e.g., Bangalore, India)."

        elif current_step == "tech_stack":
            if is_non_empty(user_input):
                st.session_state.candidate_data["tech_stack"] = user_input.strip()
                # Generate technical questions using LLM
                prompt = get_step_prompt("generate_questions", st.session_state.candidate_data)
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
                response = get_llm_response(messages)
                response += "\n\nPlease answer them one by one. Type 'exit' when done."
                st.session_state.current_step = "answering_questions"
            else:
                response = "I need your tech stack to generate questions. Please list your skills (e.g., Java, Spring Boot, AWS)."

        elif current_step == "answering_questions":
            # During Q&A phase, just echo and continue (or optionally evaluate with LLM)
            response = "Thank you for your answer! Feel free to answer the next question or type 'exit' when finished."

        else:
            response = "Let's continue — please provide the requested information."

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
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
    st.session_state.current_step = "name"

# Exit keywords
EXIT_WORDS = ["exit", "quit", "bye", "stop", "done"]

# ------------------- UI Setup -------------------
st.title("TalentScout Hiring Assistant 🤖")
st.markdown("Hi! I'm here to help screen you for tech roles. I'll collect your details and ask some technical questions based on your skills.")

# Initial greeting
if not st.session_state.messages:
    greeting = "Let's get started! What's your full name?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------- User Input -------------------
if user_input := st.chat_input("Type your response here..."):

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for exit keywords first
    if any(word in user_input.lower() for word in EXIT_WORDS):
        response = "Thank you for your time! Your profile has been recorded. Our team will review it and get back to you soon. Have a great day! 👋"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.stop()

    # Check for restart
    if user_input.lower().strip() == "restart":
        st.session_state.current_step = "name"
        st.session_state.candidate_data = {}
        response = "Conversation restarted! What's your full name?"
    else:
        current_step = st.session_state.current_step

        # ------------------- Step-by-Step Flow with Validation -------------------
        if current_step == "name":
            if is_non_empty(user_input):
                st.session_state.candidate_data["name"] = user_input.strip()
                response = "Nice to meet you, {}! What's your email address?".format(user_input.strip())
                st.session_state.current_step = "email"
            else:
                response = "I didn't catch your name. Could you please tell me your full name?"

        elif current_step == "email":
            if is_valid_email(user_input):
                st.session_state.candidate_data["email"] = user_input.strip()
                response = "Thanks! What's your phone number? (e.g., +123 456 7890)"
                st.session_state.current_step = "phone"
            else:
                response = "That doesn't seem like a valid email. Could you please enter a correct one?"

        elif current_step == "phone":
            if is_valid_phone(user_input):
                st.session_state.candidate_data["phone"] = user_input.strip()
                response = "Got it! How many years of professional experience do you have?"
                st.session_state.current_step = "experience"
            else:
                response = "That phone number looks invalid. Please try again (e.g., +91 9876543210)."

        elif current_step == "experience":
            if is_valid_experience(user_input):
                st.session_state.candidate_data["experience"] = user_input.strip()
                response = "Great! What position(s) are you interested in? (e.g., Full Stack Developer, Data Engineer)"
                st.session_state.current_step = "position"
            else:
                response = "Please enter a valid number of years (e.g., 3 or 4.5). How many years of experience do you have?"

        elif current_step == "position":
            if is_non_empty(user_input):
                st.session_state.candidate_data["position"] = user_input.strip()
                response = "Where are you currently located? (e.g., Bangalore, India)"
                st.session_state.current_step = "location"
            else:
                response = "I didn't catch that. What position are you applying for?"

        elif current_step == "location":
            if is_non_empty(user_input):
                st.session_state.candidate_data["location"] = user_input.strip()
                response = "Perfect! Now, please list your tech stack (languages, frameworks, databases, tools you're proficient in).\nExample: Python, Django, React, PostgreSQL, AWS"
                st.session_state.current_step = "tech_stack"
            else:
                response = "Please tell me your current location (e.g., Mumbai, India)."

        elif current_step == "tech_stack":
            if is_non_empty(user_input):
                st.session_state.candidate_data["tech_stack"] = user_input.strip()

                # Generate technical questions directly
                tech_stack = st.session_state.candidate_data["tech_stack"]
                generate_prompt = f"""
You are an expert technical interviewer.
The candidate is proficient in: {tech_stack}

Generate 3–5 relevant and challenging technical questions to assess their real proficiency.
Cover the main technologies mentioned.
Make questions practical and scenario-based where possible.
Format as a clean numbered list only — no intro or extra text.
Example:
1. Explain how Django's ORM handles relationships...
2. What are React Hooks and when would you use useEffect?
"""

                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": generate_prompt}
                ]
                response = get_llm_response(messages)

                # Fallback if LLM fails
                if "unavailable" in response.lower() or len(response.strip()) < 20:
                    response = f"Here are some sample questions based on your tech stack ({tech_stack}):\n\n1. Explain the difference between lists and tuples in Python.\n2. How does Django handle user authentication?\n3. What is virtual DOM in React?\n4. Write a basic SQL query to join two tables.\n5. Describe REST API principles."

                response += "\n\nPlease answer them one by one. When you're done, type 'exit'."
                st.session_state.current_step = "answering_questions"
            else:
                response = "I need your tech stack to generate questions. Please list your skills (e.g., JavaScript, Node.js, MongoDB)."

        elif current_step == "answering_questions":
            response = "Thank you for your answer! You can continue with the next question or type 'exit' when finished."

        else:
            response = "Let's get back on track. Please provide the requested information."

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
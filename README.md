# 🤖 TalentScout Hiring Assistant

An intelligent hiring assistant chatbot built using Streamlit and Hugging Face LLMs.
The chatbot performs initial candidate screening by collecting essential details
and generating technical questions based on the candidate’s declared tech stack.

---

## 🚀 Features
- Interactive chat-based UI
- Step-by-step candidate information collection
- Dynamic technical question generation
- Context-aware conversation flow
- Secure API key handling using Streamlit secrets
- Graceful conversation termination

---

## 🛠️ Tech Stack
- Python
- Streamlit
- Hugging Face Inference API (Mistral-7B-Instruct)
- Prompt Engineering

---

## 📂 Project Structure
```plaintext
TalentScout_Hiring_Assistant/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions and LLM logic
├── prompts.py          # Prompt templates and engineering
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── .streamlit/
    └── secrets.toml    # Local secrets (API keys) - gitignored
```
---

## ⚙️ Installation & Setup

```bash
git clone <your-repo-url>
cd TalentScout_Hiring_Assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Create .streamlit/secrets.toml:

huggingface_api_key = "your_hf_token"


Run the app:

streamlit run app.py

---

## Live Demo
The chatbot is deployed on Streamlit Community Cloud:  
🔗 [Click here to try it live](https://talentscouthiringassistant-hawgdwl385hct55x7wwqf3.streamlit.app/)
	Demo video Link: https://www.loom.com/share/f3ff8cac79114c639e89b1a5f0aa1e2c

## Features Implemented
- Greeting and purpose explanation
- Step-by-step collection of candidate info (name, email, phone, experience, position, location, tech stack)
- LLM-powered generation of 3–5 technical questions based on tech stack
- Context-aware conversation using message history
- Graceful exit on keywords ("bye", "exit", "done")
- Fallback for unclear inputs
- Deployed publicly for demo

## Technologies Used
- Frontend: Streamlit
- LLM: Hugging Face Inference API (google/gemma-2-2b-it)
- Libraries: huggingface_hub, streamlit

## Deployment
Deployed on Streamlit Community Cloud (free tier) for live access.
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
TalentScout_Hiring_Assistant/
│
├── app.py
├── utils.py
├── prompts.py
├── requirements.txt
├── README.md
└── .streamlit/
└── secrets.toml

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

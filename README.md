# 🎯 AI Job Description Analyser

> LLM-powered resume-job fit analyser built with Groq (Llama 3), LangChain, and Streamlit

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](YOUR_LIVE_LINK_HERE)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3-F55036?style=for-the-badge)](https://groq.com)

---

## 🚀 What It Does

Upload your resume PDF + paste any job description → get instant AI-powered analysis:

- 📊 **Match Score** — 0-100% fit score
- ✅ **Matched Skills** — what you already have
- ❌ **Missing Skills** — what to learn next
- 💪 **Your Strengths** — standout qualities
- 🎯 **Recommendations** — actionable next steps
- 🧠 **AI Verdict** — overall hiring probability

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| LLM | Groq API (Llama 3.3 70B) |
| Framework | LangChain |
| Frontend | Streamlit |
| PDF Processing | PyPDF2 |
| Environment | python-dotenv |

---

## ⚙️ How It Works

1. User uploads resume as PDF
2. PyPDF2 extracts and chunks the text
3. User pastes job description
4. LangChain + Groq (Llama 3) analyses the fit
5. Results displayed in under 5 seconds

---

## 🏃 Run Locally
```bash
# Clone the repo
git clone https://github.com/raam214/ai-job-description-analyser
cd ai-job-description-analyser

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
# Create .env file and add:
# GROQ_API_KEY=your_key_here

# Run
streamlit run app.py
```

---

## 🔑 Get Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create API Key
4. Add to `.env` file

---

## 📁 Project Structure
```
ai-job-description-analyser/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
├── .env               # API key (not committed)
├── .gitignore         # Ignores .env and venv
└── README.md          # This file
```

---

Built by **Ram Dukare** · Powered by Groq (Llama 3) · LangChain · Streamlit
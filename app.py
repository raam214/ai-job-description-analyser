import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── PAGE CONFIG
st.set_page_config(
    page_title="AI Job Description Analyser",
    page_icon="🎯",
    layout="wide"
)

# ── CUSTOM CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); }
    .hero-title {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.3rem;
    }
    .hero-sub {
        text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border-radius: 16px; padding: 1.5rem;
        border: 1px solid #2d3450; text-align: center;
    }
    .score-big {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .section-card {
        background: #1e2130; border-radius: 12px;
        padding: 1.2rem; border: 1px solid #2d3450;
        margin-bottom: 1rem;
    }
    .tag {
        display: inline-block; background: #2d3450;
        color: #667eea; padding: 4px 12px;
        border-radius: 20px; margin: 3px;
        font-size: 0.85rem; font-weight: 600;
    }
    .tag-missing {
        display: inline-block; background: #3d1e2a;
        color: #ff6b8a; padding: 4px 12px;
        border-radius: 20px; margin: 3px;
        font-size: 0.85rem; font-weight: 600;
    }
    .tag-strong {
        display: inline-block; background: #1e3d2a;
        color: #4caf82; padding: 4px 12px;
        border-radius: 20px; margin: 3px;
        font-size: 0.85rem; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER
st.markdown('<div class="hero-title">🎯 AI Job Description Analyser</div>',
            unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload your resume & paste a job description — get instant AI-powered fit analysis</div>', unsafe_allow_html=True)

# ── GROQ CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── PDF EXTRACTOR


def extract_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# ── GROQ ANALYSER


def analyse_fit(resume_text, jd_text):
    prompt = f"""
You are an expert HR analyst and career coach. Analyse the fit between this resume and job description.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:2000]}

Respond in this EXACT format:

MATCH_SCORE: [number 0-100]

MATCHED_SKILLS:
- [skill 1]
- [skill 2]
- [skill 3]
- [skill 4]
- [skill 5]

MISSING_SKILLS:
- [missing skill 1]
- [missing skill 2]
- [missing skill 3]
- [missing skill 4]
- [missing skill 5]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

RECOMMENDATIONS:
- [recommendation 1]
- [recommendation 2]
- [recommendation 3]

VERDICT:
[2-3 sentence summary of overall fit and chances]
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content

# ── PARSER


def parse_section(text, section):
    try:
        start = text.index(section + ":") + len(section) + 1
        next_sections = ["MATCH_SCORE", "MATCHED_SKILLS", "MISSING_SKILLS",
                         "STRENGTHS", "RECOMMENDATIONS", "VERDICT"]
        end = len(text)
        for s in next_sections:
            if s != section and s + ":" in text[start:]:
                pos = text.index(s + ":", start)
                if pos < end:
                    end = pos
        return text[start:end].strip()
    except:
        return ""


def parse_score(text):
    try:
        line = [l for l in text.split("\n") if "MATCH_SCORE:" in l][0]
        return int(''.join(filter(str.isdigit, line)))
    except:
        return 0


def parse_bullets(text, section):
    content = parse_section(text, section)
    items = [l.strip().lstrip("-•").strip()
             for l in content.split("\n") if l.strip().startswith("-")]
    return items


# ── MAIN UI
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📄 Your Resume")
    uploaded = st.file_uploader("Upload PDF resume", type=["pdf"])
    resume_text = ""
    if uploaded:
        resume_text = extract_pdf_text(uploaded)
        st.success(
            f"✅ Resume loaded — {len(resume_text)} characters extracted")

with col2:
    st.markdown("### 💼 Job Description")
    jd_text = st.text_area("Paste the job description here", height=200,
                           placeholder="Paste the full job description...")

st.divider()

if st.button("🚀 Analyse My Fit", use_container_width=True):
    if not resume_text:
        st.error("Please upload your resume PDF!")
    elif not jd_text.strip():
        st.error("Please paste a job description!")
    else:
        with st.spinner("🤖 Groq AI is analysing your fit..."):
            result = analyse_fit(resume_text, jd_text)

        score = parse_score(result)
        matched = parse_bullets(result, "MATCHED_SKILLS")
        missing = parse_bullets(result, "MISSING_SKILLS")
        strengths = parse_bullets(result, "STRENGTHS")
        recommendations = parse_bullets(result, "RECOMMENDATIONS")
        verdict = parse_section(result, "VERDICT")

        # Score
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            color = "#4caf82" if score >= 70 else "#ffa726" if score >= 50 else "#ff6b8a"
            label = "🟢 Strong Match" if score >= 70 else "🟡 Moderate Match" if score >= 50 else "🔴 Weak Match"
            st.markdown(f"""
            <div class="metric-card">
                <div style="color:#888; font-size:1rem; margin-bottom:0.5rem">MATCH SCORE</div>
                <div class="score-big" style="color:{color};">{score}%</div>
                <div style="color:{color}; font-size:1.2rem; font-weight:700;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Skills columns
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### ✅ Matched Skills")
            st.markdown('<div class="section-card">' +
                        "".join([f'<span class="tag-strong">{s}</span>' for s in matched]) +
                        '</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown("#### ❌ Missing Skills")
            st.markdown('<div class="section-card">' +
                        "".join([f'<span class="tag-missing">{s}</span>' for s in missing]) +
                        '</div>', unsafe_allow_html=True)

        # Strengths & Recommendations
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### 💪 Your Strengths")
            for s in strengths:
                st.markdown(f"✦ {s}")

        with col_d:
            st.markdown("#### 🎯 Recommendations")
            for r in recommendations:
                st.markdown(f"→ {r}")

        # Verdict
        if verdict:
            st.markdown("---")
            st.markdown("#### 🧠 AI Verdict")
            st.info(verdict)

# ── FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:0.85rem;'>
    Built by <b>Raam Patil </b> · Powered by Groq (Llama 3) · LangChain · Streamlit
</div>
""", unsafe_allow_html=True)

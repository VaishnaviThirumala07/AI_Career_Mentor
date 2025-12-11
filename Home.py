# app.py
import streamlit as st
from pathlib import Path
import time
import io

# ------------------------------------------------------------
# 1. Page Config (must be first Streamlit command)
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Career Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# 2. Custom CSS
# ------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* App container spacing */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Hero */
        .hero {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }
        .hero .title {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            line-height: 1.1;
        }
        .hero .subtitle {
            color: #6b7280;
            margin-top: 0.25rem;
            margin-bottom: 0;
            font-size: 1rem;
        }

        /* Gradient title accent */
        .brand-accent {
            background: linear-gradient(90deg, #0066ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Card */
        .card {
            background-color: #0f1724;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.04);
            box-shadow: 0 6px 20px rgba(2,6,23,0.6);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 30px rgba(2,6,23,0.7);
            border-color: rgba(124,58,237,0.9);
        }
        .card h4 { margin: 0 0 6px 0; font-size: 1.1rem; }
        .card p { margin: 0; color: #9aa0a6; font-size: 0.95rem; }

        /* CTA center */
        .center-cta { text-align:center; margin-top: 1rem; }

        /* Hide built-in streamlit footer and menu for clean demo */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Make file uploader compact */
        .stFileUpload > label { font-weight: 600; }

        /* Responsive tweak */
        @media (max-width: 800px) {
            .hero { flex-direction: column; align-items: flex-start; gap: 0.3rem; }
            .hero .title { font-size: 1.6rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# ------------------------------------------------------------
# 3. Sidebar navigation + uploader (single source of truth)
# ------------------------------------------------------------
st.sidebar.title("AI Career Mentor")
nav = st.sidebar.radio(
    "Tools",
    options=["Home", "Resume Screener", "Mock Interviewer", "Skill Roadmap", "Resources", "Settings"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Actions")

# Use a single uploader in the sidebar (single source of truth)
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
    st.session_state["resume_name"] = ""
    st.session_state["resume_bytes"] = None

with st.sidebar.expander("Upload resume (PDF / DOCX / TXT)", expanded=True):
    uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"], key="sidebar_resume")
    if uploaded_resume:
        # Save bytes into session_state for use across pages
        try:
            # read file bytes
            file_bytes = uploaded_resume.read()
            st.session_state["resume_uploaded"] = True
            st.session_state["resume_name"] = uploaded_resume.name
            st.session_state["resume_bytes"] = file_bytes
            st.success(f"Resume uploaded: {uploaded_resume.name} ✔")
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")
            st.session_state["resume_uploaded"] = False
            st.session_state["resume_name"] = ""
            st.session_state["resume_bytes"] = None

st.sidebar.markdown("---")
st.sidebar.write("A prototype UI for an AI-driven career mentor. Connect your model to get live recommendations.")

# ------------------------------------------------------------
# 4. Shared helper utilities
# ------------------------------------------------------------
def render_card(title: str, description: str, bullets=None):
    bullets = bullets or []
    bullet_html = "".join([f"<li>{b}</li>" for b in bullets])
    html = f"""
    <div class="card">
        <h4>{title}</h4>
        <p>{description}</p>
        <ul style="margin-top:10px; padding-left:18px; color:#bdbdbf; font-size:0.92rem;">
            {bullet_html}
        </ul>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ------------------------------------------------------------
# 5. HOME: hero + feature overview + metrics
# ------------------------------------------------------------
if nav == "Home":
    hero_col1, hero_col2 = st.columns([3,1], gap="large")
    with hero_col1:
        st.markdown('<div class="hero">', unsafe_allow_html=True)
        st.markdown('<div><h1 class="title">AI Career Mentor <span class="brand-accent">Platform</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Personalized career roadmaps, resume optimization, and mock interviews powered by generative AI.</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### What you can do")
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            render_card("Resume Screener", "Upload a resume and job description to receive an ATS-friendly score and improvement checklist.", ["Match score", "Keyword gap", "Formatting suggestions"])
        with c2:
            render_card("Mock Interviewer", "Practice role-specific technical and behavioral interviews with real-time feedback.", ["Adaptive questions", "Score & explanations", "Replay answers"])
        with c3:
            render_card("Skill Roadmap", "Receive weekly study plans and project suggestions to reach your target role.", ["Milestones", "Free resources", "Capstone suggestions"])

        st.markdown("---")
        st.markdown("### Quick Metrics")
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg Resume Match", "72%", "+6% vs last week")
        m2.metric("Avg Mock Score", "78/100", "+3 points")
        m3.metric("Active Roadmaps", "142", "New: 18")

    with hero_col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Instant Demo", unsafe_allow_html=True)
        st.markdown("- Upload a resume in the sidebar and try the Resume Screener.", unsafe_allow_html=True)
        st.markdown("- Use the Mock Interviewer to simulate a 10-question session.", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 6. Resume Screener - uses sidebar uploader (no duplicate uploader)
# ------------------------------------------------------------
elif nav == "Resume Screener":
    st.header("Resume Screener")
    st.write("Upload or paste your resume and a target job description. This screen is scaffolded to integrate an ATS/LLM analysis function.")

    col_left, col_right = st.columns([2,1], gap="large")
    with col_left:
        # Use bytes from the sidebar uploader
        resume_uploaded = st.session_state.get("resume_uploaded", False)
        resume_name = st.session_state.get("resume_name", "")
        resume_bytes = st.session_state.get("resume_bytes", None)

        if resume_uploaded:
            st.success(f"Using uploaded resume: {resume_name}")
        else:
            st.info("You can upload a resume in the sidebar, or paste the text below.")

        # Allow pasting resume text if user prefers
        pasted_resume_text = st.text_area("Or paste resume text here (optional)", height=200, placeholder="Paste full resume text...")

        jd_text = st.text_area("Paste target Job Description (or link to JD)", height=180, placeholder="Paste the full JD or key requirements here...")
        run_button = st.button("Analyze Resume")

        if run_button:
            # Decide which resume source to analyze: sidebar upload > pasted text
            if not resume_uploaded and not pasted_resume_text.strip():
                st.error("Please upload a resume in the sidebar or paste resume text before running analysis.")
            else:
                # Simulated analysis flow - replace these with real model calls
                with st.spinner("Running ATS analysis and keyword extraction..."):
                    time.sleep(1.2)
                # Sample outputs (placeholders)
                match_score = 78  # placeholder; compute using your model
                keyword_gaps = ["Docker", "Kubernetes", "System Design"]
                format_issues = ["No section for 'Projects'", "Inconsistent date format"]

                st.success("Analysis complete")
                st.metric("Match Score", f"{match_score}%")
                st.markdown("**Top missing keywords**")
                st.write(", ".join(keyword_gaps))
                st.markdown("**Formatting & structural suggestions**")
                for it in format_issues:
                    st.write(f"- {it}")

                with st.expander("View Actionable Recommendations"):
                    st.write("1. Add a Projects section highlighting impact metrics.")
                    st.write("2. Use reverse chronological layout for experience.")
                    st.write("3. Add keywords from JD in skills and bullet points.")

    with col_right:
        st.markdown("### Tips for better matches")
        st.write("- Mirror the job title and key terms from the JD.")
        st.write("- Use metrics when describing accomplishments.")
        st.write("- Keep resume length appropriate for your level (1-2 pages).")

# ------------------------------------------------------------
# 7. Mock Interviewer - simple chat-like practice UI
# ------------------------------------------------------------
elif nav == "Mock Interviewer":
    st.header("Mock Interviewer")
    st.write("Select role and difficulty, then start a simulated interview. This UI is designed to connect to an LLM backend for question generation and evaluation.")

    role = st.selectbox("Select Role", ["Software Engineer - Backend", "Data Scientist", "Frontend Engineer", "Product Manager"])
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    num_questions = st.slider("Number of Questions", 3, 15, 8)

    if "mock_history" not in st.session_state:
        st.session_state.mock_history = []

    start = st.button("Start Interview")
    if start:
        st.session_state.mock_history = []
        # Simulate question generation
        for i in range(num_questions):
            q = f"Question {i+1} for {role} (difficulty: {difficulty}) - provide a focused answer describing approach and trade-offs."
            st.session_state.mock_history.append({"q": q, "a": ""})
        st.experimental_rerun()

    if st.session_state.get("mock_history"):
        with st.form("mock_form", clear_on_submit=False):
            for idx, qa in enumerate(st.session_state.mock_history):
                st.markdown(f"**Q{idx+1}.** {qa['q']}")
                response = st.text_area(f"Your answer for Q{idx+1}", value=qa.get("a", ""), key=f"ans_{idx}", height=120)
                st.session_state.mock_history[idx]["a"] = response
                st.markdown("---")
            submitted = st.form_submit_button("Submit Answers for Feedback")

        if submitted:
            with st.spinner("Scoring answers using the evaluation model..."):
                time.sleep(1.1)
            # Placeholder scoring
            sample_scores = [70 + (i % 5) for i in range(len(st.session_state.mock_history))]
            avg_score = sum(sample_scores) // len(sample_scores)
            st.success(f"Interview complete — Average Score: {avg_score}/100")
            st.write("Detailed feedback (mock):")
            for i, s in enumerate(sample_scores):
                st.write(f"- Q{i+1}: Score {s}/100 — Focus more on structure; include specific metrics where possible.")

# ------------------------------------------------------------
# 8. Skill Roadmap - dynamic plan generator
# ------------------------------------------------------------
elif nav == "Skill Roadmap":
    st.header("Skill Roadmap")
    st.write("Provide your current skills and target role. The system will generate a 12-week plan with milestones.")

    col1, col2 = st.columns(2)
    with col1:
        current_skills = st.multiselect("Current Skills (select)", ["Python", "SQL", "Data Structures", "Machine Learning", "React", "Docker"], default=["Python"])
        target_role = st.selectbox("Target Role", ["Data Scientist", "ML Engineer", "Backend Engineer", "Frontend Engineer"])
        create_plan = st.button("Generate Roadmap")

    with col2:
        st.markdown("### Snapshot")
        st.write(f"Target: **{target_role}**")
        st.write("Recommended weekly time commitment: **8-12 hours**")
        st.progress(0)

    if create_plan:
        # Simple mock roadmap generation
        weeks = 12
        roadmap = []
        for w in range(1, weeks + 1):
            if w <= 4:
                phase = "Core foundations"
            elif w <= 8:
                phase = "Applied learning"
            else:
                phase = "Capstone & interviews"
            roadmap.append((w, phase))

        st.success("Roadmap generated")
        for w, phase in roadmap:
            st.markdown(f"**Week {w} — {phase}**")
            st.write("- Objectives: ...")
            st.write("- Suggested tasks: ...")
            st.write("")

# ------------------------------------------------------------
# 9. Resources & Settings
# ------------------------------------------------------------
elif nav == "Resources":
    st.header("Resources")
    st.write("Curated links, templates, and sample projects to accelerate learning.")
    st.markdown("- Resume templates (ATS-friendly)")
    st.markdown("- Common interview questions by role")
    st.markdown("- Free learning resources and project ideas")
    with st.expander("Sample Resume Templates"):
        st.write("Template A — Reverse-chronological. Template B — Skills-first. (Add more here.)")

elif nav == "Settings":
    st.header("Settings")
    st.write("Configure integrations, privacy, and model preferences.")
    api_option = st.selectbox("Model integration", ["Local (not configured)", "OpenAI (not configured)", "Custom API"])
    st.checkbox("Enable session logging for analytics", value=False)
    st.markdown("**Note:** Connect your chosen model in backend to enable real analysis.")

# ------------------------------------------------------------
# 10. Footer / CTA
# ------------------------------------------------------------
st.markdown("---")
st.markdown('<div class="center-cta"><strong>Tip:</strong> Connect your model endpoint to replace placeholders with real AI-driven results.</div>', unsafe_allow_html=True)

import streamlit as st

# ------------------------------------------------------------
# 1. Page Config (Must be first)
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Career Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# 2. Custom CSS (The Modern Look)
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
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Hero Section */
        .hero {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .hero .title {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
        }
        .hero .subtitle {
            color: #94a3b8; /* Slate 400 */
            margin-top: 0.5rem;
            font-size: 1.1rem;
            font-weight: 300;
        }

        /* Gradient title accent */
        .brand-accent {
            background: linear-gradient(90deg, #3B82F6, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Card Styling */
        .card {
            background-color: #1e293b; /* Slate 800 */
            padding: 24px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out, border-color 0.2s;
            height: 100%;
        }
        .card:hover {
            transform: translateY(-5px);
            border-color: #6366f1; /* Indigo 500 */
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .card h4 {
            margin: 0 0 10px 0;
            font-size: 1.25rem;
            color: #f8fafc;
            font-weight: 600;
        }
        .card p {
            margin: 0;
            color: #cbd5e1; /* Slate 300 */
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        /* Bullet points in cards */
        .card ul {
            margin-top: 12px;
            padding-left: 20px;
            color: #94a3b8;
            font-size: 0.9rem;
        }

        /* Hide standard Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# ------------------------------------------------------------
# 3. Sidebar (Clean - No Uploader)
# ------------------------------------------------------------
st.sidebar.title("AI Career Mentor")
st.sidebar.markdown("---")
st.sidebar.info("👈 **Navigate** using the menu above to access the tools.")
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Google Gemini AI")


# ------------------------------------------------------------
# 4. Helper Function: Render HTML Card
# ------------------------------------------------------------
def render_card(title: str, description: str, bullets=None):
    bullets = bullets or []
    bullet_html = "".join([f"<li>{b}</li>" for b in bullets])
    html = f"""
    <div class="card">
        <h4>{title}</h4>
        <p>{description}</p>
        <ul>
            {bullet_html}
        </ul>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ------------------------------------------------------------
# 5. Main Dashboard Layout (Hero + Cards)
# ------------------------------------------------------------

# Hero Section
col1, col2 = st.columns([3, 1], gap="large")
with col1:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<div><h1 class="title">AI Career Mentor <span class="brand-accent">Platform</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Personalized career roadmaps, resume optimization, and mock interviews powered by Generative AI.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Metrics Section
    m1, m2, m3 = st.columns(3)
    m1.metric("System Status", "Online", "Gemini-1.5-Flash")
    m2.metric("Resume Parser", "Active", "PDF/Text Support")
    m3.metric("Interview Engine", "Ready", "Context Aware")

with col2:
    # "Status" Card
    st.markdown("""
    <div class="card" style="text-align: center; border-color: #3B82F6;">
        <h4 style="color: #60A5FA;">🚀 Ready</h4>
        <p style="margin-bottom: 10px;">Select a tool from the sidebar to begin.</p>
        <div style="font-size: 0.8rem; color: #64748b;">
            Version: <strong>MVP 1.0</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Feature Cards (The Grid)
st.subheader("Available Tools")
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    render_card(
        "📄 Resume Screener", 
        "Upload a resume and job description to receive an ATS-friendly score.", 
        ["Match score calculation", "Keyword gap analysis", "Formatting suggestions"]
    )

with c2:
    render_card(
        "🤖 Mock Interviewer", 
        "Practice role-specific technical and behavioral interviews.", 
        ["Adaptive difficulty", "Real-time AI feedback", "Behavioral & Technical modes"]
    )

with c3:
    render_card(
        "🗺️ Skill Roadmap", 
        "Receive weekly study plans to reach your target role.", 
        ["12-week timeline", "Free resource links", "Capstone project ideas"]
    )

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #475569; font-size: 0.8rem;">Powered by Gemini AI • Built with Streamlit</div>', unsafe_allow_html=True)
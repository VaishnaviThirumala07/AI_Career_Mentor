import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')

st.title("🗺️ AI Learning Roadmap")
st.write("Generate a personalized study plan to reach your career goals.")

# 2. Input Form
with st.form("roadmap_form"):
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.text_input("Current Role / Skills", placeholder="e.g. Student, know Python & SQL")
    with col2:
        target_role = st.text_input("Target Role", placeholder="e.g. AI Engineer, Data Scientist")
    
    timeline = st.slider("Timeline (Weeks)", min_value=1, max_value=12, value=4)
    submit_button = st.form_submit_button("Generate Roadmap")

# 3. Logic
if submit_button and current_role and target_role:
    with st.spinner("Drafting your path to success..."):
        # The Prompt
        prompt = f"""
        Act as a Senior Technical Career Coach. 
        Create a detailed {timeline}-week learning roadmap to go from "{current_role}" to "{target_role}".
        
        Strict Requirements:
        1. Break it down week by week.
        2. For each week, list 2-3 specific topics to master.
        3. PROVIDE FREE RESOURCES: Include actual names of YouTube channels, Coursera courses (audit mode), or Documentation links for each topic.
        4. Include a small "Capstone Project" idea at the end to practice skills.
        
        Format the output in clean Markdown. Use tables where possible.
        """
        
        try:
            response = model.generate_content(prompt)
            st.success("Roadmap Generated!")
            st.markdown(response.text)
            
            # Optional: Add a download button
            st.download_button(
                label="Download Roadmap",
                data=response.text,
                file_name="my_career_roadmap.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif submit_button:
    st.warning("Please fill in both your current skills and target role.")
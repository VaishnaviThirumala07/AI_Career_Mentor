import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Using 1.5 Pro for significantly better reasoning and rule-following
MODEL_NAME = 'gemini-2.5-pro' 

st.title("🤖 AI Mock Interviewer")

# 2. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Sidebar Settings
with st.sidebar:
    st.header("Interview Settings")
    role = st.selectbox("Target Role", ["Python Developer", "Data Scientist", "AI Engineer", "Product Manager"])
    topic = st.selectbox("Focus Topic", ["Technical Skills", "Behavioral (HR)", "System Design"])
    difficulty = st.select_slider("Difficulty", options=["Junior", "Mid-Level", "Senior"])
    
    if st.button("Start New Interview"):
        st.session_state.messages = []
        
        # System Prompt - Now passed as a permanent instruction
        system_instruction = f"""
        You are an expert Technical Interviewer for a {difficulty} {role} position. 
        Focus heavily on {topic}.
        
        Rules:
        1. Ask only ONE question at a time.
        2. Wait for the user's response.
        3. After the user answers, provide brief feedback (correct/incorrect) and then ask the NEXT question.
        4. Keep the tone professional but encouraging.
        
        Start by introducing yourself and asking the first question.
        """
        
        try:
            # Initialize model with SYSTEM INSTRUCTIONS
            model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)
            response = model.generate_content("Begin the interview by introducing yourself.")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            # Save the system instruction in session state for the chat loop
            st.session_state.system_instruction = system_instruction
        except Exception as e:
            st.error(f"Error starting interview: {e}")

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. User Input Handling
if user_answer := st.chat_input("Type your answer here..."):
    # A. Display User Message
    with st.chat_message("user"):
        st.write(user_answer)
    st.session_state.messages.append({"role": "user", "content": user_answer})

    # B. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing and preparing next question..."):
            try:
                # Re-initialize model with the same system instruction
                current_instruction = st.session_state.get("system_instruction", "You are a career interviewer.")
                model = genai.GenerativeModel(MODEL_NAME, system_instruction=current_instruction)
                
                # Format history for Gemini (exclude current user answer which is sent via send_message)
                chat_history = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages[:-1]
                ]
                
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(user_answer)
                
                st.write(response.text)
                
                # C. Save AI Response to memory
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error generating response: {e}")
import streamlit as st
import requests
import json
import os
from datetime import datetime
import time

# Configuration - USE ENVIRONMENT VARIABLE FOR DOCKER
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Page configuration
st.set_page_config(
    page_title="Azercell AI Chatbot",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_health():
    """Check if backend is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message(message):
    """Send message to backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": message, "user_id": "streamlit_user"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: Could not reach the backend service. Please check if the backend is running."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">📱 Azercell AI Chatbot</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        
        # Backend status
        if check_backend_health():
            st.success("🟢 Backend Online")
        else:
            st.error("🔴 Backend Offline")
        
        st.markdown("---")
        
        # About section
        st.subheader("About Azercell")
        st.write("""
        🏢 **Azercell Telecom LLC** is Azerbaijan's first and largest mobile network operator.
        
        📅 **Founded:** 1996  
        📍 **Headquarters:** Baku, Azerbaijan  
        👥 **Customers:** Millions served nationwide  
        🌐 **Services:** 4G/5G, Mobile Internet, Digital Solutions
        """)
        
        st.markdown("---")
        
        # Example queries
        st.subheader("💡 Try asking:")
        example_queries = [
            "What services does Azercell offer?",
            "Tell me about Azercell's network coverage",
            "How can I contact Azercell customer service?",
            "What are Azercell's mobile plans?",
            "Tell me about Azercell's history"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}", use_container_width=True):
                st.session_state.example_query = query

    # Main chat interface
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            welcome_msg = """
            👋 Welcome to Azercell AI Chatbot! 
            
            I'm here to help you with information about Azercell's services, plans, coverage, and more. 
            Feel free to ask me anything about Azerbaijan's leading mobile operator!
            """
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg, "timestamp": datetime.now()})

        # Display chat messages
        for message in st.session_state.messages:
            timestamp = message["timestamp"].strftime("%H:%M")
            
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑‍💻 You ({timestamp}):</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Azercell AI ({timestamp}):</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)

        # Handle example query from sidebar
        if "example_query" in st.session_state:
            user_input = st.session_state.example_query
            del st.session_state.example_query
            
            # Add user message
            st.session_state.messages.append({
                "role": "user", 
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Get bot response
            with st.spinner("🤔 Thinking..."):
                bot_response = send_message(user_input)
            
            # Add bot response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_response,
                "timestamp": datetime.now()
            })
            
            st.rerun()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Chat input - OUTSIDE the columns and main function
    st.markdown("---")
    
    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("💬 Ask me about Azercell services...", placeholder="Type your message here...")
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)

    # Handle form submission
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            bot_response = send_message(user_input)
        
        # Add bot response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": bot_response,
            "timestamp": datetime.now()
        })
        
        st.rerun()

if __name__ == "__main__":
    main()
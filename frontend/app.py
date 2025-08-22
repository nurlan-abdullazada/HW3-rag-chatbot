import os
from datetime import datetime

import requests
import streamlit as st

# Configuration - USE ENVIRONMENT VARIABLE FOR DOCKER
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Page configuration
st.set_page_config(
    page_title="Azercell AI Chatbot",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app styling */
    .main-header {
        text-align: center;
        color: #1e88e5;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1e88e5, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat message containers */
    .chat-message {
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease-in;
    }
    
    /* User message - Light Gray */
    .user-message {
        background: linear-gradient(135deg, #f5f5f5, #eeeeee);
        border-left: 5px solid #616161;
        margin-left: 2rem;
        color: #424242;
    }
    
    /* Bot message - Azercell Blue */
    .bot-message {
        background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
        border-left: 5px solid #0277bd;
        margin-right: 2rem;
        color: #01579b;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e88e5, #1565c0);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Status indicators */
    .status-online {
        background: linear-gradient(90deg, #4caf50, #66bb6a);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(76,175,80,0.3);
    }
    
    .status-offline {
        background: linear-gradient(90deg, #f44336, #ef5350);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(244,67,54,0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #1e88e5, #1976d2);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30,136,229,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30,136,229,0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1e88e5;
        box-shadow: 0 0 10px rgba(30,136,229,0.2);
    }
    
    /* Company info cards */
    .info-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    /* Animation for messages */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #1e88e5;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)


def check_backend_health():
    """Check if backend is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)  # Increased timeout
        return response.status_code == 200
    except requests.exceptions.RequestException:
        # Try alternative check
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    except Exception:
        return False


def send_message(message):
    """Send message to backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": message, "user_id": "streamlit_user"},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException:
        return "Connection error: Could not reach the backend service. Please check if the backend is running."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def main():
    # Header
    st.markdown(
        '<h1 class="main-header">📱 Azercell AI Chatbot</h1>', unsafe_allow_html=True
    )

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
        st.write(
            """
        🏢 **Azercell Telecom LLC** is Azerbaijan's first and largest mobile network operator.

        📅 **Founded:** 1996
        
        📍 **Headquarters:** Baku, Azerbaijan
        
        👥 **Customers:** Millions served nationwide
        
        🌐 **Services:** 4G/5G, Mobile Internet, Digital Solutions
        """
        )

        st.markdown("---")

        # Example queries
        st.subheader("💡 Try asking:")
        example_queries = [
            "What services does Azercell offer?",
            "Tell me about Azercell's network coverage",
            "How can I contact Azercell customer service?",
            "What are Azercell's mobile plans?",
            "Tell me about Azercell's history",
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
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": welcome_msg,
                    "timestamp": datetime.now(),
                }
            )

        # Display chat messages
        for message in st.session_state.messages:
            timestamp = message["timestamp"].strftime("%H:%M")
            
            if message["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>🧑‍💻 You ({timestamp}):</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Azercell AI ({timestamp}):</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)

        # Handle example query from sidebar
        if "example_query" in st.session_state:
            user_input = st.session_state.example_query
            del st.session_state.example_query

            # Add user message
            st.session_state.messages.append(
                {"role": "user", "content": user_input, "timestamp": datetime.now()}
            )

            # Get bot response
            with st.spinner("🤔 Thinking..."):
                bot_response = send_message(user_input)

            # Add bot response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": bot_response,
                    "timestamp": datetime.now(),
                }
            )

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
            user_input = st.text_input(
                "💬 Ask me about Azercell services...",
                placeholder="Type your message here...",
            )
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)

    # Handle form submission
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input, "timestamp": datetime.now()}
        )

        # Get bot response
        with st.spinner("🤔 Thinking..."):
            bot_response = send_message(user_input)

        # Add bot response
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_response, "timestamp": datetime.now()}
        )

        st.rerun()


if __name__ == "__main__":
    main()

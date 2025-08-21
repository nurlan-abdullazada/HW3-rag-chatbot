# RAG Chatbot - Azercell AI Assistant

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI backend and Streamlit frontend, deployed using Docker and AWS services.

## 🏗️ Architecture

- **Backend**: FastAPI with AWS Bedrock (Claude 3.7 Sonnet)
- **Frontend**: Streamlit web interface
- **Deployment**: Docker containers on AWS EC2
- **AI Model**: Anthropic Claude 3.7 Sonnet via AWS Bedrock

## 📁 Project Structure

rag-chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic data models
│   ├── config.py            # Configuration settings
│   ├── bedrock_service.py   # AWS Bedrock integration
│   └── Dockerfile           # Backend container config
├── frontend/
│   ├── app.py              # Streamlit application
│   └── Dockerfile          # Frontend container config
├── assets/
│   ├── backend/            # Backend screenshots
│   └── frontend/           # Frontend screenshots
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
└── README.md             # This file



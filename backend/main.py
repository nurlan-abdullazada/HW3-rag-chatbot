from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import json
from models import ChatMessage, ChatResponse, HealthResponse
from bedrock_service import BedrockService
from config import config

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Bedrock service
bedrock_service = BedrockService()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        is_healthy = bedrock_service.health_check()
        if is_healthy:
            return HealthResponse(status="healthy", message="All services are running")
        else:
            return HealthResponse(status="unhealthy", message="Bedrock service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint"""
    try:
        response = bedrock_service.generate_response(message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(message: ChatMessage):
    """Streaming chat endpoint"""
    try:
        def generate():
            response = bedrock_service.generate_response(message.message)
            # Simulate streaming by yielding chunks
            words = response.split()
            for i, word in enumerate(words):
                chunk = {
                    "response": word + " ",
                    "is_complete": i == len(words) - 1
                }
                yield f"data: {json.dumps(chunk)}\n\n"
        
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming chat failed: {str(e)}")

if __name__ == "__main__":
    print(f"Starting server on {config.BACKEND_HOST}:{config.BACKEND_PORT}")
    uvicorn.run(
        "main:app",  # Changed from 'app' to "main:app"
        host=config.BACKEND_HOST, 
        port=config.BACKEND_PORT,
        reload=False  # Changed from True to False for Docker
    )

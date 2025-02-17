from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
from app.services.ai_service import AIService
from app.models.database import SessionLocal
import json
from datetime import datetime

router = APIRouter()

db_session = SessionLocal()

user_contexts = {} 

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.ai_service = AIService(db_session)

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def chat_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    user_contexts[client_id] = {}  # Initialize context for the user
    
    try:
        # Send welcome message
        welcome_message = {
            "type": "system",
            "message": "Welcome! I'm here to help you schedule your vaccination appointment. What type of vaccine are you looking for?",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_message(json.dumps(welcome_message), client_id)
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            print("Received message:", data)  # Debug log

            message_data = json.loads(data)

            user_context = user_contexts.get(client_id, {})

            # Process message with AI service
            ai_response = await manager.ai_service.process_query(message_data["message"], user_context)
            
            print("Received ai_response:", ai_response, client_id)  # Debug log

            # Add timestamp to response
            ai_response["timestamp"] = datetime.now().isoformat()
            
            # Send response back to client
            await manager.send_message(json.dumps(ai_response), client_id)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        error_message = {
            "type": "error",
            "message": f"An error occurred: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_message(json.dumps(error_message), client_id)
        manager.disconnect(client_id) 
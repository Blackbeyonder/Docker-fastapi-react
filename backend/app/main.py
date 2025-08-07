import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from app.database import Base, engine
from typing import Dict, List
import os

# Import other routes as needed
import app.models

from app.routes.transportistas import router as transportistas_router  # Router de transportistas
from dotenv import load_dotenv
from app.config import get_settings
from app.services.websocket_manager import ws_manager

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()
# Cargar variables de entorno
load_dotenv()

# Accediendo a las variables cargadas
database_url = os.getenv('DATABASE_URL')  # Obtiene la URL de la base de datos
secret_key = os.getenv('SECRET_KEY')  # Obtiene la clave secreta
algorithm = os.getenv('ALGORITHM')  # Obtiene el algoritmo de JWT
access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))  # Obtiene el tiempo de expiración del token, con un valor por defecto de 30

# Create templates directory if it doesn't exist
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(templates_dir, exist_ok=True)

# Mount static files directory if needed
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)

# Initialize templates
templates = Jinja2Templates(directory=templates_dir)

active_connections: List[WebSocket] = []

# Crear la instancia de FastAPI
app = FastAPI(
    title="OMS-AMERISA API",
    description="Backend API for OMS-AMERISA System",
    version="1.0.0"
)



# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure CORS
origins = [
    "*",
    # Add other allowed origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"], 
)

# Incluir routers con prefijos y tags consistentes

app.include_router(transportistas_router, prefix="/api/v1", tags=["transportistas"])  # Evidencias


# Endpoint raíz modificado para servir un HTML
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para depuración (opcional, eliminar en producción)
@app.get("/routes")
def get_routes():
    return [{"path": route.path, "methods": route.methods} for route in app.routes]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await ws_manager.connect(websocket, room_id)
    try:
        while True:
            await websocket.receive_text()  # Mantiene la conexión abierta
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, room_id)



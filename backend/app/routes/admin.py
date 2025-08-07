from app.dependencies import require_role
from app.models import User
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError  # Importar IntegrityError
from typing import List
import time
from typing import Optional
from datetime import datetime
from app.database import get_db
from pydantic import BaseModel
import logging
import traceback
router = APIRouter()

@router.get("/admin")
async def admin_route(user: User = Depends(require_role("admin"))):
    return {"message": "Bienvenido, administrador"}


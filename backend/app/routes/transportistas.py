

from collections import defaultdict
from app.models.responseBase import ResponseBase
from fastapi import FastAPI, Query, Request, Depends, HTTPException, File, UploadFile, Path, Body
from fastapi import APIRouter
from sqlalchemy.orm import Session, joinedload,load_only
from typing import List
from app.database import get_db  

from datetime import date, datetime, time, timedelta
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os



from sqlalchemy import func, desc, text


from passlib.context import CryptContext
from math import radians, sin, cos, sqrt, atan2
import math
from app.services.websocket_manager import ws_manager

import requests

from operator import attrgetter
import pytz
import geopy
from geopy.distance import geodesic, great_circle
from app.models.test import Test
from app.schemas.Test import RequestTestBase, TestBase

mexico_tz = pytz.timezone('America/Merida')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def Horamexico(): return datetime.now() - timedelta(hours=6)


@router.post("/save_ubication/operador", 
            # response_model=ResponseBase[None]
            )
async def save_ubication(
    requestSaveUbication: RequestTestBase,
    db: Session = Depends(get_db),
    # verify_token: str = Depends(new_verify_token)
):

    try:
        nuevaUbicacion = Test(
            latitud=requestSaveUbication.latitud, 
            longitud= requestSaveUbication.longitud, 
            timestamp= requestSaveUbication.timestamp
        )

        db.add(nuevaUbicacion)
        db.commit()
        db.refresh(nuevaUbicacion)

        room_id = "salaMonitoreo"

        await ws_manager.send_message({
                "action": "create",
                "data": nuevaUbicacion.to_dict()
                }, room_id)
        
        print("guardar")


        return ResponseBase(status=200, msg="Ubicaciones guardada exitosamente")

    except Exception as e:
        db.rollback()
        print(e)
        return ResponseBase(status=500, msg=f"Error: {str(e)}", data=None)


@router.get("/ubicaciones/operador", 
            response_model=ResponseBase[List[TestBase]]
            )
async def get_ubicaciones(
    db: Session = Depends(get_db),
):

    try:
        ubicacion = db.query(Test).all()
        print("obtener")


        return ResponseBase(status=200, msg="Success", data=ubicacion)

    except Exception as e:
        db.rollback()
        print(e)
        return ResponseBase(status=500, msg=f"Error: {str(e)}", data=None)
    



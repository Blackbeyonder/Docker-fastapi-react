# app/__init__.py
from app.config import get_settings
from app.database import get_db

__all__ = ['get_settings', 'get_db']
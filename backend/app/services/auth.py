import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1  # Tiempo de expiración para el Access Token
REFRESH_TOKEN_EXPIRE_DAYS = 7    # Tiempo de expiración para el Refresh Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def new_create_access_token(data: dict, expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})  # Se agrega el campo de expiración al token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def new_create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})  # Se agrega el campo de expiración al token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def new_verify_token(token: str = Depends(oauth2_scheme)):

    try:
        # Decodifica el token usando la clave secreta y el algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Recupera el 'sub' (nombre de usuario o campo)
        if username is None:
            raise HTTPException(status_code=401, detail="Token no válido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token no válido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token ha expirado")

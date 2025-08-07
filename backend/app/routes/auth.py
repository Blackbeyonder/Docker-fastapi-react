from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt  # Importa PyJWT
from jwt.exceptions import PyJWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv
import logging
from app.config import get_settings
from typing import List, Optional, Dict
from fastapi import Body

# Cargar variables de entorno
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configuración para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def Horamexico(): return datetime.now() - timedelta(hours=6)

# Función para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Token recibido: {token}")  # Log del token
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        print(f"Payload decodificado: {payload}")  # Log del payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        print("Token expirado")  # Log de token expirado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError as e:
        print(f"Error decodificando el token: {e}")  # Log de error de decodificación
        raise credentials_exception
    except jwt.exceptions.InvalidAlgorithmError:
        payload = jwt.decode(token, options={"verify_signature": False})

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        print(f"Usuario no encontrado: {email}")  # Log de usuario no encontrado
        raise credentials_exception

    return user

# Modelo para la solicitud de login
class LoginRequest(BaseModel):
    email: str
    password: str

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No se ha configurado SECRET_KEY")

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=365)  # Aumenta el tiempo de vida del token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Función para crear logs
def create_log(db: Session, user: User, action: str, details: str = None):
    log_entry = Log(
        username=user.name if user else "System",
        action=action,
        timestamp=Horamexico(),
        details=details,
        user_id=user.id if user else None
    )
    db.add(log_entry)
    db.commit()
    return log_entry

# Endpoint de login
@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Intento de login recibido: email={request.email}, password={request.password}")

    user = db.query(User).filter(User.email == request.email).first()

    if not user or not pwd_context.verify(request.password, user.password):
        logger.warning(f"Intento de login fallido para el email: {request.email}")
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    logger.info(f"Inicio de sesión exitoso para el usuario: {user.email}, rol: {user.role}")

    return {
        "message": "Inicio de sesión exitoso",
        "id": user.id,  # <-- AGREGADO PARA FRONTEND WMS
        "role": user.role,
        "name": user.name,
        "access_token": create_access_token(data={"sub": user.email, "role": user.role}),
    }

# Modelo para el registro de usuarios
class UserRegister(BaseModel):
    email: str
    name: str
    password: str
    role: str = "Creado"

# Endpoint de registro
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado exitosamente"}

# Endpoint para obtener la información del usuario actual
@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    print(f"Usuario actual: {current_user.name}, {current_user.email}, {current_user.role}")
    return {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }

# Endpoint para actualizar el perfil
@router.put("/update-profile")
async def update_profile(updated_profile: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    changes = []
    if updated_profile.get("name") != user.name:
        changes.append(f"Nombre: {user.name} → {updated_profile.get('name')}")
    if updated_profile.get("email") != user.email:
        changes.append(f"Email: {user.email} → {updated_profile.get('email')}")

    user.name = updated_profile.get("name", user.name)
    user.email = updated_profile.get("email", user.email)

    db.commit()
    db.refresh(user)

    if changes:
        log_details = f"Perfil actualizado: {', '.join(changes)}"
        create_log(db, current_user, "update_profile", log_details)

    return {"message": "Perfil actualizado correctamente", "user": user}

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

# Endpoint para cambiar la contraseña
@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user or not pwd_context.verify(request.current_password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    user.password = pwd_context.hash(request.new_password)
    db.commit()

    log_details = f"Contraseña cambiada para el usuario: {user.email}"
    create_log(db, current_user, "change_password", log_details)

    return {"message": "Contraseña cambiada correctamente"}

# Modelo para listar usuarios
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str

# Endpoint para obtener todos los usuarios (solo admin)
@router.get("/users")
async def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )
    users = db.query(User).all()
    return users

class UpdateRoleRequest(BaseModel):
    new_role: str

# Endpoint para actualizar el rol de un usuario (solo admin)
@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    request: UpdateRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    previous_role = user.role
    new_role = request.new_role

    user.role = new_role
    db.commit()
    db.refresh(user)

    log_details = f"Rol actualizado para el usuario '{user.name}' (ID: {user.id}): {previous_role} → {new_role}"
    create_log(db, current_user, "update_user_role", log_details)

    return {"message": "Rol actualizado correctamente"}

# Endpoint para eliminar un usuario (solo admin)
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_name = user.name
    user_email = user.email
    user_role = user.role

    db.delete(user)
    db.commit()

    log_details = f"Usuario eliminado: {user_name} (Email: {user_email}, Rol: {user_role})"
    create_log(db, current_user, "delete_user", log_details)

    return {"message": "Usuario eliminado correctamente"}

# Endpoint para obtener permisos específicos del usuario actual
@router.get("/permissions", response_model=dict)
async def get_user_permissions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role == "admin":
            all_roles = db.query(Role).all()
            all_permissions = []
            for role in all_roles:
                all_permissions.extend(role.permissions or [])

            unique_permissions = list(set(all_permissions))
            return {"permissions": unique_permissions}

        role = db.query(Role).filter(Role.name == current_user.role).first()

        if role:
            return {"permissions": role.permissions or []}

        return {"permissions": []}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener permisos: {str(e)}"
        )

# Model for client assignment request
class ClientAssignmentRequest(BaseModel):
    clientIds: List[int]

# Endpoint to assign clients to a user with 'client' role
@router.post("/users/{user_id}/assign-clients")
async def assign_clients_to_user(
    user_id: int,
    request: ClientAssignmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user.role != "client":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden asignar clientes a usuarios con rol 'client'"
        )

    try:
        db.query(UserClient).filter(UserClient.user_id == user_id).delete()

        for client_id in request.clientIds:
            client = db.query(Cuenta).filter(Cuenta.id == client_id).first()
            if client:
                new_assignment = UserClient(
                    user_id=user_id,
                    client_id=client_id,
                    created_at=Horamexico()
                )
                db.add(new_assignment)

        db.commit()

        client_count = len(request.clientIds)
        log_details = f"Se asignaron {client_count} clientes al usuario '{user.name}' (ID: {user.id})"
        create_log(db, current_user, "assign_clients", log_details)

        return {"message": f"{client_count} clientes asignados correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar clientes: {str(e)}"
        )

# Endpoint to get clients assigned to a user
@router.get("/users/{user_id}/clients")
async def get_user_clients(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los clientes de otros usuarios"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        assigned_clients = (
            db.query(Cuenta)
            .join(UserClient, UserClient.client_id == Cuenta.id)
            .filter(UserClient.user_id == user_id)
            .all()
        )

        return assigned_clients

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los clientes asignados: {str(e)}"
        )

# Modelo para la respuesta de reseteo de contraseña
class PasswordResetResponse(BaseModel):
    userId: int
    newPassword: str
    message: str

# Endpoint para resetear la contraseña de un usuario (solo admin)
@router.post("/users/{user_id}/reset-password", response_model=PasswordResetResponse)
async def reset_user_password(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar que el usuario actual sea admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción"
        )
        
    # Buscar el usuario
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Generar una contraseña aleatoria
    import random
    import string
    
    # Generar una contraseña de 10 caracteres con letras, números y símbolos
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    new_password = ''.join(random.choice(chars) for _ in range(10))
    
    # Hashear la nueva contraseña y actualizarla en la base de datos
    user.password = pwd_context.hash(new_password)
    db.commit()
    
    # Registrar este evento por seguridad
    log_details = f"El administrador {current_user.name} (ID: {current_user.id}) ha reseteado la contraseña del usuario {user.name} (ID: {user.id})"
    create_log(db, current_user, "reset_password", log_details)
    
    return {
        "userId": user.id,
        "newPassword": new_password,
        "message": "Contraseña reseteada correctamente"
    }

# --- ENDPOINTS DE NOTIFICACIONES ---

@router.get("/users/{user_id}/notifications", response_model=Optional[Dict[str, bool]])
async def get_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver las notificaciones de este usuario"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user.notifications

@router.put("/users/{user_id}/notifications", response_model=Dict[str, bool])
async def update_user_notifications(
    user_id: int,
    notifications: Dict[str, bool] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar las notificaciones de este usuario"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.notifications = notifications
    db.commit()
    db.refresh(user)
    log_details = f"Notificaciones actualizadas para el usuario {user.name} (ID: {user.id})"
    create_log(db, current_user, "update_notifications", log_details)
    return user.notifications

@router.delete("/users/{user_id}/notifications")
async def delete_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para borrar las notificaciones de este usuario"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.notifications = None
    db.commit()
    log_details = f"Notificaciones eliminadas para el usuario {user.name} (ID: {user.id})"
    create_log(db, current_user, "delete_notifications", log_details)
    return {"message": "Preferencias de notificaciones eliminadas"}


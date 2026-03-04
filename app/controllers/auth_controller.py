from fastapi import HTTPException, status
from app.config.db_config import get_db_connection
from app.utils.auth_utils import verify_password, create_access_token
import psycopg2

class AuthController:
    def login(self, login_data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Buscar usuario por email
            cursor.execute("SELECT id, password, nombre FROM usuarios WHERE email = %s AND estado = TRUE", (login_data.email,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Correo o contraseña incorrectos",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id, hashed_password, user_name = user
            
            if not verify_password(login_data.password, hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Correo o contraseña incorrectos",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Crear token de acceso
            access_token = create_access_token(data={"sub": str(user_id)})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user_id,
                    "nombre": user_name,
                    "email": login_data.email
                }
            }
            
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
        finally:
            if conn:
                conn.close()

auth_controller = AuthController()

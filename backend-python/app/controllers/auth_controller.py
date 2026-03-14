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
            
            # Buscar usuario por correo con su rol
            cursor.execute("""
                SELECT u.id, u.password as contrasena, u.nombre, r.nombre_rol 
                FROM usuarios u
                LEFT JOIN roles r ON u.rol_id = r.id
                WHERE u.email = %s AND u.estado = TRUE
            """, (login_data.correo,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario o contraseña incorrectos",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id, db_password, user_name, role_name = user
            
            # Verificación de contraseña
            authenticated = False
            if login_data.contrasena == db_password:
                authenticated = True
            else:
                try:
                    # Intentar verificar si es un hash de bcrypt
                    if db_password.startswith('$2b$') or db_password.startswith('$2y$'):
                        if verify_password(login_data.contrasena, db_password):
                            authenticated = True
                except Exception:
                    pass
            
            if not authenticated:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario o contraseña incorrectos",
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
                    "correo": login_data.correo,
                    "rol": role_name or "estudiante" # Fallback if no role assigned
                }
            }
            
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
        finally:
            if conn:
                conn.close()

auth_controller = AuthController()

from fastapi import Header, HTTPException, Depends
from app.config.db_config import get_db_connection
import psycopg2

def get_current_user_id(user_id: int = Header(..., alias="X-User-ID")):
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID header missing")
    return user_id

class PermissionChecker:
    def __init__(self, modulo_id: int):
        self.modulo_id = modulo_id

    def __call__(self, user_id: int = Depends(get_current_user_id)):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Obtener el rol del usuario
            cursor.execute("SELECT rol_id FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")
            
            rol_id = result[0]

            # Verificar permiso en la tabla permisos_rol
            cursor.execute(
                "SELECT acceso FROM permisos_rol WHERE rol_id = %s AND modulo_id = %s", 
                (rol_id, self.modulo_id)
            )
            permiso = cursor.fetchone()

            if not permiso or not permiso[0]:
                 raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este módulo")

            return True

        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

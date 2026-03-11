from app.controllers.base_controller import BaseController
from app.models import User, UserCreate
from app.config.db_config import get_db_connection
from app.utils.auth_utils import get_password_hash

class UserController(BaseController):
    def create_user(self, user: UserCreate):
        
        query = """
            INSERT INTO usuarios (rol_id, tipo_documento_id, numero_documento, facultad_id, nombre, correo, contrasena, created_, updated_)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 
                    (NOW() AT TIME ZONE 'America/Bogota'), 
                    (NOW() AT TIME ZONE 'America/Bogota'))
            RETURNING id, created_, updated_
        """
        
        hashed_password = get_password_hash(user.contrasena)
        params = (user.rol_id, user.tipo_documento_id, user.numero_documento, user.facultad_id, user.nombre, user.correo, hashed_password)
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            conn.commit()
            
            return {
                "id": row[0],
                "rol_id": user.rol_id,
                "tipo_documento_id": user.tipo_documento_id,
                "numero_documento": user.numero_documento,
                "facultad_id": user.facultad_id,
                "nombre": user.nombre,
                "correo": user.correo,
                "created_": row[1],
                "updated_": row[2]
            }
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

user_controller = UserController("usuarios")

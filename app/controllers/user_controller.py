from app.controllers.base_controller import BaseController
from app.models.all_models import User
from app.config.db_config import get_db_connection

class UserController(BaseController):
    def create_user(self, user: User):
        
        query = """
            INSERT INTO usuarios (nombres, apellidos, correo, password, rol_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, 
                    (NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota'), 
                    (NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota'))
            RETURNING id, created_at, updated_at
        """
        
        params = (user.nombres, user.apellidos, user.correo, user.password, user.rol_id)
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            conn.commit()
            
            return {
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "correo": user.correo,
                "rol_id": user.rol_id,
                "id": row[0],
                "created_at": row[1],
                "updated_at": row[2]
            }
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

user_controller = UserController("usuarios")

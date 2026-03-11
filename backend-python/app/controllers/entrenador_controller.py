from app.controllers.base_controller import BaseController
from app.config.db_config import get_db_connection
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

class EntrenadorController(BaseController):
    def __init__(self):
        super().__init__("entrenadores")

    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT e.*, u.nombre as nombre_usuario
                FROM entrenadores e
                JOIN usuarios u ON e.usuario_id = u.id
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            colnames = [desc[0] for desc in cursor.description]
            
            payload = []
            for row in result:
                content = dict(zip(colnames, row))
                payload.append(content)
                
            return {"resultado": jsonable_encoder(payload)}
                
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

entrenador_controller = EntrenadorController()

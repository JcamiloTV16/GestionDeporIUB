from app.controllers.base_controller import BaseController
from app.config.db_config import get_db_connection
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

class DeporteController(BaseController):
    def __init__(self):
        super().__init__("deportes")

    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deportes WHERE estado = TRUE")
            result = cursor.fetchall()
            
            colnames = [desc[0] for desc in cursor.description]
            payload = []
            for row in result:
                payload.append(dict(zip(colnames, row)))
                
            return {"resultado": jsonable_encoder(payload)}
                
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

deporte_controller = DeporteController()

from app.controllers.base_controller import BaseController
from app.config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

class InscripcionController(BaseController):
    def get_estudiantes_por_horario(self, horario_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT DISTINCT u.id, u.nombre, u.email as correo, i.create_ as fecha_inscripcion, i.estado
                FROM inscripciones i
                JOIN usuarios u ON i.estudiante_id = u.id
                WHERE i.deporte_id = (SELECT deporte_id FROM horarios WHERE id = %s)
            """
            cursor.execute(query, (horario_id,))
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

inscripcion_controller = InscripcionController("inscripciones")

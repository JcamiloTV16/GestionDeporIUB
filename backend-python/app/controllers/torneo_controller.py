from app.controllers.base_controller import BaseController
from app.config.db_config import get_db_connection
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

class TorneoController(BaseController):
    def __init__(self):
        super().__init__("torneos")

    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.*, d.nombre as deporte_nombre, u.nombre as creador_nombre
                FROM torneos t
                LEFT JOIN deportes d ON t.deporte_id = d.id
                LEFT JOIN usuarios u ON t.creado_por = u.id
                WHERE t.estado = TRUE
                ORDER BY t.fecha_inicio ASC
            """)
            result = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            payload = [dict(zip(colnames, row)) for row in result]
            return {"resultado": jsonable_encoder(payload)}
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def delete(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE torneos SET estado = FALSE WHERE id = %s", (id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Torneo no encontrado")
            return {"resultado": "Torneo eliminado correctamente"}
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

torneo_controller = TorneoController()

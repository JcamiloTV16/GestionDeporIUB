from app.controllers.base_controller import BaseController
from app.config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

class InscripcionTorneoController(BaseController):
    def __init__(self):
        super().__init__("inscripciones_torneo")

    def inscribir_estudiante(self, torneo_id: int, estudiante_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verificar que el torneo existe y tiene inscripciones abiertas
            cursor.execute(
                "SELECT estado_torneo FROM torneos WHERE id = %s AND estado = TRUE",
                (torneo_id,)
            )
            torneo = cursor.fetchone()
            if not torneo:
                raise HTTPException(status_code=404, detail="Torneo no encontrado")
            if torneo[0] != "Inscripciones Abiertas":
                raise HTTPException(
                    status_code=400,
                    detail="Las inscripciones no están abiertas para este torneo"
                )

            # Verificar que no esté ya inscrito
            cursor.execute(
                "SELECT id FROM inscripciones_torneo WHERE torneo_id = %s AND estudiante_id = %s AND estado = TRUE",
                (torneo_id, estudiante_id)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="Ya estás inscrito en este torneo"
                )

            # Crear la inscripción
            cursor.execute(
                """INSERT INTO inscripciones_torneo (torneo_id, estudiante_id, estado_inscripcion)
                   VALUES (%s, %s, 'Pendiente') RETURNING *""",
                (torneo_id, estudiante_id)
            )
            result = cursor.fetchone()
            conn.commit()

            colnames = [desc[0] for desc in cursor.description]
            content = dict(zip(colnames, result))
            return {"resultado": jsonable_encoder(content)}

        except HTTPException:
            if conn:
                conn.rollback()
            raise
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def get_inscritos_por_torneo(self, torneo_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT it.id, it.torneo_id, it.estudiante_id, it.estado_inscripcion,
                       it.create_ as fecha_inscripcion,
                       u.nombre as estudiante_nombre, u.email as estudiante_correo
                FROM inscripciones_torneo it
                JOIN usuarios u ON it.estudiante_id = u.id
                WHERE it.torneo_id = %s AND it.estado = TRUE
                ORDER BY it.create_ ASC
            """, (torneo_id,))
            result = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            payload = [dict(zip(colnames, row)) for row in result]
            return {"resultado": jsonable_encoder(payload)}

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def get_torneos_por_estudiante(self, estudiante_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT it.id as inscripcion_id, it.estado_inscripcion,
                       it.create_ as fecha_inscripcion,
                       t.id as torneo_id, t.nombre, t.descripcion,
                       t.fecha_inicio, t.fecha_fin, t.lugar, t.estado_torneo,
                       d.nombre as deporte_nombre
                FROM inscripciones_torneo it
                JOIN torneos t ON it.torneo_id = t.id
                LEFT JOIN deportes d ON t.deporte_id = d.id
                WHERE it.estudiante_id = %s AND it.estado = TRUE AND t.estado = TRUE
                ORDER BY t.fecha_inicio ASC
            """, (estudiante_id,))
            result = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            payload = [dict(zip(colnames, row)) for row in result]
            return {"resultado": jsonable_encoder(payload)}

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def actualizar_estado_inscripcion(self, inscripcion_id: int, nuevo_estado: str):
        conn = None
        try:
            if nuevo_estado not in ["Pendiente", "Aprobada", "Rechazada"]:
                raise HTTPException(
                    status_code=400,
                    detail="Estado de inscripción inválido. Debe ser: Pendiente, Aprobada o Rechazada"
                )
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inscripciones_torneo SET estado_inscripcion = %s, update_ = NOW() WHERE id = %s AND estado = TRUE",
                (nuevo_estado, inscripcion_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Inscripción no encontrada")
            return {"resultado": f"Inscripción actualizada a {nuevo_estado}"}

        except HTTPException:
            if conn:
                conn.rollback()
            raise
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def cancelar_inscripcion(self, inscripcion_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inscripciones_torneo SET estado = FALSE, update_ = NOW() WHERE id = %s AND estado = TRUE",
                (inscripcion_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Inscripción no encontrada")
            return {"resultado": "Inscripción cancelada correctamente"}

        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

inscripcion_torneo_controller = InscripcionTorneoController()

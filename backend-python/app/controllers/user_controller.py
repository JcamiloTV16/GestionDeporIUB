from app.controllers.base_controller import BaseController
from app.models import User, UserCreate
from app.config.db_config import get_db_connection
from app.utils.auth_utils import get_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from app.models.base_models import get_colombia_time
import psycopg2

class UserController(BaseController):
    # SOBREESCRIBIR GET_ALL PARA FILTRAR ACTIVOS Y UNIR CON ROLES
    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.*, r.nombre_rol 
                FROM usuarios u
                LEFT JOIN roles r ON u.rol_id = r.id
                WHERE u.estado = TRUE
                ORDER BY u.id DESC
            """)
            result = cursor.fetchall()
            
            colnames = [desc[0] for desc in cursor.description]
            payload = []
            for row in result:
                content = dict(zip(colnames, row))
                payload.append(content)
                
            return {"resultado": jsonable_encoder(payload)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    # OBTENER USUARIOS INACTIVOS PARA AUDITORÍA
    def get_inactive(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.*, r.nombre_rol 
                FROM usuarios u
                LEFT JOIN roles r ON u.rol_id = r.id
                WHERE u.estado = FALSE
                ORDER BY u.id DESC
            """)
            result = cursor.fetchall()
            
            colnames = [desc[0] for desc in cursor.description]
            payload = []
            for row in result:
                content = dict(zip(colnames, row))
                payload.append(content)
                
            return {"resultado": jsonable_encoder(payload)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    # BORRADO LÓGICO (DESACTIVAR)
    def delete(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET estado = FALSE WHERE id = %s", (id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"resultado": "Usuario desactivado correctamente"}
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    def update(self, id: int, data: dict):
        if "password" in data and data["password"]:
            data["password"] = get_password_hash(data["password"])
        elif "password" in data:
            del data["password"]
            
        data["update_"] = get_colombia_time()
        return super().update(id, data)

    # REACTIVAR USUARIO
    def reactivate(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET estado = TRUE WHERE id = %s", (id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"resultado": "Usuario reactivado correctamente"}
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    def create_user(self, user: UserCreate):
        query = """
            INSERT INTO usuarios (rol_id, tipo_documento_id, numero_documento, facultad_id, nivel_educativo_id, programa_id, nombre, email, password, create_, update_)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    (NOW() AT TIME ZONE 'America/Bogota'), 
                    (NOW() AT TIME ZONE 'America/Bogota'))
            RETURNING id, create_, update_
        """
        
        hashed_password = get_password_hash(user.password)
        params = (
            user.rol_id, 
            user.tipo_documento_id, 
            user.numero_documento, 
            user.facultad_id, 
            user.nivel_educativo_id, 
            user.programa_id, 
            user.nombre, 
            user.email, 
            hashed_password
        )
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            new_user_id = row[0]
            
            # Si el rol es Entrenador (rol_id=3), crear registro en tabla entrenadores
            if user.rol_id == 3:
                cursor.execute("""
                    INSERT INTO entrenadores (usuario_id, deporte_id, biografia)
                    VALUES (%s, %s, %s)
                """, (new_user_id, 1, None))  # deporte_id=1 por defecto, se puede cambiar después
            
            conn.commit()
            
            return {
                "id": new_user_id,
                "rol_id": user.rol_id,
                "tipo_documento_id": user.tipo_documento_id,
                "numero_documento": user.numero_documento,
                "facultad_id": user.facultad_id,
                "nivel_educativo_id": user.nivel_educativo_id,
                "programa_id": user.programa_id,
                "nombre": user.nombre,
                "email": user.email,
                "create_": row[1],
                "update_": row[2]
            }
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

user_controller = UserController("usuarios")

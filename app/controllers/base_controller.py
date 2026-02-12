import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder

class BaseController:
    def __init__(self, table_name):
        self.table_name = table_name

    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            result = cursor.fetchall()
            
            # Get column names
            colnames = [desc[0] for desc in cursor.description]
            
            payload = []
            for row in result:
                content = dict(zip(colnames, row))
                payload.append(content)
                
            json_data = jsonable_encoder(payload)        
            return {"resultado": json_data}
                
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def get_by_id(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (id,))
            result = cursor.fetchone()
            
            if result:
                colnames = [desc[0] for desc in cursor.description]
                content = dict(zip(colnames, result))
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail=f"{self.table_name} not found")
                
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def create(self, data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            columns = list(data.keys())
            values = list(data.values())
            
            placeholders = ",".join(["%s"] * len(values))
            columns_str = ",".join(columns)
            
            query = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders}) RETURNING id"
            
            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]
            conn.commit()
            
            return {"resultado": f"{self.table_name} created", "id": new_id}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def update(self, id: int, data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            set_clauses = [f"{key} = %s" for key in data.keys()]
            values = list(data.values())
            values.append(id)
            
            query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = %s"
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"{self.table_name} with id {id} not found")
                
            return {"resultado": f"{self.table_name} updated"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    def delete(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"{self.table_name} with id {id} not found")
                
            return {"resultado": f"{self.table_name} deleted"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

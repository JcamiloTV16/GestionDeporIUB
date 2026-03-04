import os
import sys
from app.config.db_config import get_db_connection

def clean_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Tablas de transacciones/vínculos: las vaciamos completamente para evitar conflictos de FK
    # (podemos reconstruirlas luego si el usuario quiere, pero para "limpieza" es lo más seguro)
    transactions = [
        "auditoria_accesos",
        "inscripciones",
        "horarios",
        "entrenadores"
    ]
    
    # 2. Tablas maestras: aquí sí mantendremos los 2 primeros registros
    masters = [
        "permisos_rol",
        "usuarios",
        "deportes",
        "modulos",
        "roles"
    ]
    
    print("--- Iniciando Limpieza Agresiva de Base de Datos ---")
    
    try:
        # Paso 1: Vaciar transacciones
        for table in transactions:
            cur.execute(f"DELETE FROM {table}")
            print(f"{table}: Vaciada completamente ({cur.rowcount} registros eliminados).")
            
        # Paso 2: Trim de tablas maestras
        for table in masters:
            cur.execute(f"SELECT id FROM {table} ORDER BY id ASC LIMIT 2")
            ids_to_keep = [r[0] for r in cur.fetchall()]
            
            if not ids_to_keep:
                print(f"{table}: Ya está vacía.")
                continue
                
            query = f"DELETE FROM {table} WHERE id NOT IN %s"
            cur.execute(query, (tuple(ids_to_keep),))
            print(f"{table}: Manteniendo IDs {ids_to_keep}. Se borraron {cur.rowcount} registros.")
        
        conn.commit()
        print("\n¡Limpieza de base de Datos ejecutada satisfactoriamente!")
        
    except Exception as e:
        conn.rollback()
        print(f"\nERROR crítico durante la limpieza: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    # Asegurar que el directorio actual está en el path para las importaciones
    sys.path.append(os.getcwd())
    clean_db()

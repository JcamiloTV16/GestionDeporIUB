from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from app.config.db_config import get_db_connection
from app.config.auth_config import auth_config
import psycopg2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception

class PermissionChecker:
    def __init__(self, modulo_id: int):
        self.modulo_id = modulo_id

    def __call__(self, user_id: int = Depends(get_current_user_id)):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Obtener el rol del usuario
            cursor.execute("SELECT rol_id FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")
            
            rol_id = result[0]

            # Verificar permiso en la tabla permisos_rol
            cursor.execute(
                "SELECT estado FROM permisos_rol WHERE rol_id = %s AND modulo_id = %s", 
                (rol_id, self.modulo_id)
            )
            permiso = cursor.fetchone()


            if not permiso or not permiso[0]:
                 raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este módulo")

            return True

        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()


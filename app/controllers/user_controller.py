from app.controllers.base_controller import BaseController
from app.models.all_models import User

class UserController(BaseController):
    def create_user(self, user: User):
        
        query = """
            INSERT INTO usuarios (nombres, apellidos, correo, password, rol_id, created_at, updated_at)
            VALUES (:nombres, :apellidos, :correo, :password, :rol_id, 
                    (NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota'), 
                    (NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota'))
            RETURNING id, created_at, updated_at
        """
        
        
        params = user.dict(exclude={'id', 'created_at', 'updated_at'})
        
        try:
            
            result = self.db.execute(query, params)
            row = result.fetchone()
            self.db.commit()
            
            return {
                **params,
                "id": row[0],
                "created_at": row[1],
                "updated_at": row[2]
            }
        except Exception as e:
            self.db.rollback()
            raise e
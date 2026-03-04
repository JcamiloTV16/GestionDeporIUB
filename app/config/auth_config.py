import os
from dotenv import load_dotenv

load_dotenv()

class AuthConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-for-development")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

auth_config = AuthConfig()

import os
from dotenv import load_dotenv
from pathlib import Path

# Carga variables desde un archivo .env si existe
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Modo del entorno (dev, prod, etc.)
ENV = os.getenv("ENV", "dev")

# Clave secreta para la aplicación
SECRET_KEY = os.getenv("KEY_SECRET")
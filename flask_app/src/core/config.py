import os

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = 'auth_service'

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
DB_USER = os.getenv('DB_USER', 'auth_service')
DB_PASS = os.getenv('DB_PASS', 'auth_service')
DB_HOST = os.getenv('DB_HOST', 'postgres_db')

DB_NAME = os.getenv('DB_NAME', 'auth_service')
DB_TEST_NAME = os.getenv('DB_TEST_NAME', 'auth_service_test')
DB_PORT = os.getenv('DB_PORT', 5432)

TESTING = os.getenv('TESTING', True)

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = os.getenv('FLASK_PORT', 8000)

REDIS_HOST = os.getenv('REDIS_HOST', 'auth_redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

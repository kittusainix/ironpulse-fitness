import os

# Root of the entire project (one level up from backend/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Frontend paths
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_FOLDER = os.path.join(FRONTEND_DIR, "static")
TEMPLATE_FOLDER = os.path.join(FRONTEND_DIR, "templates")

# Upload folder — use /tmp on serverless (Vercel), local path otherwise
_local_uploads = os.path.join(STATIC_FOLDER, "uploads")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", _local_uploads)

SECRET_KEY = os.getenv("SECRET_KEY", "ironpulse_titan_super_secret_key_2026")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max

# Database Mode Toggle:
# Set USE_ORACLE = True to route calls through Oracle PL/SQL via python-oracledb.
# When False, runs natively on the built-in SQLite engine with identical PL/SQL business logic.
USE_ORACLE = os.getenv("USE_ORACLE", "False").lower() in ("true", "1", "yes")

ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "oracle")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/XEPDB1")

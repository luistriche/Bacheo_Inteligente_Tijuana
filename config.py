"""
Configuración central: carga secretos desde variables de entorno.
En local lee un archivo .env (ignorado por git); en Vercel usa las
variables configuradas en el dashboard. Nunca se queman llaves en el código.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_dotenv(path=None):
    path = path or os.path.join(BASE_DIR, ".env")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


_load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_SECRET = os.environ.get("TELEGRAM_SECRET", "")

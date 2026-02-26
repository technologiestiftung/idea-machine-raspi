import os

from dotenv import load_dotenv

load_dotenv()

# Secrets aus Umgebungsvariablen holen
API_KEY = os.getenv("OPENAI_API_KEY")
BROKER_IP = os.getenv("BROKER_IP")

# Projektspezifische Konstanten
PROJECT_TITLE = "KI-Würfel"
PROJECT_SUBTITLE = "kulturBdigital"
LOGO_PATH = "assets/logo.png"

if not API_KEY:
    raise ValueError("OPENAI_API_KEY is not in .env!")
if not BROKER_IP:
    raise ValueError("BROKER_IP is not in .env!")
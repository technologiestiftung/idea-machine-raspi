import os

from dotenv import load_dotenv

load_dotenv()

# Secrets aus Umgebungsvariablen holen
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_AGENT_ID = os.getenv("MISTRAL_AGENT_ID")
BROKER_IP = os.getenv("BROKER_IP")

# Projektspezifische Konstanten
PROJECT_TITLE = "KI-Würfel"
PROJECT_SUBTITLE = "ZUKUNFTSWERK WIESBADEN"
LOGO_PATH = "assets/logo.png"


if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is not in .env!")
if not MISTRAL_AGENT_ID:
    raise ValueError("MISTRAL_AGENT_ID is not in .env!")
if not BROKER_IP:
    raise ValueError("BROKER_IP is not in .env!")
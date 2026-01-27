
import os
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# Secrets aus Umgebungsvariablen holen
api_key = os.getenv("OPENAI_API_KEY")
broker_ip = os.getenv("BROKER_IP")

# Validierung (optional aber empfohlen)
if not api_key:
    raise ValueError("OPENAI_API_KEY is not in .env!")
if not broker_ip:
    raise ValueError("BROKER_IP is not in .env!")
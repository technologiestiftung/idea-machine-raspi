"""
Hilfsfunktionen für Text-Verarbeitung und Drucker-Formatierung
"""
import os
import time

import RPi.GPIO as GPIO
from PIL import Image, ImageOps


def generate_ai_prompt(dice_text):
    """Erstellt den Prompt für die AI"""

    system_message = {
      "role": "system",
      "content": """
        Antworte NUR auf Deutsch.
        Persönlich, optimistisch, zukunftsorientiert und inspirierend.
        Zukunftsperspektive: Jahr 2050, schreibe an dich selbst 2026.
        Der Text MUSS Maximal 500 Zeichen lang sein.
        Der Text MUSS mit exakt folgendem Satz beginnen:
        In der Zukunft von Wiesbaden schreibe ich dir aus dem Jahr 2050.
      """
      }

    user_message = {
    "role": "user",
    "content": f"""
      Erzeuge EINE inspirierende, konkrete Idee für ein lebenswertes Wiesbaden.
      Die Idee MUSS aus der inhaltlichen Kombination aus den drei Bereichen mit den Begriffen: {dice_text}, entstehen.
      Die Begriffe müssen funktional miteinander verknüpft sein.
      Die Idee muss nicht realistisch sein und der Text soll einfach zu lesen sein.
      Bitte gib der Ideen einen Namen
    """
    }
    
    return [system_message, user_message]

def process_image_for_print(image_path, output_path="temp_logo.png", target_width=384, max_height=256):
    """
    Lädt ein Bild, skaliert es und konvertiert es zu 1-Bit Schwarz-Weiß.
    Optimiert für Thermaldrucker.
    Gibt den Pfad zum verarbeiteten Bild zurück oder None bei Fehler.
    """
    # Cache check: existiert bereits?
    if os.path.exists(output_path):
        return output_path
    
    try:
        # Bild laden
        img = Image.open(image_path)
        
        # Zu RGB konvertieren (falls es RGBA oder andere Modi hat)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Weißen Hintergrund für Transparenz
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Aspekt-Ratio berechnen
        width_percent = (target_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        
        # Höhenbegrenzung für Thermaldrucker (max. 256 Pixel)
        if height_size > max_height:
            height_percent = (max_height / float(img.size[1]))
            target_width = int((float(img.size[0]) * float(height_percent)))
            height_size = max_height
        
        # Skalieren mit hochwertigem Filter
        img = img.resize((target_width, height_size), Image.Resampling.LANCZOS)
        
        # Kontrast erhöhen für bessere Ergebnisse
        img = ImageOps.autocontrast(img, cutoff=2)
        
        # Zu Schwarz-Weiß (1-Bit) konvertieren mit Dithering
        # FLOYDSTEINBERG Dithering für bessere Qualität
        img = img.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
        
        # Speichern
        img.save(output_path)
        return output_path
        
    except Exception as e:
        print(f"Fehler bei Bildverarbeitung: {e}")
        return None


def blink(led_pin, event):
    while event.is_set():
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.3)    
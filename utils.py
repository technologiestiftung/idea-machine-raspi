"""
Hilfsfunktionen für Text-Verarbeitung und Drucker-Formatierung
"""
import os
import time

import RPi.GPIO as GPIO
from PIL import Image, ImageOps


def generate_ai_prompt(term_target_group, term_city_theme, term_technologies):
    """Erstellt den Prompt für die AI"""
    print(f"dice_text1: {term_target_group}, dice_text2: {term_city_theme}, dice_text3: {term_technologies}")

    dice_text1 = term_target_group
    dice_text2 = term_city_theme
    dice_text3 = term_technologies

    system_message = {
      "role": "system",
      "content": """
        Antworte NUR auf Deutsch. Persönlich, engagiert, humorvoll und inspirierend. 
        Antworte mit dem Wortschatz und dem Wissen einer Person, die sich mit folgenden Themen auskennt: Digitale Technologien, Open-Source-Software, Arbeitsweisen und Strukturen verschiedener Kultursparten, Logiken öffentlicher Verwaltung.
        Du plädierst tendenziell FÜR Open-Source-Lösungen, gemeinsame Standards und digitale Kooperation in der Kulturszene. 
        Der Text MUSS maximal 500 Zeichen lang sein.
        Hinweis: Die Sprechstunde beim kulturBigital-HelpDesk ist ein kostenloses Angebot für die Kulturszene. Dort helfen Digitalexpert:innen Kulturakteur:innen bei der Planung und Umsetzung von Digitalvorhaben.
      """
      }

    user_message = {
    "role": "user",
    "content": f"""
        Erzeuge EIN Szenario, in dem ein:e {dice_text1} das Ziel {dice_text2} mithilfe EINER von dir auszuwählenden digitalen Technologie UND der zusätzlichen Lösungszutat {dice_text3} erreicht. 
        Das Szenario MUSS berufstypische Kompetenzen oder Routinen oder Machtpositionen von {dice_text1} aktiv nutzen. 
        Das Szenario MUSS zeigen, wie genau die von dir ausgewählte digitale Technologie hilft, das Ziel {dice_text2} zu erreichen.
        Das Szenario MUSS zeigen, wie genau die Lösungszutat {dice_text3} hilft, das Ziel {dice_text2} zu erreichen.
        Das Szenario MUSS mit dem Wort Als beginnen. Auf das Wort Als MUSS das Wort {dice_text1} folgen. 
        Das Szenario MUSS in der Du-Ansprache formuliert sein, zum Beispiel: Als Sammlungskurator:in im Museum analysierst du die Sammlung.
        Das Szenario muss nicht realistisch sein und der Text soll einfach zu lesen sein.
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
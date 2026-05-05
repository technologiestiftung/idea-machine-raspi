"""
Hilfsfunktionen für Text-Verarbeitung und Drucker-Formatierung
"""
import os
import time

import RPi.GPIO as GPIO
from PIL import Image, ImageOps


def process_image_for_print(image_path, output_path="temp_logo.png", target_width=384, max_height=256):
    """
    Lädt ein Bild, skaliert es und konvertiert es zu 1-Bit Schwarz-Weiß.
    Optimiert für Thermaldrucker.
    Gibt den Pfad zum verarbeiteten Bild zurück oder None bei Fehler.
    """
    if os.path.exists(output_path):
        return output_path
    
    try:
        img = Image.open(image_path)
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        width_percent = (target_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        
        if height_size > max_height:
            height_percent = (max_height / float(img.size[1]))
            target_width = int((float(img.size[0]) * float(height_percent)))
            height_size = max_height
        
        img = img.resize((target_width, height_size), Image.Resampling.LANCZOS)
        
        img = ImageOps.autocontrast(img, cutoff=2)
        img = img.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
        
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
import RPi.GPIO as GPIO
import time
from openai import OpenAI
import os


from state import button_pressed, state, get_dice_begriff
from config import broker_ip, api_key
from constants import SENSOR_PIN, PRINTER_NAME, PRINTER_WIDTH
from utils import remove_umlauts, format_for_printer, generate_ai_prompt
from mqtt_handler import setup_mqtt


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# OpenAI Client
openai_client = OpenAI(api_key=api_key)

# MQTT Setup
mqtt_client = setup_mqtt(broker_ip)


# ============ MAIN LOOP ============

try:
    while True:
        # Button prüfen
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:
            button_pressed()
            print("Button gedrückt")
           
        button_active = state["button"]["pressed"]

        if button_active:
            print("Button Status: AKTIV - Generiere Idee...")

            # Würfelbegriffe holen
            gelb_begriff = get_dice_begriff("gelb")
            blau_begriff = get_dice_begriff("blau")
            pink_begriff = get_dice_begriff("pink")

            fehlende = []

            if gelb_begriff == "N/A":
                fehlende.append("Gelb")
            if blau_begriff == "N/A":
                fehlende.append("Blau")
            if pink_begriff == "N/A":
                fehlende.append("Pink")

            if fehlende:
                print(f"Nicht gewürfelt: {', '.join(fehlende)}")
                state["button"]["pressed"] = False
            else:
                # AI-Text generieren
                dice_text = f"{gelb_begriff}\n{blau_begriff}\n{pink_begriff}"
                messages = generate_ai_prompt(dice_text)
                
                completion = openai_client.chat.completions.create(
                    model="gpt-5-nano",
                    messages=messages
                )

                ai_text = completion.choices[0].message.content
                print(f"Original: {ai_text}")
                
                # Formatieren und drucken
                ai_text_clean = remove_umlauts(ai_text)
                formatted_text = format_for_printer(
                    ai_text_clean, 
                    gelb_begriff, 
                    blau_begriff, 
                    pink_begriff,
                    width=PRINTER_WIDTH
                )
     
                print(f"Formatiert:\n{formatted_text}")
                os.system(f'echo "{formatted_text}" | lp -d {PRINTER_NAME}')
                print("✓ Gedruckt!")

                # Button zurücksetzen - hier kannst du die LED steuern
                state["button"]["pressed"] = False
                # TODO: LED anschalten
                print("Button Status auf INAKTIV gesetzt")

        else:
            print("Button Status: INAKTIV")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet")
    print("Finaler State:")
    print(f"  Button: {state['button']}")
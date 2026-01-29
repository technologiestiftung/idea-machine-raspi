import RPi.GPIO as GPIO
import time
from openai import OpenAI
import os
import threading


from state import button_pressed, state, get_dice_begriff
from config import broker_ip, api_key
from constants import BUTTON_PIN, PRINTER_NAME, PRINTER_WIDTH, YELLOW_DICE_LED, PINK_DICE_LED, BLUE_DICE_LED, BUTTON_GREEN_LED
from utils import remove_umlauts, format_for_printer, generate_ai_prompt, blink
from mqtt_handler import setup_mqtt

#Thread-Setup for blinking LED
blink_event = threading.Event()
# Thread-Setup for blinking LEDs

blink_thread = None


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

GPIO.setup(YELLOW_DICE_LED, GPIO.OUT)
GPIO.output(YELLOW_DICE_LED, GPIO.LOW)
GPIO.setup(PINK_DICE_LED, GPIO.OUT)
GPIO.output(PINK_DICE_LED, GPIO.LOW)
GPIO.setup(BLUE_DICE_LED, GPIO.OUT)
GPIO.output(BLUE_DICE_LED, GPIO.LOW)
GPIO.setup(BUTTON_GREEN_LED, GPIO.OUT)
GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)  

# OpenAI Client
openai_client = OpenAI(api_key=api_key)

# MQTT Setup
mqtt_client = setup_mqtt(broker_ip)

# ============ MAIN LOOP ============

try:
    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
    

    while True:
        # Button prüfen
        button_active = False
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if not state["button"]["pressed"]:
                button_pressed()
                print("Button gedrückt – halte 2 Sekunden...")
                
        
        if state["button"]["pressed"]:
        # Button wurde losgelassen → abbrechen
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                state["button"]["pressed"] = False
                print("Button losgelassen – Abbruch")
            else:
                held_time = time.time() - state["button"]["last_press"]
                if held_time >= 0.5:
                    button_active = True


        if button_active:
            state["button"]["pressed"] = False
            button_active = False   
            print("Button Status: AKTIV - Generiere Idee...")

            # Würfelbegriffe holen
            gelb_begriff = get_dice_begriff("gelb")
            blau_begriff = get_dice_begriff("blau")
            pink_begriff = get_dice_begriff("pink")

            blink_event = threading.Event()
            blink_event.set()
            blink_thread = threading.Thread(target=blink, args=(BUTTON_GREEN_LED, blink_event))
            blink_thread.start()

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
            blink_event.clear()
            if blink_thread is not None:
                blink_thread.join(timeout=1)
            print("Button Status auf INAKTIV gesetzt")
            GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)


        else:
            print("Button Status: INAKTIV")
            blink_event.clear()
            if blink_thread is not None:
                blink_thread.join(timeout=1)
            GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
        
        
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet")
    print("Finaler State:")
    print(f"  Button: {state['button']}")
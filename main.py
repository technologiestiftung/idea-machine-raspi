import threading
import time

import RPi.GPIO as GPIO

from config import BROKER_IP
from constants import (BLUE_DICE_LED, BUTTON_GREEN_LED, BUTTON_PIN,
                       PINK_DICE_LED, YELLOW_DICE_LED)
from mqtt_handler import setup_mqtt
from print_handler import handle_print
from state import button_pressed, get_dice_begriff, state
from utils import blink

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


# MQTT Setup
mqtt_client = setup_mqtt(BROKER_IP)

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

            term_city_theme = get_dice_begriff("gelb")
            term_target_group = get_dice_begriff("blau")
            term_technologies = get_dice_begriff("pink")

            blink_event = threading.Event()
            blink_event.set()
            blink_thread = threading.Thread(target=blink, args=(BUTTON_GREEN_LED, blink_event))
            blink_thread.start()

            result = handle_print(term_city_theme, term_target_group, term_technologies)

            blink_event.clear()
            if blink_thread is not None:
                blink_thread.join(timeout=1)

            if result == "success":
                print("Druck erfolgreich")
                GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
            elif result == "api_error":
                print("API-Fehler - dreifaches Blinken")
                # Dreifaches langsames Blinken für API-Fehler
                for _ in range(12):
                    GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)
                    time.sleep(0.125)
                    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
                    time.sleep(0.125)
                GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
            else:  # printer_error
                print("Druckfehler - schnelles Blinken")
                # Schnelles Blinken für Druckfehler
                for _ in range(12):
                    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
                    time.sleep(0.125)
                    GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)
                    time.sleep(0.125)
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
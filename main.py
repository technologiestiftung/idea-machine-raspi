import signal
import sys
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

def handle_exit(signum, frame):
    print("Signal empfangen, räume GPIO auf...")
    blink_event.clear()
    if blink_thread is not None:
        blink_thread.join(timeout=1)
    GPIO.cleanup()
    sys.exit(0)

blink_event = threading.Event()
blink_thread = None

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(YELLOW_DICE_LED, GPIO.OUT)
GPIO.output(YELLOW_DICE_LED, GPIO.LOW)
GPIO.setup(PINK_DICE_LED, GPIO.OUT)
GPIO.output(PINK_DICE_LED, GPIO.LOW)
GPIO.setup(BLUE_DICE_LED, GPIO.OUT)
GPIO.output(BLUE_DICE_LED, GPIO.LOW)
GPIO.setup(BUTTON_GREEN_LED, GPIO.OUT)
GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)  


# ============ MAIN LOOP ============

try:
    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
    # MQTT Setup
    mqtt_client = setup_mqtt(BROKER_IP)

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

            dice_character = get_dice_begriff("gelb")
            dice_goal = get_dice_begriff("blau")
            dice_solution = get_dice_begriff("pink")

            blink_event.set()
            blink_thread = threading.Thread(target=blink, args=(BUTTON_GREEN_LED, blink_event))
            blink_thread.start()

            result = handle_print(dice_character, dice_goal, dice_solution)

            blink_event.clear()
            if blink_thread is not None:
                blink_thread.join(timeout=1)

            if result == "success":
                print("Druck erfolgreich")
                GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
            elif result == "api_error":

                for _ in range(12):
                    GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)
                    time.sleep(0.125)
                    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
                    time.sleep(0.125)
                GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
            else:  # printer_error
                print("Druckfehler - schnelles Blinken")
                for _ in range(12):
                    GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
                    time.sleep(0.125)
                    GPIO.output(BUTTON_GREEN_LED, GPIO.LOW)
                    time.sleep(0.125)
                GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
        else:
            #print("Button Status: INAKTIV")
            blink_event.clear()
            if blink_thread is not None:
                blink_thread.join(timeout=1)
            GPIO.output(BUTTON_GREEN_LED, GPIO.HIGH)
        
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    print("Clean up GPIO")
    GPIO.cleanup()

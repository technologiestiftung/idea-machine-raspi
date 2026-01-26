import RPi.GPIO as GPIO
import time
from state import button_pressed, update_button_timeout, state, dice_update, get_dice_begriff
from config import broker_ip
import paho.mqtt.client as mqtt
import threading
from openai import OpenAI
from config import api_key
import os
from datetime import datetime


SENSOR_PIN = 17
TIMEOUT = 5  # Sekunden
broker = broker_ip
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

openai_client = OpenAI(api_key=api_key)  # ← Umbenannt!


def remove_umlauts(text):
    """Ersetzt deutsche Umlaute für ASCII-Drucker"""
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ß': 'ss', '"': '"', '"': '"',
        '„': '"', '–': '-', '—': '-'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_for_printer(text, gelb_begriff, blau_begriff, pink_begriff, width=26):
     # Würfelbegriffe einfügen
    gelb_begriff = get_dice_begriff("gelb")
    blau_begriff = get_dice_begriff("blau")
    pink_begriff = get_dice_begriff("pink")


    """Formatiert Text für 58mm Thermodrucker (32 Zeichen breit)"""
    lines = []
    
    # Header
    lines.append("=" * width)
    lines.append("IDEENWUERFEL".center(width))
    lines.append("ZUKUNFTSWERK WIESBADEN".center(width))
    lines.append("=" * width)
    lines.append("Verwendete Begriffe:".center(width))  # optional zentriert
    lines.append(gelb_begriff.center(width))
    lines.append(blau_begriff.center(width))
    lines.append(pink_begriff.center(width))   
    lines.append("=" * width)
    lines.append("")  # Leerzeile als Trennung zum Text
    # Text umbrechen (Wörter nicht abschneiden)
    words = text.split()
    current_line = ""
    
    for word in words:
        # Prüfe ob Wort in aktuelle Zeile passt
        if len(current_line) + len(word) + 1 <= width:
            current_line += word + " "
        else:
            # Zeile ist voll, zur Liste hinzufügen
            lines.append(current_line.strip())
            current_line = word + " "
    
    # Letzte Zeile hinzufügen
    if current_line:
        lines.append(current_line.strip())
    
    lines.append("")
    lines.append("-" * width)
    
    # Timestamp
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    lines.append(timestamp.center(width))
    lines.append("-" * width)
    
    # Leerzeilen zum Abreißen
    lines.append("")
    lines.append("")
    lines.append("")
    
    return "\n".join(lines) + "\n\n\n"

# ============ MQTT CALLBACKS ============

def on_connect(client, userdata, flags, rc):
    print("MQTT verbunden")
    client.subscribe("dice/gelb")
    client.subscribe("dice/blau")
    client.subscribe("dice/pink")
    client.subscribe("dice/gelb/status")
    client.subscribe("dice/blau/status")
    client.subscribe("dice/pink/status")

def on_disconnect(client, userdata, rc):
    print("MQTT Verbindung verloren")

def on_message(client, userdata, message):
    payload = message.payload.decode().strip()
    
    if message.topic == "dice/gelb":
        dice_update("gelb", value=payload)
        print(f"Gelber Würfel: {payload} -> {get_dice_begriff('gelb')}")
    elif message.topic == "dice/blau":
        dice_update("blau", value=payload)
        print(f"Blauer Würfel: {payload} -> {get_dice_begriff('blau')}")
    elif message.topic == "dice/pink":
        dice_update("pink", value=payload)
        print(f"Pinker Würfel: {payload} -> {get_dice_begriff('pink')}")
    elif message.topic == "dice/gelb/status":
        dice_update("gelb", status=payload)
        print(f"Status Gelber Würfel: {payload}")
    elif message.topic == "dice/blau/status":
        dice_update("blau", status=payload)
        print(f"Status Blauer Würfel: {payload}")
    elif message.topic == "dice/pink/status":
        dice_update("pink", status=payload)
        print(f"Status Pinker Würfel: {payload}")
    else:
        print(f"Unbekanntes Thema: {message.topic}")

 
# ============ MQTT SETUP ============

mqtt_client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)  # ← Umbenannt!
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
mqtt_client.reconnect_delay_set(min_delay=1, max_delay=30)

mqtt_client.connect(broker, 1883, 60)

def mqtt_loop():
    mqtt_client.loop_forever()

threading.Thread(target=mqtt_loop, daemon=True).start()

def background_tasks():
    """Läuft im Hintergrund und prüft Timeouts"""
    while True:
        update_button_timeout()
        time.sleep(1)

threading.Thread(target=background_tasks, daemon=True).start()

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:
            button_pressed()
            print("Button gedrückt - Timer zurückgesetzt")
           
        button_active = state["button"]["pressed"]

        if button_active:
            last_press = state["button"]["last_press"]  # ← Korrigiert!
            remaining = int(TIMEOUT - (time.time() - last_press))
            print(f"Button Status: AKTIV (noch {remaining} Sekunden)")

            gelb_begriff = get_dice_begriff("gelb")
            blau_begriff = get_dice_begriff("blau")
            pink_begriff = get_dice_begriff("pink")

            if "N/A" in (gelb_begriff, blau_begriff, pink_begriff):
                print("Einer der Würfel wurde nicht gewürfelt.")
            else:
                dice_text = (
                    f"{gelb_begriff}\n"
                    f"{blau_begriff}\n"
                    f"{pink_begriff}"    
                )
                
                completion = openai_client.chat.completions.create(  # ← Korrigiert!
                    model="gpt-5-nano",
                    messages=[
                         {
                            "role": "system",
                            "content": """
                You are a helpful assistant .
                The value is the full generated answer in German.
                Max 350 characters, witty, personal message..
                You live decades in the future and write to yourself in 2026.
                Start with a sentence with "In der Zukunft von Wiesbaden..."
                """
                        },
                        {
                            "role": "user",
                            "content": f"""
                Generate an idea for a liveable Wiesbaden, whose function can be described in one line.
                It should be forward-looking and inspiring.
                Topic areas:
                {dice_text}
                """
                        }
                    ],
                )

                ai_text = completion.choices[0].message.content
                print(f"Original: {ai_text}")
                
                # Umlaute ersetzen für Drucker
                ai_text_print = remove_umlauts(ai_text)
                print(f"Zum Drucken: {ai_text_print}")

                # Für Drucker formatieren
                formatted_text = format_for_printer(ai_text_print, gelb_begriff, blau_begriff,pink_begriff)
     
                print(f"Formatiert:\n{formatted_text}")
               
                # Drucken
                #os.system(f'echo "{ai_text_print}" | lp -d Termo')
                os.system(f'echo "{formatted_text}" | lp -d Termo')

                print("✓ Gedruckt!")

                # Button Status zurücksetzen nach erfolgreichem Druck
                state["button"]["pressed"] = False
                print("Button Status auf INAKTIV gesetzt")

        else:
            print("Button Status: INAKTIV")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet")
    print("Finaler State:")
    print(f"  Button: {state['button']}")
"""
MQTT Handler für Würfel-Kommunikation
"""

import paho.mqtt.client as mqtt
import threading
from state import dice_update, get_dice_begriff


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
    
    topic_handlers = {
        "dice/gelb": lambda: dice_update("gelb", value=payload),
        "dice/blau": lambda: dice_update("blau", value=payload),
        "dice/pink": lambda: dice_update("pink", value=payload),
        "dice/gelb/status": lambda: dice_update("gelb", status=payload),
        "dice/blau/status": lambda: dice_update("blau", status=payload),
        "dice/pink/status": lambda: dice_update("pink", status=payload),
    }
    
    handler = topic_handlers.get(message.topic)
    if handler:
        handler()
        farbe = message.topic.split("/")[1]
        if "status" not in message.topic:
            print(f"{farbe.capitalize()} Würfel: {payload} -> {get_dice_begriff(farbe)}")
        else:
            print(f"Status {farbe.capitalize()} Würfel: {payload}")
    else:
        print(f"Unbekanntes Thema: {message.topic}")


def setup_mqtt(broker_ip, port=1883):
    """
    Startet MQTT Client und gibt ihn zurück
    """
    client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    
    client.connect(broker_ip, port, 60)
    
    # Loop in eigenem Thread starten
    def mqtt_loop():
        client.loop_forever()
    
    threading.Thread(target=mqtt_loop, daemon=True).start()
    
    print("MQTT Handler gestartet")
    return client
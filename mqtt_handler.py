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
    
    if message.topic == "dice/gelb":
        dice_update("gelb", value=payload)
        print(f"gelb dice: {payload} -> {get_dice_begriff('gelb')}")
    elif message.topic == "dice/blau":
        dice_update("blau", value=payload)
        print(f"Blauer Würfel: {payload} -> {get_dice_begriff('blau')}")
    elif message.topic == "dice/pink":
        dice_update("pink", value=payload)
        print(f"Pinker Würfel: {payload} -> {get_dice_begriff('pink')}")
    elif message.topic == "dice/gelb/status":
        dice_update("yellow", status=payload)
        print(f"Status yellow Würfel: {payload}")
    elif message.topic == "dice/blau/status":
        dice_update("blau", status=payload)
        print(f"Status Blauer Würfel: {payload}")
    elif message.topic == "dice/pink/status":
        dice_update("pink", status=payload)
        print(f"Status Pinker Würfel: {payload}")
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
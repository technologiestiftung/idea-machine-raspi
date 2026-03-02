import random
import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{
            "1": "Wohnen",
            "2": "Verkehr & Fortbewegung",
            "3": "Stadtplanung",
            "4": "Miteinander & Gemeinschaft",
            "5": "Digitale Stadt",
            "6": "?"
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{
            "1": "Bürger:innen",
            "2": "Kinder & Jugendliche",
            "3": "Verwaltungspersonal",
            "4": "Forscher:innen",
            "5": "Schwächere Gruppen",
            "6": "?"
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{
            "1": "Künstliche Intelligenz & Daten",
            "2": "Web & Apps",
            "3": "Vernetzte Geräte & Sensoren",
            "4": "Spielerische Technik",
            "5": "Virtuelle Realität",
            "6": "?"
        }},
    }
}


def button_pressed():
    state["button"]["pressed"] = True
    state["button"]["last_press"] = time.time()


def dice_update(dice_name, value=None, status=None):
    if dice_name in state["dice"]:
        if value is not None:
            state["dice"][dice_name]["value"] = value
        if status is not None:
            state["dice"][dice_name]["status"] = status


def get_dice_begriff(dice_name):
    """Holt den Begriff für den aktuellen Würfelwert"""
    dice = state["dice"].get(dice_name)
    if dice and dice["value"]:
        begriff = dice["mapping"].get(dice["value"], "N/A")

        if begriff == "?":
            available = [v for k, v in dice["mapping"].items() if v != "?" and k != dice["value"]]
            if available:
                begriff = random.choice(available)
                print(f"  → Zufällig gewählt: {begriff}")
        
        return begriff
    return "N/A"


def update_timestamp():
    state["last_update"] = time.time()
import random
import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{#orange
            "1": "Wohnen",
            "2": "Verkehr & Fortbewegung",
            "3": "Stadtplanung",#Oeffentlicher Raum & Stadgestaltung
            "4": "Miteinander & Gemeinschaft",#Digitale Stadt
            "5": "Digitale Stadt",#Miteinander & Gemeinschaft
            "6": "?"
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{
            "1": "Bürger:innen",
            "2": "Kinder & Jugendliche",#Verwaltungsangestellte
            "3": "Verwaltungspersonal",#Marginalisierte Gruppe
            "4": "Forscher:innen",
            "5": "Schwächere Gruppen",#Unternehmer:innen
            "6": "?"
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{#beige
            "1": "Künstliche Intelligenz & Daten",#Mixed Reality
            "2": "Virtuelle Realität",#Web & Apps
            "3": "Spielerische Technik",#Vernetzte Geräte & Sensoren
            "4": "Vernetzte Geräte & Sensoren",#Spielerische Technik
            "5": "Web & Apps",#Virtuelle Realität
            "6": "?"#Kunstinstallation
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

        # Wenn "?" gewürfelt wurde, zufälligen Begriff wählen
        if begriff == "?":
            available = [v for k, v in dice["mapping"].items() if v != "?" and k != dice["value"]]
            if available:
                begriff = random.choice(available)
                print(f"  → Zufällig gewählt: {begriff}")
        
        return begriff
    return "N/A"


def update_timestamp():
    state["last_update"] = time.time()
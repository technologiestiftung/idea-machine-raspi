import time
import random

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{
            "1": "Wohnen",
            "2": "Mobilitaet & Verkehr",
            "3": "Oeffentlicher Raum",
            "4": "Energie",
            "5": "Klimaschutz",
            "6": "?"
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{
            "1": "Buerger:innen",
            "2": "Verwaltungsangestellte",
            "3": "Marginalisierte Gruppe",
            "4": "Forscher:innen",
            "5": "Unternehmer:innen",
            "6": "?"
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{
            "1": "Mixed Reality",
            "2": "Machine learning & AI",
            "3": "Website & App",
            "4": "IoT",
            "5": "?",
            "6": "Kunstinstallation"
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
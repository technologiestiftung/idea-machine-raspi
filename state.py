import random
import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{ # Charakterwürfel
            "1": "Sammlungskurator:in (Museum)",
            "2": "Technische:r Direktor:in (Theater)",
            "3": "Performance-Künstler:in (Kollektiv)",
            "4": "Personalmitarbeiter:in (Opernhaus)",
            "5": "Kommunikationsmanager:in (Literaturhaus)",
            "6": "Outreach-Referent:in (Gedenkstätte)"
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{ # Zielwürfel
            "1": "Sichtbarkeit steigern",
            "2": "Team-Zusammenarbeit",
            "3": "Neue Formate",
            "4": "Barrierefreiheit",
            "5": "IT-Sicherheit",
            "6": "Digitale Souveränität"
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{ # Lösungszutat
            "1": "30 Stunden Arbeitszeit",
            "2": "HelpDesk-Sprechstunde",
            "3": "Meeting mit Geschäftsführung",
            "4": "Ehrenamtlicher IT-Admin",
            "5": "Eine Tarnkappe",
            "6": "50.000 € (anonym)"
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
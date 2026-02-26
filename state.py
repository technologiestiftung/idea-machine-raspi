import random
import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{ # Charakterwürfel
            "1": "Sammlungskurator:in eines Museums",
            "2": "Technische:r Direktor:in am Theater",
            "3": "Performance-Künstler:in in einem Kollektiv",
            "4": "Personalmitarbeiter:in eines Opernhauses",
            "5": "Kommunikationsmanager:in eines Literaturhauses",
            "6": "Outreach-Referent:in einer Gedenkstätte"
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{ # Zielwürfel
            "1": "Sichtbarkeit der eigenen Angebote steigern",
            "2": "Im Team effizienter zusammenarbeiten",
            "3": "Neue künstlerische Formate entwickeln",
            "4": "Digitale Barrierefreiheit erhöhen",
            "5": "IT-Sicherheit erhöhen",
            "6": "Digitale Souveränität steigern"
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{ # Lösungszutat
            "1": "30 Stunden Arbeitszeit",
            "2": "Sprechstunde beim kulturBdigital-HelpDesk",
            "3": "Ein persönliches Meeting mit der Geschäftsführung",
            "4": "Ein ehrenamtlicher IT-Admin",
            "5": "Eine Tarnkappe",
            "6": "50.000 Euro von einem:einer anonymen Spender:in"
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
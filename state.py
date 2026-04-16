import random
import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected","mapping":{ # Charakterwürfel
            "1": {
                "prompt": "Sammlungskurator:in",
                "print": "Sammlungskurator:in",
                "institutions": [
                    "Museum",
                    "Museum für zeitgenössische Kunst",
                    "Museum für Naturkunde",
                    "Archiv",
                    "kulturhistorisches Museum",
                    "Ausstellungshaus"
                ]
            },
            "2": {
                "prompt": "Technische:r Leiter:in",
                "print": "Technische Leitung",
                "institutions": [
                    "Theater",
                    "Museum",
                    "Ausstellungshaus",
                    "Kulturzentrum",
                    "Opernhaus",
                    "Konzerthaus",
                    "Performance-Ort"
                ]
            },
            "3": {
                "prompt": "Performance-Künstler:in",
                "print": "Performance-Künstler:in",
                "institutions": ["Kollektiv"]
            },
            "4": {
                "prompt": "Personalmitarbeiter:in",
                "print": "HR-Mitarbeiter:in",
                "institutions": [
                    "Opernhaus",
                    "Museum",
                    "Ausstellungshaus",
                    "Theater",
                    "Konzerthaus",
                    "Literaturhaus",
                    "Gedenkstätte",
                    "Erinnerungsort",
                    "Bibliothek",
                    "Archiv",
                    "Jugendkunstschule",
                    "Musikschule",
                    "Musiktheater"
                ]
            },
            "5": {
                "prompt": "Kommunikationsmanager:in",
                "print": "Kommunikationsmanager:in",
                "institutions": [
                    "Museum",
                    "Ausstellungshaus",
                    "Theater",
                    "Opernhaus",
                    "Konzerthaus",
                    "Literaturhaus",
                    "Gedenkstätte",
                    "Erinnerungsort",
                    "Bibliothek",
                    "Archiv",
                    "Jugendkunstschule",
                    "Musikschule",
                    "Musiktheater"
                ]
            },
            "6": {
                "prompt": "Outreach-Referent:in",
                "print": "Outreach-Referent:in",
                "institutions": [
                    "Gedenkstätte",
                    "Museum",
                    "Ausstellungshaus",
                    "Theater",
                    "Opernhaus",
                    "Orchester",
                    "Literaturhaus",
                    "Musiktheater",
                    "soziokulturelles Zentrum"
                ]
            },
        }},
        "blau": {"value": None, "status": "disconnected","mapping":{ # Zielwürfel
            "1": {"prompt": "Sichtbarkeit der eigenen Angebote steigern", "print": "Sichtbarkeit"},
            "2": {"prompt": "Im Team effizienter zusammenarbeiten", "print": "Effiziente Zusammenarbeit"},
            "3": {"prompt": "Neue künstlerische Formate entwickeln", "print": "Künstlerische Formate"},
            "4": {"prompt": "Digitale Barrierefreiheit erhöhen", "print": "Digitale Barrierefreiheit"},
            "5": {"prompt": "IT-Sicherheit erhöhen", "print": "IT-Sicherheit"},
            "6": {"prompt": "Digitale Souveränität steigern", "print": "Digitale Souveränität"}
        }},        
        "pink": {"value": None, "status": "disconnected","mapping":{ # Lösungszutat
            "1": {"prompt": "30 Stunden Arbeitszeit", "print": "30h Arbeitszeit"},
            "2": {"prompt": "Sprechstunde beim kulturBdigital-HelpDesk", "print": "Sprechstunde kBd-HelpDesk"},
            "3": {"prompt": "Ein persönliches Meeting mit der Geschäftsführung", "print": "Meeting mit Geschäftsführung"},
            "4": {"prompt": "Ein ehrenamtlicher IT-Admin", "print": "Ehrenamtlicher IT-Admin"},
            "5": {"prompt": "Interview mit Lokalzeitung", "print": "Zeitungs-Interview"},
            "6": {"prompt": "50.000 Euro von einem:einer anonymen Spender:in", "print": "50.000 Euro Spende (anonym)"}
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
    """Holt den Begriff für den aktuellen Würfelwert.
    Gibt ein Dict zurück: {"prompt": str, "print": str, "institution": str|None}
    """
    dice = state["dice"].get(dice_name)
    if dice and dice["value"]:
        entry = dice["mapping"].get(dice["value"])

        if entry is None:
            return {"prompt": "N/A", "print": "N/A", "institution": None}

        if isinstance(entry, str):
            if entry == "?":
                available = [v for k, v in dice["mapping"].items() if v != "?" and k != dice["value"]]
                if available:
                    entry = random.choice(available)
                    print(f"  → Zufällig gewählt: {entry}")
            if isinstance(entry, str):
                return {"prompt": entry, "print": entry, "institution": None}

        institution = None
        if entry.get("institutions"):
            institution = random.choice(entry["institutions"])

        return {
            "prompt": entry["prompt"],
            "print": entry["print"],
            "institution": institution
        }

    return {"prompt": "N/A", "print": "N/A", "institution": None}


def update_timestamp():
    state["last_update"] = time.time()
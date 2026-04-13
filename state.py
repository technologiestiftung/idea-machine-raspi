import time

state = {
    "last_update": None,
    "button": {"pressed": False, "last_press": None},
    
    "dice": {
        "gelb": {"value": None, "status": "disconnected"},  # Charakterwürfel (1-6)
        "blau": {"value": None, "status": "disconnected"},  # Zielwürfel (1-6)
        "pink": {"value": None, "status": "disconnected"},  # Lösungszutat (1-6)
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


def update_timestamp():
    state["last_update"] = time.time()
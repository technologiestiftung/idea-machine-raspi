"""
Hilfsfunktionen für Text-Verarbeitung und Drucker-Formatierung
"""
import textwrap
from datetime import datetime
from constants import PRINTER_WIDTH
import subprocess

ESC_RESET = "\x1b@"


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


def format_for_printer(text, gelb_begriff, blau_begriff, pink_begriff, width=PRINTER_WIDTH):
    """Formatiert Text für 58mm Thermodrucker"""
    lines = []
    
    # Header
    lines.append("=" * width)
    lines.append("KI-Wuerfel Zukunftswerk".center(width))
    lines.append("ZUKUNFTSWERK WIESBADEN".center(width))
    lines.append("=" * width)
    lines.append("Verwendete Begriffe:".center(width))
    
    def add_begriff(begriff):
        # Lange Begriffe manuell splitten
        if begriff in ["Virtuelle Erweiterung der Realitaet", "Vernetzte Geraete & Sensoren"]:
            parts = begriff.split()
            mid = len(parts)//2
            lines.append(" ".join(parts[:mid]).center(width))
            lines.append(" ".join(parts[mid:]).center(width))
        else:
            lines.append(begriff.center(width))

    add_begriff(gelb_begriff)
    add_begriff(blau_begriff)
    add_begriff(pink_begriff)

    lines.append("=" * width)
    lines.append("")

    # ================= AI-TEXT =================
    # Text umbrechen (Wörter nicht abschneiden)
    wrapped_lines = textwrap.wrap(
        text,
        width=width,
        break_long_words=True,
        break_on_hyphens=True
    )
    lines.extend(wrapped_lines)
    lines.append("")

    # ================= FOOTER =================
    lines.append("-" * width)
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    lines.append(timestamp.center(width))
    lines.append("-" * width)

    # Leerzeilen zum Abreißen
    lines.append("")
    lines.append("")
    lines.append("")

    # ================= ESC/POS RESET VOR TEXT =================
    final_text = ESC_RESET + "\n".join(lines) + "\n\n\n"

    return final_text

def generate_ai_prompt(dice_text):
    """Erstellt den Prompt für die AI"""
    system_message = {
        "role": "system",
        "content": """
You are a helpful assistant.
The value is the full generated answer in German.
Max 350 characters, witty, personal message.
You live decades in the future and write to yourself in 2026.
Start with a sentence with "In der Zukunft von Wiesbaden schreibe ich dir aus dem Jahr 2050"
"""
    }
    
    user_message = {
        "role": "user",
        "content": f"""
Generate an idea for a liveable Wiesbaden, whose function can be described in one line.
It should be forward-looking and inspiring.
Topic areas:
{dice_text}
"""
    }
    
    return [system_message, user_message]
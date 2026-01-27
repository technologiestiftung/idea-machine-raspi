"""
Hilfsfunktionen für Text-Verarbeitung und Drucker-Formatierung
"""

from datetime import datetime


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


def format_for_printer(text, gelb_begriff, blau_begriff, pink_begriff, width=26):
    """Formatiert Text für 58mm Thermodrucker"""
    lines = []
    
    # Header
    lines.append("=" * width)
    lines.append("IDEENWUERFEL".center(width))
    lines.append("ZUKUNFTSWERK WIESBADEN".center(width))
    lines.append("=" * width)
    lines.append("Verwendete Begriffe:".center(width))
    lines.append(gelb_begriff.center(width))
    lines.append(blau_begriff.center(width))
    lines.append(pink_begriff.center(width))   
    lines.append("=" * width)
    lines.append("")
    
    # Text umbrechen (Wörter nicht abschneiden)
    words = text.split()
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    lines.append("")
    lines.append("-" * width)
    
    # Timestamp
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    lines.append(timestamp.center(width))
    lines.append("-" * width)
    
    # Leerzeilen zum Abreißen
    lines.append("")
    lines.append("")
    lines.append("")
    
    return "\n".join(lines) + "\n\n\n"


def generate_ai_prompt(dice_text):
    """Erstellt den Prompt für die AI"""
    system_message = {
        "role": "system",
        "content": """
You are a helpful assistant.
The value is the full generated answer in German.
Max 350 characters, witty, personal message.
You live decades in the future and write to yourself in 2026.
Start with a sentence with "In der Zukunft von Wiesbaden..."
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
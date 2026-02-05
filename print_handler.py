import textwrap
from datetime import datetime

from escpos.printer import Usb
from openai import OpenAI

from config import API_KEY, LOGO_PATH, PROJECT_SUBTITLE, PROJECT_TITLE
from utils import generate_ai_prompt, process_image_for_print


def handle_print(term_city_theme, term_target_group, term_technologies):
    # OpenAI Client
    openai_client = OpenAI(api_key=API_KEY)

    LINE_WIDTH = 32

    # -------- TEXT GENERATION --------
    headline = "Verwendete Begriffe:"

    # generate AI text
    dice_text = f"Stadtthema: {term_city_theme}\n Zielgruppe: {term_target_group}\n Technologien: {term_technologies}"
    messages = generate_ai_prompt(dice_text)

    print("Generiere KI-Text...")

    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )

    ai_text = completion.choices[0].message.content
    print(f"Fertig! Text: {ai_text[:50]}...")

    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")

    # -------- DRUCKER --------
    # Drucker verbinden mit korrekten Endpoint-Adressen & initialisieren
    p = Usb(0x0456, 0x0808, in_ep=0x81, out_ep=0x3, profile="POS-5890")
    p.hw("init")

    # Bild für Thermaldrucker vorbereiten
    processed_image = process_image_for_print(LOGO_PATH, target_width=384)

    # Druck
    if processed_image:
        p.image(processed_image, high_density_vertical=True, high_density_horizontal=True)
    else:
        print("Fehler beim Verarbeiten des Bildes")

    p.text("\n\n")

    # Trennlinie + Title
    p.set(align='center')
    p.text("=" * LINE_WIDTH + "\n")
    p.text(f"{PROJECT_TITLE}\n{PROJECT_SUBTITLE}\n")
    p.text("=" * LINE_WIDTH + "\n\n")

    # Begriffe mit Umbruch
    p.text(f"{headline}\n")
    wrapped_gelb = textwrap.fill(term_city_theme, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
    wrapped_blau = textwrap.fill(term_target_group, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
    wrapped_pink = textwrap.fill(term_technologies, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
    p.text(f"{wrapped_gelb}\n{wrapped_blau}\n{wrapped_pink}\n")
    p.text("-" * LINE_WIDTH + "\n\n")

    # Haupttext mit Umbruch
    p.set(align='left')
    wrapped_text = textwrap.fill(ai_text, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
    p.text(f"{wrapped_text}\n\n")

    # Timestamp
    p.set(align='center')
    p.text("-" * LINE_WIDTH + "\n")
    p.text(f"{timestamp}\n")
    p.text("-" * LINE_WIDTH + "\n")

    p.cut()
    p.close()
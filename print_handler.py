import textwrap
from datetime import datetime

from escpos.printer import Usb
from openai import OpenAI

from config import API_KEY, LOGO_PATH, PROJECT_SUBTITLE, PROJECT_TITLE
from utils import generate_ai_prompt, process_image_for_print


def handle_print(term_character, term_goal, term_solution):
    openai_client = OpenAI(api_key=API_KEY)
    LINE_WIDTH = 32

    # -------- TEXT GENERATION --------
    headline = "Verwendete Begriffe:"
    messages = generate_ai_prompt(term_character, term_goal, term_solution)

    print("Generiere KI-Text...")
    
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
        ai_text = completion.choices[0].message.content
        print(f"Fertig! Text: {ai_text[:50]}...")
    except Exception as e:
        print(f"OpenAI API Fehler: {e}")
        return "api_error"
    
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")

    # -------- DRUCKER --------
    try:
        p = Usb(0x0456, 0x0808, in_ep=0x81, out_ep=0x3, profile="POS-5890")
        p.hw("init")

        processed_image = process_image_for_print(LOGO_PATH, target_width=384)

        if processed_image:
            p.image(processed_image, high_density_vertical=True, high_density_horizontal=True)
        else:
            print("Fehler beim Verarbeiten des Bildes")

        p.text("\n\n")
        p.set(align='center')
        p.text("=" * LINE_WIDTH + "\n")
        p.text(f"{PROJECT_TITLE}\n{PROJECT_SUBTITLE}\n")
        p.text("=" * LINE_WIDTH + "\n\n")
        p.text(f"{headline}\n")
        
        wrapped_character = textwrap.fill(term_character, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        wrapped_goal = textwrap.fill(term_goal, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        wrapped_solution = textwrap.fill(term_solution, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        p.text(f"{wrapped_character}\n{wrapped_goal}\n{wrapped_solution}\n")
        p.text("-" * LINE_WIDTH + "\n\n")

        p.set(align='left')
        wrapped_text = textwrap.fill(ai_text, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        p.text(f"{wrapped_text}\n\n")

        p.set(align='center')
        p.text("-" * LINE_WIDTH + "\n")
        p.text(f"{timestamp}\n")
        p.text("-" * LINE_WIDTH + "\n")

        p.cut()
        p.close()
        
        return "success"
        
    except Exception as e:
        print(f"Druckerfehler: {e}")
        return "printer_error"
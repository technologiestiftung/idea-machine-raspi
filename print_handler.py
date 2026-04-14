import json
import textwrap
from datetime import datetime

from escpos.printer import Usb
from mistralai.client import Mistral

from config import (LOGO_PATH, MISTRAL_AGENT_ID, MISTRAL_API_KEY,
                    PROJECT_SUBTITLE, PROJECT_TITLE)
from utils import process_image_for_print


def handle_print(term_character, term_goal, term_solution):
    mistral_client = Mistral(api_key=MISTRAL_API_KEY)
    LINE_WIDTH = 32

    # -------- TEXT GENERATION --------
    headline = "Verwendete Begriffe:"
    user_message = f"PERSON: {term_character} | ZIEL: {term_goal} | ZUTAT: {term_solution}"

    print("Generiere KI-Text...")
    
    try:
        response = mistral_client.beta.conversations.start(
            agent_id=MISTRAL_AGENT_ID,
            inputs=[{"role": "user", "content": user_message}]
        )
        
        # Extract text from Mistral response (original working code)
        ai_text = ""
        
        for entry in response.outputs:
            if entry.type == "message.output":
                for chunk in entry.content:
                    if chunk.type == "text":
                        data = json.loads(chunk.text)
                        ai_text = data["text"]
        
        if not ai_text:
            raise ValueError("No text returned from Mistral agent")
        
        print(f"Fertig! Text: {ai_text[:50]}...")
    except Exception as e:
        print(f"Mistral API Fehler: {e}")
        import traceback
        traceback.print_exc()
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
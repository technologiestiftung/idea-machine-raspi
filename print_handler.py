import textwrap
from datetime import datetime

from escpos.printer import Usb
from mistralai.client import Mistral

from config import (LOGO_PATH, MISTRAL_AGENT_ID, MISTRAL_API_KEY,
                    PROJECT_SUBTITLE, PROJECT_TITLE)
from utils import process_image_for_print


def handle_print(
    dice_a,
    dice_b,
    dice_c,
    label_a="PERSON",
    label_b="ZIEL",
    label_c="ZUTAT"
):
    """
    Beispiele für Labels:
    - Mistral: PERSON / ZIEL / ZUTAT
    - OpenAI alt: Stadtthema / Zielgruppe / Technologien
    """

    mistral_client = Mistral(api_key=MISTRAL_API_KEY)
    LINE_WIDTH = 32

    # -------- TEXT GENERATION --------
    headline = "Verwendete Begriffe:"

    user_message = (
        f"{label_a}: {dice_a} | "
        f"{label_b}: {dice_b} | "
        f"{label_c}: {dice_c}"
    )

    print("Generiere KI-Text...")

    try:
        response = mistral_client.agents.complete(
            agent_id=MISTRAL_AGENT_ID,
            messages=[{"role": "user", "content": user_message}],
            response_format={"type": "text"}
        )

        ai_text = response.choices[0].message.content

        if isinstance(ai_text, list):
            ai_text = "".join(
                chunk.text for chunk in ai_text if hasattr(chunk, "text")
            )

        if not ai_text:
            raise ValueError("No text returned from Mistral agent")

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

        processed_image = process_image_for_print(
            LOGO_PATH,
            target_width=384
        )

        if processed_image:
            p.image(
                processed_image,
                high_density_vertical=True,
                high_density_horizontal=True
            )
        else:
            print("Fehler beim Verarbeiten des Bildes")

        p.text("\n\n")
        p.set(align='center')
        p.text("=" * LINE_WIDTH + "\n")
        p.text(f"{PROJECT_TITLE}\n{PROJECT_SUBTITLE}\n")
        p.text("=" * LINE_WIDTH + "\n\n")

        p.text(f"{headline}\n")

        wrapped_a = textwrap.fill(dice_a, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        wrapped_b = textwrap.fill(dice_b, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)
        wrapped_c = textwrap.fill(dice_c, width=LINE_WIDTH, break_long_words=True, break_on_hyphens=False)

        p.text(f"{wrapped_a}\n{wrapped_b}\n{wrapped_c}\n")
        p.text("-" * LINE_WIDTH + "\n\n")

        p.set(align="left")
        wrapped_text = textwrap.fill(ai_text, width=LINE_WIDTH)
        p.text(f"{wrapped_text}\n\n")

        p.set(align="center")
        p.text("-" * LINE_WIDTH + "\n")
        p.text(f"{timestamp}\n")
        p.text("-" * LINE_WIDTH + "\n")

        p.cut()
        p.close()

        return "success"

    except Exception as e:
        print(f"Druckerfehler: {e}")
        return "printer_error"
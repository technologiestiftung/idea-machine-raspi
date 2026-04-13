"""
Lokales Testskript – testet nur print_handler mit echtem Mistral.
"""

import os
import sys
import types


def install_stubs():
    rpi_mod = types.ModuleType("RPi")
    gpio_mod = types.ModuleType("RPi.GPIO")
    gpio_mod.HIGH = 1; gpio_mod.LOW = 0; gpio_mod.BCM = 11
    gpio_mod.OUT = 0; gpio_mod.IN = 1; gpio_mod.PUD_UP = 22
    gpio_mod.output = lambda *_, **__: None
    gpio_mod.setmode = lambda *_, **__: None
    gpio_mod.setup = lambda *_, **__: None
    gpio_mod.cleanup = lambda *_, **__: None
    rpi_mod.GPIO = gpio_mod
    sys.modules["RPi"] = rpi_mod
    sys.modules["RPi.GPIO"] = gpio_mod

    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

    dotenv_mod = types.ModuleType("dotenv")
    dotenv_mod.load_dotenv = lambda *_, **__: None
    sys.modules["dotenv"] = dotenv_mod

    class FakeUsb:
        def __init__(self, *_, **__):
            self._out = []
        def hw(self, _): pass
        def image(self, *_, **__): self._out.append("[IMAGE]")
        def text(self, txt): self._out.append(txt)
        def set(self, **kw): self._out.append(f"[ALIGN: {kw.get('align', 'left')}]")
        def cut(self): self._out.append("[CUT]")
        def close(self): pass
        def get_output(self): return "".join(self._out)

    escpos_mod = types.ModuleType("escpos")
    printer_mod = types.ModuleType("escpos.printer")
    printer_mod.Usb = FakeUsb
    escpos_mod.printer = printer_mod
    sys.modules["escpos"] = escpos_mod
    sys.modules["escpos.printer"] = printer_mod


def run():
    install_stubs()

    from escpos.printer import Usb

    import print_handler

    print_handler.process_image_for_print = lambda *_, **__: None

    fake_printer = None
    original_usb = Usb

    def usb_wrapper(*args, **kwargs):
        nonlocal fake_printer
        fake_printer = original_usb(*args, **kwargs)
        return fake_printer

    print_handler.Usb = usb_wrapper

    if not os.getenv("MISTRAL_API_KEY") or not os.getenv("MISTRAL_AGENT_ID"):
        raise RuntimeError("MISTRAL_API_KEY und MISTRAL_AGENT_ID fehlen in .env")

    print("Testing Mistral + Printer...")
    result = print_handler.handle_print("4", "5", "6")
    assert result == "success"

    print("\n" + "=" * 60)
    print("DRUCKAUSGABE:")
    print("=" * 60)
    print(fake_printer.get_output() if fake_printer else "(kein Output)")
    print("=" * 60)
    print("✓ OK\n")


if __name__ == "__main__":
    run()
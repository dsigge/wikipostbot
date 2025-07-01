from playwright.sync_api import sync_playwright
from datetime import date
import os

def capture_sections():
    today = date.today().strftime("%Y-%m-%d")
    output_dir = "screenshots"

    # Ordner erstellen, falls nicht vorhanden
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1200, "height": 2000},
            device_scale_factor=2
        )
        page.goto("https://de.wikipedia.org/wiki/Wikipedia:Hauptseite", timeout=15000)

        selectors = {
            "schon_gewusst": "#wissenswertes.hauptseite-box",
            "was_geschah": "#ereignisse.hauptseite-box",
            "verstorbene": "#verstorbene.hauptseite-box",
            "nachrichten": "#nachrichten.hauptseite-box"
        }

        for name, selector in selectors.items():
            try:
                print(f"📸 Versuche Screenshot von {name}...")
                element = page.locator(selector)
                path = os.path.join(output_dir, f"screenshot_{name}_{today}.png")
                element.screenshot(path=path, timeout=15000)
                print(f"✅ Screenshot gespeichert: {path}")
            except Exception as e:
                print(f"❌ Fehler bei {name}: {e}")

        browser.close()

if __name__ == "__main__":
    print("🎬 Starte Bereichs-Screenshots")
    capture_sections()

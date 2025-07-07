from PIL import Image, ImageDraw, ImageFont
from datetime import date
import os

def embed_into_template(input_path, output_path):
    template_size = (1080, 1350)

        # Wochentag als Zahl (0=Montag, 6=Sonntag)
    weekday = date.today().weekday()

    # Definiere Farben für jeden Wochentag (hell und pastellig)
    weekday_colors = [
        (255, 230, 230),  # Montag: helles Rosa
        (230, 255, 230),  # Dienstag: helles Grün
        (230, 230, 255),  # Mittwoch: helles Blau
        (255, 255, 230),  # Donnerstag: helles Gelb
        (255, 230, 255),  # Freitag: helles Pink
        (230, 255, 255),  # Samstag: helles Türkis
        (245, 245, 245)   # Sonntag: helles Grau
    ]
    
    background_color = weekday_colors[weekday]

    # Hintergrund mit der entsprechenden Farbe anlegen
    background = Image.new("RGB", template_size, color=background_color)

    # Screenshot laden
    screenshot = Image.open(input_path)
    max_width, max_height = 1000, 1250  # Fast randlos, aber mit minimalem Weiß

    # Verhältnis berechnen und skalieren
    ratio = min(max_width / screenshot.width, max_height / screenshot.height)
    new_size = (int(screenshot.width * ratio), int(screenshot.height * ratio))
    screenshot = screenshot.resize(new_size, Image.LANCZOS)

    # Zentriert einfügen
    x = (template_size[0] - screenshot.width) // 2
    y = (template_size[1] - screenshot.height) // 2
    background.paste(screenshot, (x, y))

    # Datum einfügen
    draw = ImageDraw.Draw(background)
    today = date.today().strftime("%d.%m.%Y")
    draw.text((30, 1300), f"📅 {today}", fill=(100, 100, 100))

    # Logo (optional)
    #logo_path = "assets/wikipedia_logo.png"
    #if os.path.exists(logo_path):
    #    logo = Image.open(logo_path).convert("RGBA")
    #    logo = logo.resize((80, 80))
    #    background.paste(logo, (960, 30), logo)

    # Speichern
    background.save(output_path)
    print(f"✅ Gespeichert: {output_path}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    names = ["schon_gewusst", "was_geschah", "verstorbene", "nachrichten"]

    # Ordner 'posts' anlegen, falls nicht existent
    os.makedirs("posts", exist_ok=True)

    for name in names:
        input_file = f"screenshots/screenshot_{name}_{today}.png"
        output_file = f"posts/post_{name}_{today}.png"
        if os.path.exists(input_file):
            embed_into_template(input_file, output_file)
        else:
            print(f"⚠️ Nicht gefunden: {input_file}")

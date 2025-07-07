from PIL import Image, ImageDraw, ImageFont
from datetime import date
import os

def embed_into_template(input_path, output_path):
    template_size = (1080, 1350)
    
    # Wochentag als Zahl (0=Montag, 6=Sonntag)
    weekday = date.today().weekday()

    # Deine Wunschfarben für die Wochentage Montag bis Sonntag
    weekday_colors = [
        (195, 223, 224),  # Montag - #C3DFE0 Light blue
        (188, 217, 121),  # Dienstag - #BCD979 Pistachio
        (157, 173, 111),  # Mittwoch - #9DAD6F Olivine
        (125, 109, 97),   # Donnerstag - #7D6D61 Dim gray
        (94, 87, 77),     # Freitag - #5E574D Walnut brown
        (205, 197, 180),  # Samstag - #CDC5B4
        (181, 157, 164)   # Sonntag - #B59DA4
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

    # Speichern
    background.save(output_path)
    print(f"✅ Gespeichert: {output_path}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    names = ["schon_gewusst", "was_geschah", "verstorbene", "nachrichten"]

    for name in names:
        input_file = f"screenshots/screenshot_{name}_{today}.png"
        output_file = f"posts/post_{name}_{today}.png"
        if os.path.exists(input_file):
            embed_into_template(input_file, output_file)
        else:
            print(f"⚠️ Nicht gefunden: {input_file}")

from instagrapi import Client
from datetime import date
import os

def upload_carousel(image_paths, caption):
    username = "DEIN_NUTZERNAME"
    password = "DEIN_PASSWORT"

    cl = Client()
    cl.login(username, password)

    media = cl.album_upload(image_paths, caption)
    print(f"✅ Karussell hochgeladen: {media.pk}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")

    base_path = "posts"
    names_in_order = [
        "was_geschah",
        "verstorbene",
        "schon_gewusst",
        "nachrichten"  # Achtung: Muss auch vorbereitet/generiert werden
    ]

    image_paths = []
    for name in names_in_order:
        file_path = f"{base_path}/post_{name}_{today}.png"
        if os.path.exists(file_path):
            image_paths.append(file_path)
        else:
            print(f"⚠️ Nicht gefunden: {file_path}")

    if len(image_paths) >= 2:
        caption = f"Wikipedia Aktuell ({today})\n#Wikipedia #Wissenspost #SchonGewusst"
        upload_carousel(image_paths, caption)
    else:
        print("❌ Nicht genug Bilder für Karussell gefunden.")

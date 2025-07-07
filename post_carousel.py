import requests
import re
import pickle
from googleapiclient.discovery import build

# --- Facebook / Instagram Config ---
ACCESS_TOKEN = 'EAAJdgaDJ9ssBPA9IVpyDJj24s73WlZCS1sqmc4xLANXZBulWrqFjUbA6tgpPQMUfWNOCrL9J3tJ4WcjZBrkMZA2H2n6c3DI43ZC2sVgh7gZBvT5okjORBHBqEUousi9nNjHMgon6SXe4Q4ZBwMvPbsrpaSDGIHH0268CVgpN1CtAH6YMYXEbQq8KwJFU3y26SQUjnb5aX6CciZBJsPKCZBpPZA4yZB9O6eXsp3WHViX2ygZD'
IG_USER_ID = '17841475804937049'  # z.B. '17841475084937049'
BASE_URL = 'https://graph.facebook.com/v17.0'

# --- Google Drive Config ---
GOOGLE_DRIVE_FOLDER_ID = '19bJM0jfSKvfVerxHYdMP5o0HPvOtycs3'  # Dein Drive-Ordner

# Erwartete Dateistarts für die Carousel-Bilder
EXPECTED_PREFIXES = [
    "post_schon_gewusst",
    "post_was_geschah",
    "post_verstorbene",
    "post_nachrichten"
]

def list_files_in_drive_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

def filter_files(files, prefixes):
    filtered = []
    for prefix in prefixes:
        # Suche für jeden prefix genau eine Datei (z.B. die neuste, oder die mit heutigem Datum)
        candidates = [f for f in files if f['name'].startswith(prefix)]
        if not candidates:
            print(f"⚠️ Keine Datei gefunden für Prefix '{prefix}'")
            continue
        # Optional: Sortiere nach Datum im Dateinamen, nehme die neueste
        candidates.sort(key=lambda f: extract_date_from_filename(f['name']) or '', reverse=True)
        filtered.append(candidates[0])
    return filtered

def extract_date_from_filename(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else None

def build_direct_download_url(file_id):
    # Für öffentliche Dateien: direkt nutzbare URL für Instagram
    return f"https://drive.google.com/uc?export=view&id={file_id}"

# --- Instagram Graph API Methoden ---

def create_media_object(image_url, caption=""):
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['id']

def create_carousel_container(media_ids):
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    children = ",".join(media_ids)
    params = {
        'media_type': 'CAROUSEL',
        'children': children,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['id']

def publish_media(container_id):
    url = f"{BASE_URL}/{IG_USER_ID}/media_publish"
    params = {
        'creation_id': container_id,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

# --- Hauptlogik ---

def main():
    # Google Drive API initialisieren
    with open('token.pickle', 'rb') as token_file:
        creds = pickle.load(token_file)
    drive_service = build('drive', 'v3', credentials=creds)

    # Alle Dateien im Google Drive Ordner listen
    all_files = list_files_in_drive_folder(drive_service, GOOGLE_DRIVE_FOLDER_ID)

    # Gefilterte Dateien (für Carousel) holen
    carousel_files = filter_files(all_files, EXPECTED_PREFIXES)

    if len(carousel_files) < len(EXPECTED_PREFIXES):
        print("⚠️ Nicht alle erforderlichen Bilder gefunden. Abbruch.")
        return

    print("Gefundene Dateien für Carousel:")
    for f in carousel_files:
        print(f" - {f['name']} (ID: {f['id']})")

    # Medien-IDs für Instagram vorbereiten
    media_ids = []
    for f in carousel_files:
        image_url = build_direct_download_url(f['id'])
        caption = f"Wikipost: {f['name']}"
        print(f"Erstelle Medienobjekt für {f['name']} mit URL {image_url}")
        media_id = create_media_object(image_url, caption)
        media_ids.append(media_id)

    # Carousel Container erstellen
    carousel_id = create_carousel_container(media_ids)
    print(f"Carousel Container erstellt mit ID: {carousel_id}")

    # Carousel posten
    publish_result = publish_media(carousel_id)
    print(f"Carousel veröffentlicht: {publish_result}")

if __name__ == "__main__":
    main()

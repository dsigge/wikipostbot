import os
import re
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def list_files_in_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    return files

def delete_all_files_in_folder(service, folder_id):
    files = list_files_in_folder(service, folder_id)
    if not files:
        print("🗑️ Keine Dateien zum Löschen gefunden.")
    else:
        print("🗑️ Dateien im Google Drive Ordner vor dem Löschen:")
        for file in files:
            print(f"  - {file['name']} (ID: {file['id']})")

    for file in files:
        try:
            service.files().delete(fileId=file['id']).execute()
            print(f"🗑️ Datei gelöscht: {file['name']} (ID: {file['id']})")
        except Exception as e:
            print(f"⚠️ Fehler beim Löschen von Datei {file['name']} (ID: {file['id']}): {e}")

    # Nach dem Löschen nochmal checken
    files_after = list_files_in_folder(service, folder_id)
    if not files_after:
        print("✅ Alle Dateien erfolgreich gelöscht.")
    else:
        print("⚠️ Einige Dateien konnten nicht gelöscht werden:")
        for file in files_after:
            print(f"  - {file['name']} (ID: {file['id']})")

def extract_date_from_filename(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else "kein Datum gefunden"

def upload_file(service, file_path, folder_id=None):
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        date_str = extract_date_from_filename(os.path.basename(file_path))
        print(f'✅ Datei hochgeladen: {file_path} (Datum: {date_str}) (ID: {file.get("id")})')
    except Exception as e:
        print(f"⚠️ Fehler beim Hochladen von {file_path}: {e}")

def upload_folder(folder_path, folder_id=None):
    with open('token.pickle', 'rb') as token_file:
        creds = pickle.load(token_file)
    service = build('drive', 'v3', credentials=creds)

    if folder_id:
        delete_all_files_in_folder(service, folder_id)

    local_files = os.listdir(folder_path)
    if not local_files:
        print(f"⚠️ Keine lokalen Dateien im Ordner '{folder_path}' zum Hochladen gefunden.")
    else:
        print(f"📁 Lokale Dateien im Ordner '{folder_path}':")
        for f in local_files:
            print(f"  - {f}")

    for filename in local_files:
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            upload_file(service, full_path, folder_id)

if __name__ == '__main__':
    GOOGLE_DRIVE_FOLDER_ID = '19bJM0jfSKvfVerxHYdMP5o0HPvOtycs3'  # Deine Ordner-ID
    upload_folder('posts', GOOGLE_DRIVE_FOLDER_ID)

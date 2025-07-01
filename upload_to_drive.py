import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def delete_all_files_in_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    for file in files:
        service.files().delete(fileId=file['id']).execute()
        print(f"🗑️ Datei gelöscht: {file['name']} (ID: {file['id']})")

def upload_file(service, file_path, folder_id=None):
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'✅ Datei hochgeladen: {file_path} (ID: {file.get("id")})')

def upload_folder(folder_path, folder_id=None):
    with open('token.pickle', 'rb') as token_file:
        creds = pickle.load(token_file)
    service = build('drive', 'v3', credentials=creds)

    if folder_id:
        delete_all_files_in_folder(service, folder_id)

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            upload_file(service, full_path, folder_id)

if __name__ == '__main__':
    GOOGLE_DRIVE_FOLDER_ID = '19bJM0jfSKvfVerxHYdMP5o0HPvOtycs3'  # Deine Ordner-ID
    upload_folder('assets', GOOGLE_DRIVE_FOLDER_ID)

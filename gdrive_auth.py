from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

# Die API-Scopes, die du brauchst (für Drive)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Token speichern
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    print("✅ Token erfolgreich erzeugt und gespeichert.")

if __name__ == '__main__':
    main()

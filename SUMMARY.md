# Wikipostbot – Projektzusammenfassung

**Projektziel:**  
Automatisierte tägliche Erstellung von Wikipedia-Bereichs-Screenshots, Umwandlung zu Instagram-Assets und Upload dieser Bilder in einen Google Drive Ordner.

---

## Was wurde umgesetzt?

1. **Screenshot-Erstellung**  
   - Python-Script `screenshot_wikipedia.py` nutzt Playwright, um ausgewählte Bereiche der deutschen Wikipedia-Hauptseite (Schon gewusst?, Was geschah?, Verstorbene, Nachrichten) täglich zu screenshotten.  
   - Screenshots werden lokal im Ordner `screenshots/` oder `assets/` gespeichert.

2. **Asset-Erstellung**  
   - Script `generate_instagram_post.py` verarbeitet die Screenshots und erstellt quadratische Instagram-kompatible Bilder (Instagram-Kacheln) im Ordner `assets/`.

3. **Automatischer Upload zu Google Drive**  
   - Script `upload_to_drive.py` löscht vor dem Upload alte Dateien im definierten Google Drive Ordner und lädt die neuen Assets hoch.  
   - Google OAuth-Credentials und Token werden sicher als GitHub Secrets gespeichert und im Workflow als Dateien erzeugt.

4. **GitHub Actions Workflow**  
   - Der gesamte Prozess (Screenshots, Asset-Generierung, Upload) läuft täglich automatisch per GitHub Actions mit einem Cron-Job um 09:30 MESZ.  
   - Secrets (`credentials.json` und `token.pickle` als Base64) werden im GitHub-Repo sicher verwaltet.  
   - Alte lokale Dateien werden vor dem Lauf im Workflow gelöscht, um Speicher zu sparen.

5. **Sicherheit**  
   - Sensible Daten werden nicht ins Repository hochgeladen, sondern über GitHub Secrets verwaltet.  
   - Zugriff auf Google Drive erfolgt über OAuth-Token mit begrenztem Scope.

---

## Hinweise & Empfehlungen

- Workflow-Logs regelmäßig prüfen, um reibungslosen Ablauf sicherzustellen.  
- OAuth-Zugangsdaten müssen ggf. erneuert werden, wenn Token ablaufen.  
- Optional: Automatisches Löschen der Google Drive Dateien vor Upload als Teil des Upload-Skripts integriert.  
- Erweiterungen möglich, z.B. automatisches Posten auf Instagram via API oder Zapier.

---

## Verwendete Technologien

- Python (Playwright, Pillow, google-api-python-client)  
- GitHub Actions für CI/CD und Scheduling  
- Google Drive API für Datei-Management  
- GitHub Secrets für sichere Speicherung von Zugangsdaten

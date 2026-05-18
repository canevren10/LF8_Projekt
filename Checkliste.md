# LF8-Projekt: Schritt-für-Schritt Checkliste

## Phase 1: Lokale Einrichtung (MariaDB, Python, Cursor Workspace)

- [x] Projektordner in Cursor öffnen, z. B. `LF8_Projekt`.
- [x] Auf dem Mac Homebrew prüfen: `brew --version`.
- [x] Falls Homebrew fehlt, Homebrew installieren.
- [x] MariaDB lokal installieren: `brew install mariadb`.
- [x] MariaDB starten: `brew services start mariadb`.
- [x] MariaDB testen: `mariadb -u root -p`.
- [x] Lokale Datenbank erstellen: `CREATE DATABASE datenbankname;`.
- [x] SQL-Datei lokal importieren: `mariadb -u root -p datenbankname < datei.sql`.
- [x] Import prüfen mit `SHOW DATABASES;`, `USE datenbankname;` und `SELECT * FROM tabellenname;`.
- [x] Python 3 auf dem Mac prüfen: `python3 --version`.
- [x] Virtuelle Python-Umgebung erstellen: `python3 -m venv .venv`.
- [x] Virtuelle Umgebung aktivieren: `source .venv/bin/activate`.
- [x] Benötigte Bibliotheken installieren: `pip install mariadb`.
- [x] Projektdateien für die Meilensteine anlegen, z. B. `01_ConnectionTest.py`, `02_Print_SQL.py`, `03_DB_in_CSV.py`.
- [x] Zugangsdaten lokal notieren: Host `localhost`, Benutzer:root, Passwort:123, Datenbankname:heiner_it.
- [x] Erst lokal testen, bevor der Server benutzt wird.
- [ ] Später Serverzugang nur im BYOD-WLAN testen.
- [ ] Für Serverzugriff die IP, Benutzer `root`, Passwort und Datenbankname aus dem Lehrer-PDF nutzen.
- [ ] Falls nötig, MariaDB auf dem Server für Remotezugriff vorbereiten: `bind-address = 0.0.0.0`.
- [ ] Server-Datenbank importieren und mit einer einfachen SQL-Abfrage testen.

## Phase 2: Meilensteine (Codierungsaufgaben 1.1 bis 1.7)

- [ ] 1.0 Quellcode dokumentieren.
- [x] Wichtige Variablen, Methoden und Funktionen direkt im Code mit `#` kurz erklären.
- [x] Genutzte Bibliotheken kurz erklären, z. B. `mariadb`, `csv`, `xml`, `tkinter` (in `21_dropdown-vorlage.py` für `tkinter`).

- [x] 1.1 Python-Datei für den Verbindungstest öffnen oder erstellen.
- [x] MariaDB-Bibliothek importieren.
- [x] Verbindungsdaten eintragen: Server-IP oder `localhost`, Benutzer, Passwort, Datenbankname.
- [x] Verbindung zur Datenbank herstellen.
- [x] Erfolgsmeldung ausgeben, wenn die Verbindung funktioniert.
- [x] Fehler abfangen und verständlich ausgeben.
- [x] Verbindungstest lokal ausführen.

- [x] 1.2 SQL-Abfrage für alle Mitarbeiter schreiben.
- [x] SQL-Abfrage in Python ausführen.
- [x] Ergebnis in der Kommandozeile mit `print()` ausgeben.
- [x] Prüfen, ob alle Mitarbeiter korrekt angezeigt werden.

- [x] 1.3 Programm für CSV-Ausgabe erstellen.
- [x] SQL-Abfrage für den gesamten Lagerbestand schreiben.
- [x] Ergebnis der SQL-Abfrage in eine CSV-Datei schreiben.
- [x] Spaltennamen in die CSV-Datei schreiben.
- [x] CSV-Datei öffnen und prüfen, ob alle Lagerdaten vorhanden sind.
- [x] CSV-Datei testweise in Excel oder Numbers öffnen.

- [x] 1.4 Kleines Tkinter-Fenster erstellen.
- [x] Einige sinnvolle Spalten aus einer Datenbanktabelle auswählen.
- [x] Daten aus der Datenbank laden.
- [x] Daten tabellarisch im Tkinter-Fenster anzeigen.
- [x] Fenster starten und Anzeige prüfen.

- [x] 1.5 Programm für CSV-zu-XML erstellen.
- [x] CSV-Datei einlesen.
- [x] Für jede CSV-Zeile ein XML-Element erstellen.
- [x] XML-Datei speichern.
- [x] XML-Datei öffnen und Struktur prüfen.

- [x] 1.6 Kleine Erweiterung planen.
- [x] Sinnvolle Zusatzfunktion erstellen, z. B. XML-Anzeige, Suche, Filter oder Export.
- [x] Zweck der Erweiterung kurz dokumentieren.
- [x] Code der Erweiterung kommentieren.
- [x] Erweiterung testen.

- [x] 1.7 Projektdokumentation erstellen (`1.7_Projektdokumentation.md`).
- [x] Zeitaufwand für jeden Meilenstein tabellarisch notieren (ca. 16 Std. gesamt).
- [x] Probleme und Lösungen kurz aufschreiben (QR-Code-Format, Combobox-Problem).
- [ ] Screenshots wichtiger Ergebnisse einfügen (Platzhalter gesetzt, Bilder noch einfügen).
- [ ] Dokumentation als PDF vorbereiten.

## Phase 3: Hauptprogramm (Tkinter GUI und Integrationsaufgaben 2.1 bis 2.3)

- [x] Hauptprogramm auf Basis des Codegerüsts `21_dropdown` erstellen (`21_dropdown-vorlage.py`).
- [x] Nur die vorgegebenen Bibliotheken für Aufgabe 2.1 und 2.2 nutzen (`tkinter`, `ttk`, `messagebox`).
- [x] Vorhandene Einzelprogramme vorbereiten: Print-SQL, DB-in-CSV, DB-Ausgabefenster, CSV-to-XML.

- [x] 2.1 Methode `create_dropdown_login` ergänzen.
- [x] Dropdown-Menü mit diesen Abteilungen erstellen: `Lager`, `Verwaltung`, `Marketing`, `Geschäftsführung`.
- [x] Passwortfeld erstellen.
- [x] Passwort mit Enter bestätigen lassen.
- [x] Prüfen: Passwort ist gleich dem Abteilungsnamen.
- [x] Bei falschem Passwort eine Fehlermeldung anzeigen.
- [x] Bei richtigem Passwort die passenden Tools laden (`lade_tools()` als Platzhalter; Inhalt folgt in 2.2).

- [x] 2.2 Methode `verfügbare_tools(abteilung)` erweitern.
- [x] Berechtigungen im Programmcode speichern, nicht in der Datenbank (`BERECHTIGUNGEN`).
- [x] Für `Lager` diese Tools freigeben: `02_print_SQL_Ausgabe.py`, `04_DBausgabeFenster.py`.
- [x] Für `Verwaltung` diese Tools freigeben: `02_print_SQL_Ausgabe.py`, `03_DBinCSV.py`, `04_DBausgabeFenster.py`.
- [x] Für `Marketing` diese Tools freigeben: `02_print_SQL_Ausgabe.py`, `04_DBausgabeFenster.py`, `05_csv_to_xml.py`.
- [x] Für `Geschäftsführung` alle Tools freigeben (inkl. `06_Suche.py`).
- [x] Methode `create_dropdown_tools(parent, abteilung)` erstellen.
- [x] Im Tool-Dropdown nur erlaubte Tools anzeigen.
- [x] Button „Tool starten“ erstellen (`subprocess.Popen` mit `python3`).
- [x] Jedes Tool aus dem Hauptprogramm testen (alle 6 Tools erfolgreich gestartet und geprüft).

- [x] 2.3 Eigene sinnvolle Funktion planen: QR-Code Generator für Mitarbeiterdaten.
- [x] Neue Datei für die eigene Funktion erstellen (`07_QRCode_Generator.py`).
- [x] Neue Bibliotheken installieren und dokumentieren (`qrcode[pil]`, `pillow`).
- [x] Funktion ungefähr im Umfang von 2.1 oder 2.2 programmieren.
- [x] Funktion in das Hauptprogramm einbauen (`07_QRCode_Generator.py` in `BERECHTIGUNGEN` → Geschäftsführung).
- [ ] Funktion mit Screenshots dokumentieren.
- [x] Sinn und Zweck der Funktion kurz erklären: QR-Code mit Mitarbeiterinfos (Name, Abteilung) aus der DB generieren und im Fenster anzeigen.

- [x] Gesamtes Hauptprogramm lokal testen.
- [ ] Gesamtes Hauptprogramm mit Server-Datenbank testen.
- [x] Prüfen, ob Daten gelesen, verändert oder ergänzt werden können.
- [x] Prüfen, ob Ausgabe als `print`, GUI, CSV und XML funktioniert.
- [x] Programmcode sauber kommentieren (alle Dateien mit deutschen `#`-Kommentaren).
- [ ] PDF-Dokumentation final prüfen.
- [ ] Programmcode und PDF-Dokumentation für die Abgabe vorbereiten.

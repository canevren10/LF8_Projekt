# LF8-Projekt – Heiner IT Datenbankprogramm

**Schüler:** Can, Max, Hamza  
**Fach:** LF8 – Daten systemübergreifend bereitstellen  
**Datenbank:** `heiner_it` (MariaDB, lokal)

---

## Projektübersicht

Dieses Projekt verbindet eine MariaDB-Datenbank mit einer Python-Tkinter-Oberfläche.  
Nach einem abteilungsbasierten Login stehen je nach Berechtigung verschiedene Tools zur Verfügung.

---

## Voraussetzungen

| Software | Mac | Windows |
|----------|-----|---------|
| Python 3 | vorinstalliert | [python.org](https://www.python.org/downloads/) herunterladen, bei Installation „Add to PATH" aktivieren |
| MariaDB | `brew install mariadb` | [mariadb.org](https://mariadb.org/download/) → MSI-Installer |
| pip-Pakete | siehe unten | siehe unten |

---

## Bibliotheken installieren

### Mac

```bash
cd pfad/zum/LF8_Projekt
python3 -m venv .venv
source .venv/bin/activate
pip install mariadb 'qrcode[pil]' pillow
```

### Windows

```cmd
cd pfad\zum\LF8_Projekt
python -m venv .venv
.venv\Scripts\activate
pip install mariadb "qrcode[pil]" pillow
```

> **Hinweis Windows:** Das `mariadb`-Paket benötigt den installierten MariaDB-Connector.  
> Download: [mariadb.com/downloads/connectors](https://mariadb.com/downloads/connectors/)

---

## Datenbank einrichten

### Mac

```bash
brew services start mariadb
mariadb -u root -p
```

### Windows

```cmd
net start MariaDB
mysql -u root -p
```

Im MariaDB-Terminal (beide Systeme):

```sql
CREATE DATABASE heiner_it;
EXIT;
```

SQL-Datei importieren:

**Mac:**
```bash
mariadb -u root -p heiner_it < heiner_it_2025_26.sql
```

**Windows:**
```cmd
mysql -u root -p heiner_it < heiner_it_2025_26.sql
```

**Zugangsdaten:**

| Feld | Wert |
|------|------|
| Host | `localhost` |
| Benutzer | `root` |
| Passwort | `123` |
| Datenbank | `heiner_it` |

---

## Hauptprogramm starten

### Mac

```bash
cd pfad/zum/LF8_Projekt
source .venv/bin/activate
python3 21_dropdown-vorlage.py
```

### Windows

```cmd
cd pfad\zum\LF8_Projekt
.venv\Scripts\activate
python 21_dropdown-vorlage.py
```

---

## Login

Das **Passwort ist immer gleich dem Abteilungsnamen** (Groß-/Kleinschreibung beachten):

| Abteilung | Passwort |
|-----------|----------|
| Lager | `Lager` |
| Verwaltung | `Verwaltung` |
| Marketing | `Marketing` |
| Geschäftsführung | `Geschäftsführung` |

---

## Berechtigungen (Tools je Abteilung)

| Abteilung | Erlaubte Tools |
|-----------|---------------|
| Lager | SQL-Ausgabe, DB-Fenster |
| Verwaltung | SQL-Ausgabe, CSV-Export, DB-Fenster |
| Marketing | SQL-Ausgabe, DB-Fenster, XML-Export |
| Geschäftsführung | **Alle Tools** (inkl. Suche + QR-Code) |

---

## Projektdateien

| Datei | Meilenstein | Beschreibung |
|-------|-------------|--------------|
| `01_ConnectionTest.py` | 1.1 | Datenbankverbindung testen |
| `02_print_SQL_Ausgabe.py` | 1.2 | Mitarbeiterliste in der Konsole ausgeben |
| `03_DBinCSV.py` | 1.3 | Lagerbestand als `lagerbestand.csv` exportieren |
| `04_DBausgabeFenster.py` | 1.4 | Artikel tabellarisch im Tkinter-Fenster anzeigen |
| `05_csv_to_xml.py` | 1.5 | CSV-Datei in `lagerbestand.xml` umwandeln |
| `06_Suche.py` | 1.6 | Mitarbeitersuche mit Filter (Vorname/Nachname) |
| `07_QRCode_Generator.py` | 2.3 | QR-Code für Mitarbeiter aus der DB generieren |
| `21_dropdown-vorlage.py` | 2.1/2.2 | **Hauptprogramm**: Login + Tool-Auswahl |
| `lagerbestand.csv` | – | Exportierte Artikeldaten (wird durch 1.3 erzeugt) |
| `lagerbestand.xml` | – | XML-Export (wird durch 1.5 erzeugt) |

---

## Einzelne Meilensteine testen

Jede Datei kann auch **direkt** gestartet werden.

**Mac** (`python3`) / **Windows** (`python`):

```bash
python3 01_ConnectionTest.py       # Verbindungstest → Ausgabe in Konsole
python3 02_print_SQL_Ausgabe.py    # Mitarbeiterliste → Ausgabe in Konsole
python3 03_DBinCSV.py              # → lagerbestand.csv wird erstellt
python3 04_DBausgabeFenster.py     # → Tkinter-Fenster mit Artikeltabelle
python3 05_csv_to_xml.py           # → lagerbestand.xml wird erstellt
python3 06_Suche.py                # → Suchfenster für Mitarbeiter
python3 07_QRCode_Generator.py     # → QR-Code-Fenster
python3 21_dropdown-vorlage.py     # → Hauptprogramm (Login + alle Tools)
```

> Unter Windows `python` statt `python3` verwenden.

---

## QR-Code Generator (Meilenstein 2.3)

- Lädt alle Mitarbeiter aus der Tabelle `personal`
- Suchfeld filtert nach Vor- oder Nachname
- Klick auf **QR-Code generieren** (oder Doppelklick) zeigt den QR-Code im Fenster
- QR-Inhalt: `Heiner IT`, `Name: Nachname Vorname`, `Abteilung`
- Mit Handy-Kamera scannbar

---

## Verwendete Bibliotheken

| Bibliothek | Zweck |
|------------|-------|
| `mariadb` | Datenbankverbindung zu MariaDB |
| `tkinter` | GUI (Fenster, Buttons, Tabellen) |
| `csv` | CSV-Dateien lesen und schreiben |
| `xml.etree.ElementTree` | XML-Dateien erstellen |
| `subprocess` | Tools im Hintergrund starten |
| `qrcode` | QR-Code aus Text erzeugen |
| `Pillow (PIL)` | QR-Bild im Tkinter-Fenster anzeigen |

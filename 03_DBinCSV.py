# ==============================================================================
# Meilenstein 1.3 – Datenbanktabelle 'artikel' als CSV-Datei exportieren
# Zweck: Alle Artikeldaten werden aus der DB gelesen und in lagerbestand.csv
#        gespeichert. Trennzeichen: Semikolon (;) – kompatibel mit Excel (DE).
# ==============================================================================

import csv      # csv: Standardbibliothek zum Lesen und Schreiben von CSV-Dateien
import mariadb  # mariadb: Treiber für den Datenbankzugriff
import sys      # sys: Programmabbruch bei kritischen Fehlern

# Zieldatei für den Export
CSV_DATEI = "lagerbestand.csv"

# SQL: alle Spalten der Artikel-Tabelle, sortiert nach Artikelnummer
SQL = "SELECT * FROM artikel ORDER BY ArtikelNr;"


if __name__ == "__main__":
    # Schritt 1: Datenbankverbindung herstellen
    try:
        db = mariadb.connect(
            host="localhost",
            user="root",
            password="123",
            database="heiner_it"
        )
    except mariadb.Error as e:
        print(f"Datenbankverbindung fehlgeschlagen: {e}")
        sys.exit(1)  # Exit-Code 1 = Fehler

    try:
        # Schritt 2: SQL-Abfrage ausführen
        cur = db.cursor()   # Cursor zum Ausführen der SQL-Anweisung
        cur.execute(SQL)    # Alle Artikel aus der Datenbank abrufen

        # Schritt 3: CSV-Datei schreiben
        with open(CSV_DATEI, "w", newline="", encoding="utf-8") as f:
            # newline="" verhindert doppelte Zeilenumbrüche unter Windows
            w = csv.writer(f, delimiter=";")              # Semikolon als Trennzeichen
            w.writerow([d[0] for d in cur.description])   # Kopfzeile: Spaltennamen aus der DB
            w.writerows(cur)                              # Alle Datenzeilen auf einmal schreiben

    except (mariadb.Error, OSError) as e:
        # OSError fängt Dateifehler ab (z. B. fehlende Schreibrechte)
        print(f"Export fehlgeschlagen: {e}")
        sys.exit(1)
    finally:
        # Schritt 4: Verbindung immer freigeben – auch im Fehlerfall
        db.close()

    print(f"CSV-Datei erfolgreich erstellt: {CSV_DATEI}")

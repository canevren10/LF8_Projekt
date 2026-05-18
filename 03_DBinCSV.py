# Meilenstein 1.3: Tabelle artikel als CSV-Datei lagerbestand.csv exportieren

import csv
import mariadb
import sys

# Schritt 1: Verbindung zur Datenbank herstellen (wie in 02_print_SQL_Ausgabe.py)
try:
  db = mariadb.connect(
    host="localhost",
    user="root",
    password="123",
    database="heiner_it"
  )
except mariadb.Error as e:
  print(f"Datenbankverbindung fehlgeschlagen: {e}")
  sys.exit(1)

try:
  # Schritt 2: SQL ausführen – alle Zeilen aus artikel (Lager-/Artikeldaten)
  cur = db.cursor()
  cur.execute("SELECT * FROM artikel ORDER BY ArtikelNr;")

  # Schritt 3: CSV schreiben – zuerst Spaltennamen, dann alle Datensätze
  with open("lagerbestand.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow([d[0] for d in cur.description])
    w.writerows(cur)
except (mariadb.Error, OSError) as e:
  print(f"Export fehlgeschlagen: {e}")
  sys.exit(1)
finally:
  # Schritt 4: Verbindung wieder freigeben
  db.close()

print("CSV Datei erfolgreich erstellt")

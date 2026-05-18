# Meilenstein 1.2: SQL-Abfrage ausführen und Ergebnis in der Konsole ausgeben

import mariadb
import sys

# Verbindung zur Datenbank (gleiche Zugangsdaten wie in 01_ConnectionTest.py)
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

# SQL-Anweisung: alle Datensätze der Mitarbeitertabelle personal
SQL = "SELECT * FROM personal ORDER BY PersonalNr;"


def testprint(dbc, sql):
  # Führt die Abfrage aus und gibt jede Ergebniszeile mit print() aus
  try:
    cur = dbc.cursor()
    cur.execute(sql)
    for row in cur:
      print(row)
  except mariadb.Error as e:
    print(f"SQL-Abfrage fehlgeschlagen: {e}")


# Abfrage starten; Verbindung danach immer schließen
try:
  testprint(db, SQL)
finally:
  db.close()

##### Verbindung zur Datenbank herstellen #####

import mariadb
import sys

# Connect to the MySQL database 
# - definiere hier die Verbindung zur Datenbank
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

# Die Methode pürft ob eine erfolgreiche Vebrindung zur Datenbank hergesetellt werden kann.
# Ausgabe: gibt succesfull oder fail als print-Ausgabe zurück
def testConnection(dbc):      #dbc steht für die Datenbankverbindung die überprüft werden soll
  # definieren sie hier die Tests und Ausgaben
  if dbc.open:
    print("Datenbankverbindung erfolgreich")
  else:
    print("Datenbankverbindung fehlgeschlagen")
# Aufruf der Methode zum Testen der Datenbankverbindung
testConnection(db)    

##### Verbindung zur Datenbank herstellen #####

import mariadb
import sys

# Connect to the MySQL database 
# - definiere hier die Verbindung zur Datenbank
try:
  db = mariadb.connect(
    host="10.145.240.122", #10.145.240.122 #local:localhost
    user="root", #root #local:root
    password="Gr3eu1H8GRyZIS", #Gr3eu1H8GRyZIS #local:123
    database="heiner_it" #heiner_it #local:heiner_it
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

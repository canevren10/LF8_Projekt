# ==============================================================================
# Meilenstein 1.2 – SQL-Abfrage ausführen und Ergebnis in der Konsole ausgeben
# Zweck: Alle Datensätze der Tabelle 'personal' werden per SQL abgerufen
#        und zeilenweise in der Konsole ausgegeben.
# ==============================================================================

import mariadb  # mariadb: Treiber für MariaDB/MySQL-Datenbankzugriff
import sys      # sys: Programmabbruch mit sys.exit() bei Verbindungsfehler

# SQL-Abfrage: alle Spalten (*) aus personal, sortiert nach PersonalNr
SQL = "SELECT * FROM personal ORDER BY PersonalNr;"


def sql_ausgabe(dbc, sql):
    """
    Führt eine SQL-Abfrage aus und gibt jede Ergebniszeile in der Konsole aus.

    Parameter:
        dbc – aktive mariadb.Connection
        sql – SQL-String der auszuführenden Abfrage
    """
    try:
        cur = dbc.cursor()  # Cursor: Hilfsobjekt zum Ausführen von SQL-Befehlen
        cur.execute(sql)    # SQL-Anweisung an die Datenbank senden
        for row in cur:     # Jede Zeile des Ergebnisses wird durchlaufen
            print(row)      # Zeile als Python-Tupel ausgeben
    except mariadb.Error as e:
        print(f"SQL-Abfrage fehlgeschlagen: {e}")


if __name__ == "__main__":
    # Verbindung zur lokalen Entwicklungsdatenbank herstellen
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

    # Abfrage starten; Verbindung im finally-Block immer schließen
    try:
        sql_ausgabe(db, SQL)
    finally:
        db.close()  # Verhindert offen gebliebene Verbindungen (Connection Leak)

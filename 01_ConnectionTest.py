# ==============================================================================
# Meilenstein 1.1 – Verbindungstest zur MariaDB-Datenbank
# Zweck: Prüft, ob Python eine Verbindung zur Datenbank aufbauen kann.
# ==============================================================================

import mariadb  # mariadb: Treiber für Verbindung zu MariaDB/MySQL-Datenbanken
import sys      # sys: Systemfunktionen – hier für sys.exit() bei Fehler


def test_verbindung(dbc):
    """
    Prüft den Status einer bestehenden Datenbankverbindung.

    Parameter:
        dbc – mariadb.Connection-Objekt (die zu prüfende Verbindung)
    Ausgabe:
        Gibt 'erfolgreich' oder 'fehlgeschlagen' als Konsolentext aus.
    """
    if dbc.open:  # .open ist True, wenn die Verbindung aktiv ist
        print("Datenbankverbindung erfolgreich")
    else:
        print("Datenbankverbindung fehlgeschlagen")


if __name__ == "__main__":
    # Verbindungsparameter zur Schuldatenbank
    try:
        db = mariadb.connect(
            host="10.145.240.122",      # IP-Adresse des Schulservers
            user="root",                # Datenbankbenutzer
            password="Gr3eu1H8GRyZIS",  # Kennwort (nur für Schulprojekt)
            database="heiner_it"        # Name der Datenbank
        )
    except mariadb.Error as e:
        # Verbindung fehlgeschlagen – Fehlermeldung ausgeben und Programm beenden
        print(f"Datenbankverbindung fehlgeschlagen: {e}")
        sys.exit(1)  # Exit-Code 1 = Fehler

    # Verbindungsstatus prüfen und ausgeben
    test_verbindung(db)
    db.close()  # Verbindung nach dem Test immer freigeben

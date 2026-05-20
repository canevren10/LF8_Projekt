# ==============================================================================
# Meilenstein 1.4 – Datenbankdaten tabellarisch in einem Tkinter-Fenster anzeigen
# Zweck: Artikel aus der DB werden in einer scrollbaren Tabelle (Treeview)
#        in einem GUI-Fenster dargestellt.
# Bibliotheken:
#   mariadb    – Datenbankzugriff
#   tkinter    – Standard-GUI-Bibliothek von Python
#   ttk        – Moderne Widgets (Treeview, Scrollbar, Frame)
#   messagebox – Fehlermeldungsfenster als Dialog
# ==============================================================================

import mariadb
import tkinter as tk
from tkinter import ttk, messagebox

# SQL: ausgewählte Spalten der Artikel-Tabelle, sortiert nach Artikelnummer
SQL_ARTIKEL = (
    "SELECT ArtikelNr, Artikelname, Lagerbestand, Einzelpreis, Liefereinheit "
    "FROM artikel ORDER BY ArtikelNr"
)


def daten_laden():
    """
    Stellt eine Datenbankverbindung her, führt die SQL-Abfrage aus
    und gibt Spaltennamen sowie alle Datensätze zurück.

    Rückgabe:
        spalten – Liste der Spaltennamen (aus cur.description)
        zeilen  – Liste aller Datensätze als Tupel
    """
    db = mariadb.connect(
        host="localhost",
        user="root",
        password="123",
        database="heiner_it"
    )
    try:
        cur = db.cursor()               # Cursor für die SQL-Ausführung
        cur.execute(SQL_ARTIKEL)        # Abfrage an die DB senden
        spalten = [d[0] for d in cur.description]  # Spaltennamen aus dem Ergebnis-Header
        return spalten, cur.fetchall()  # Alle Zeilen auf einmal abrufen
    finally:
        db.close()  # Verbindung immer freigeben


def darstellung_tabelle():
    """Erstellt das Hauptfenster und zeigt die Datenbankdaten als Tabelle an."""
    # Schritt 1: Tkinter-Hauptfenster anlegen
    root = tk.Tk()
    root.title("Meilenstein 1.4 – Lager (Artikel, Auszug)")

    # Schritt 2: Datenbankabfrage ausführen; Fehler als Dialogfenster anzeigen
    try:
        spalten, zeilen = daten_laden()
    except mariadb.Error as e:
        messagebox.showerror("Datenbankfehler", str(e), parent=root)
        root.destroy()  # Fenster schließen, da keine Daten vorliegen
        return

    # Schritt 3: Layout-Frame mit Treeview (Tabelle) und vertikaler Scrollbar
    frm = ttk.Frame(root, padding=8)
    frm.pack(fill=tk.BOTH, expand=True)

    # Treeview: zeigt Daten in Spalten an (show="headings" = keine Baumstruktur)
    tree = ttk.Treeview(frm, columns=spalten, show="headings", height=20)
    for s in spalten:
        tree.heading(s, text=s)              # Spaltenüberschrift setzen
        tree.column(s, width=130, minwidth=70)  # Spaltenbreite festlegen

    # Scrollbar: verknüpft mit der vertikalen Treeview-Ansicht
    sy = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=sy.set)

    # Grid-Layout: Treeview links (dehnbar), Scrollbar rechts (fest)
    tree.grid(row=0, column=0, sticky="nsew")
    sy.grid(row=0, column=1, sticky="ns")
    frm.rowconfigure(0, weight=1)     # Zeile 0 dehnt sich vertikal beim Vergrößern
    frm.columnconfigure(0, weight=1)  # Spalte 0 dehnt sich horizontal beim Vergrößern

    # Schritt 4: Datenbankzeilen in den Treeview einfügen
    for z in zeilen:
        # None-Werte durch leere Strings ersetzen; Decimal-Typen in str umwandeln
        werte = tuple("" if v is None else str(v) for v in z)
        tree.insert("", tk.END, values=werte)  # tk.END = ans Ende der Liste anhängen

    # Schritt 5: Ereignisschleife starten – Fenster bleibt bis zum Schließen offen
    root.mainloop()


if __name__ == "__main__":
    darstellung_tabelle()

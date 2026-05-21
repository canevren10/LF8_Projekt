# ==============================================================================
# Meilenstein 1.6 – Erweiterung: Mitarbeitersuche mit GUI
# Zweck: Zusätzlich zur reinen Anzeige (Meilenstein 1.4) können Mitarbeiter
#        aus der Tabelle 'personal' gezielt per Nachname oder Vorname gesucht
#        werden. Ein leeres Suchfeld zeigt die vollständige Liste.
# Sicherheit: Platzhalter (%s) in der SQL-Abfrage verhindern SQL-Injection.
# Bibliotheken:
#   mariadb    – Datenbankzugriff
#   tkinter    – GUI-Fenster und Widgets
#   ttk        – Moderne Tkinter-Widgets (Treeview, Entry, Button)
#   messagebox – Dialogfenster für Fehlermeldungen
# ==============================================================================

import mariadb
import tkinter as tk
from tkinter import ttk, messagebox


def personal_laden(suchtext):
    """
    Lädt Mitarbeiterdaten aus der Tabelle 'personal'.

    Parameter:
        suchtext – Suchbegriff (leer = alle Datensätze)
    Rückgabe:
        spalten – Liste der Spaltennamen
        zeilen  – Liste der Ergebniszeilen als Tupel
    """
    db = mariadb.connect(
        host="10.145.240.122",
        user="root",
        password="Gr3eu1H8GRyZIS",
        database="heiner_it",
    )
    try:
        cur = db.cursor()
        t = suchtext.strip()  # Leerzeichen am Rand entfernen

        if not t:
            # Kein Suchbegriff: alle Datensätze, sortiert nach PersonalNr
            cur.execute("SELECT * FROM personal ORDER BY PersonalNr")
        else:
            # Suchbegriff: LIKE prüft auf Teiltreffer in Nachname oder Vorname
            # %s als Platzhalter → parametrisierte Abfrage verhindert SQL-Injection
            muster = f"%{t}%"  # % = beliebiger Text vor/nach dem Suchbegriff
            cur.execute(
                "SELECT * FROM personal "
                "WHERE Nachname LIKE %s OR Vorname LIKE %s "
                "ORDER BY PersonalNr",
                (muster, muster),
            )

        spalten = [d[0] for d in cur.description]  # Spaltennamen aus dem Ergebnis-Header
        return spalten, cur.fetchall()              # Alle Ergebniszeilen abrufen
    finally:
        db.close()  # Verbindung immer freigeben


def mitarbeiter_suche_fenster():
    """Erstellt das Such-Fenster und verwaltet die Benutzerinteraktion."""
    root = tk.Tk()
    root.title("Mitarbeitersuche (personal)")

    # --- Suchleiste: Label + Eingabefeld + Suchen-Button ---
    kopf = ttk.Frame(root, padding=8)
    kopf.pack(fill=tk.X)
    ttk.Label(kopf, text="Mitarbeiter suchen:").pack(side=tk.LEFT, padx=(0, 8))
    eingabe = ttk.Entry(kopf, width=32)  # Texteingabe für den Suchbegriff
    eingabe.pack(side=tk.LEFT, padx=(0, 8))

    # --- Bereich für die Ergebnistabelle ---
    frm = ttk.Frame(root, padding=8)
    frm.pack(fill=tk.BOTH, expand=True)

    tree = None  # Treeview wird erst beim ersten Laden erzeugt (lazy init)

    def tabelle_fuellen(zeilen):
        """Löscht alte Treeview-Einträge und fügt neue Zeilen ein."""
        for k in tree.get_children():
            tree.delete(k)  # Alle vorhandenen Einträge entfernen
        for z in zeilen:
            werte = tuple("" if v is None else str(v) for v in z)  # None → ""
            tree.insert("", tk.END, values=werte)

    def suchen(_event=None):
        """Datenbankabfrage starten und Tabelle aktualisieren."""
        nonlocal tree  # Zugriff auf tree aus dem äußeren Scope
        try:
            spalten, zeilen = personal_laden(eingabe.get())
        except mariadb.Error as e:
            messagebox.showerror("Datenbankfehler", str(e), parent=root)
            return

        if tree is None:
            # Treeview und Scrollbar beim ersten Aufruf einmalig erstellen
            tree = ttk.Treeview(frm, columns=spalten, show="headings", height=18)
            for s in spalten:
                tree.heading(s, text=s)
                tree.column(s, width=110, minwidth=60)
            sy = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=sy.set)
            tree.grid(row=0, column=0, sticky="nsew")
            sy.grid(row=0, column=1, sticky="ns")
            frm.rowconfigure(0, weight=1)     # Treeview dehnt sich beim Vergrößern
            frm.columnconfigure(0, weight=1)

        tabelle_fuellen(zeilen)  # Ergebnisse in die Tabelle eintragen

    ttk.Button(kopf, text="Suchen", command=suchen).pack(side=tk.LEFT)
    eingabe.bind("<Return>", suchen)  # Enter-Taste löst die Suche aus

    suchen()  # Beim Start direkt alle Mitarbeiter laden

    root.mainloop()


if __name__ == "__main__":
    mitarbeiter_suche_fenster()

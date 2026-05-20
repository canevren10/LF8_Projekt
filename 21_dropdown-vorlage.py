# ==============================================================================
# Meilenstein 2.1 / 2.2 – Hauptprogramm: Login und abteilungsbasierte Tool-Auswahl
# Zweck: Benutzer wählen ihre Abteilung, geben das Passwort ein und erhalten
#        danach nur die für ihre Abteilung freigegebenen Python-Tools zur Auswahl.
#        Das gewählte Tool wird als separater Prozess gestartet.
# Bibliotheken:
#   os         – Dateipfade ermitteln (__file__, path.join)
#   subprocess – Untergeordnete Python-Prozesse im Hintergrund starten
#   tkinter    – GUI-Fenster und Widgets
#   ttk        – Moderne Tkinter-Widgets (Combobox, Frame, Button)
#   messagebox – Login-Fehlermeldung als Dialog
# ==============================================================================

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Absoluter Pfad zum Projektordner (hier liegen alle Skripte)
SKRIPT_ORDNER = os.path.dirname(os.path.abspath(__file__))

# Alle verfügbaren Abteilungen; das Passwort entspricht dem Abteilungsnamen
ABTEILUNGEN = ("Lager", "Verwaltung", "Marketing", "Geschäftsführung")

# Zuordnung: Abteilung → erlaubte Tools (Dateinamen im SKRIPT_ORDNER)
# Geschäftsführung hat Zugriff auf alle Tools
BERECHTIGUNGEN = {
    "Lager": [
        "02_print_SQL_Ausgabe.py",
        "04_DBausgabeFenster.py",
    ],
    "Verwaltung": [
        "02_print_SQL_Ausgabe.py",
        "03_DBinCSV.py",
        "04_DBausgabeFenster.py",
    ],
    "Marketing": [
        "02_print_SQL_Ausgabe.py",
        "04_DBausgabeFenster.py",
        "05_csv_to_xml.py",
    ],
    "Geschäftsführung": [
        "02_print_SQL_Ausgabe.py",
        "03_DBinCSV.py",
        "04_DBausgabeFenster.py",
        "05_csv_to_xml.py",
        "06_Suche.py",
        "07_QRCode_Generator.py",
    ],
}


def verfügbare_tools(abteilung):
    """Gibt die erlaubten Tools einer Abteilung zurück (leere Liste bei unbekannter Abteilung)."""
    return BERECHTIGUNGEN.get(abteilung, [])


def create_dropdown_tools(parent, abteilung):
    """
    Erstellt den Tool-Auswahl-Bereich nach erfolgreichem Login.

    Parameter:
        parent    – Tkinter-Widget, in dem die Auswahl eingefügt wird
        abteilung – Name der eingeloggten Abteilung
    """
    tools = verfügbare_tools(abteilung)  # Nur für diese Abteilung erlaubte Tools laden

    rahmen = ttk.Frame(parent, padding=10)
    rahmen.pack(fill=tk.X)

    tool_var = tk.StringVar(value=tools[0])  # Standardauswahl: erstes Tool
    ttk.Label(rahmen, text=f"Tools ({abteilung}):").pack(anchor=tk.W)

    # Combobox: Dropdown-Liste mit erlaubten Tools; nur lesbar (state="readonly")
    ttk.Combobox(rahmen, textvariable=tool_var, values=tools, state="readonly").pack(
        fill=tk.X, pady=(0, 8)
    )

    def tool_starten():
        """Gewähltes Skript als eigenen Python-Prozess starten."""
        pfad = os.path.join(SKRIPT_ORDNER, tool_var.get())  # Vollständiger Dateipfad
        subprocess.Popen(["python3", pfad])  # Popen: startet Hintergrundprozess; Hauptfenster bleibt offen

    ttk.Button(rahmen, text="Tool starten", command=tool_starten).pack()


def create_dropdown_login(parent):
    """
    Erstellt den Login-Bereich: Abteilung auswählen und Passwort eingeben.

    Parameter:
        parent – Tkinter-Wurzelfenster
    """
    rahmen = ttk.Frame(parent, padding=10)
    rahmen.pack(fill=tk.X)

    # Abteilungs-Dropdown
    abteilung = tk.StringVar(value=ABTEILUNGEN[0])  # Standardauswahl: erste Abteilung
    ttk.Label(rahmen, text="Abteilung:").pack(anchor=tk.W)
    ttk.Combobox(
        rahmen, textvariable=abteilung, values=ABTEILUNGEN, state="readonly"
    ).pack(fill=tk.X, pady=(0, 8))

    # Passwort-Eingabe (Eingabe wird als * maskiert)
    ttk.Label(rahmen, text="Passwort:").pack(anchor=tk.W)
    pw = tk.Entry(rahmen, show="*")
    pw.pack(fill=tk.X, pady=(0, 8))
    pw.focus()  # Cursor direkt ins Passwortfeld setzen

    def pruefe_login(_event=None):
        """Login-Prüfung: Passwort muss dem Abteilungsnamen entsprechen."""
        if pw.get() != abteilung.get():
            messagebox.showerror("Login fehlgeschlagen", "Falsches Passwort.")
            return
        # Login erfolgreich: Login-Bereich entfernen, Tool-Auswahl einblenden
        rahmen.destroy()
        create_dropdown_tools(parent, abteilung.get())

    ttk.Button(rahmen, text="Login", command=pruefe_login).pack()
    pw.bind("<Return>", pruefe_login)  # Enter-Taste löst Login-Prüfung aus


if __name__ == "__main__":
    root = tk.Tk()
    root.title("LF8 – Hauptprogramm")
    create_dropdown_login(root)
    root.mainloop()

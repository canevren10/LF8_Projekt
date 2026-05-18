# Meilenstein 2.1/2.2: Login und Tool-Auswahl nach Abteilung
# tkinter = GUI (Fenster, Felder, Buttons) | subprocess = Skripte im Hintergrund starten

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Ordner dieser Datei – Tool-Skripte liegen im gleichen Projektordner
SKRIPT_ORDNER = os.path.dirname(os.path.abspath(__file__))

# Alle Abteilungen; Passwort = exakt dieser Name
ABTEILUNGEN = ("Lager", "Verwaltung", "Marketing", "Geschäftsführung")

# Welche Python-Datei welche Abteilung nutzen darf (fest im Code, nicht in der DB)
BERECHTIGUNGEN = {
  "Lager": ["02_print_SQL_Ausgabe.py", "04_DBausgabeFenster.py"],
  "Verwaltung": ["02_print_SQL_Ausgabe.py", "03_DBinCSV.py", "04_DBausgabeFenster.py"],
  "Marketing": ["02_print_SQL_Ausgabe.py", "04_DBausgabeFenster.py", "05_csv_to_xml.py"],
  "Geschäftsführung": [
    "02_print_SQL_Ausgabe.py", "03_DBinCSV.py", "04_DBausgabeFenster.py",
    "05_csv_to_xml.py", "06_Suche.py", "07_QRCode_Generator.py",
  ],
}


def verfügbare_tools(abteilung):
  return BERECHTIGUNGEN.get(abteilung, [])


def create_dropdown_tools(parent, abteilung):
  # Nach Login: nur erlaubte Tools der Abteilung anzeigen
  tools = verfügbare_tools(abteilung)
  rahmen = ttk.Frame(parent, padding=10)
  rahmen.pack(fill=tk.X)

  tool_var = tk.StringVar(value=tools[0])
  ttk.Label(rahmen, text=f"Tools ({abteilung}):").pack(anchor=tk.W)
  ttk.Combobox(rahmen, textvariable=tool_var, values=tools, state="readonly").pack(
    fill=tk.X, pady=(0, 8)
  )

  def tool_starten():
    # Gewähltes Skript mit python3 starten – Hauptfenster bleibt offen
    pfad = os.path.join(SKRIPT_ORDNER, tool_var.get())
    subprocess.Popen(["python3", pfad])

  ttk.Button(rahmen, text="Tool starten", command=tool_starten).pack()


def lade_tools(parent, abteilung):
  # Wird nach erfolgreichem Login aufgerufen (Meilenstein 2.1 → 2.2)
  create_dropdown_tools(parent, abteilung)


def create_dropdown_login(parent):
  # Login-Bereich: Abteilung wählen, Passwort prüfen
  rahmen = ttk.Frame(parent, padding=10)
  rahmen.pack(fill=tk.X)

  abteilung = tk.StringVar(value=ABTEILUNGEN[0])
  ttk.Label(rahmen, text="Abteilung:").pack(anchor=tk.W)
  ttk.Combobox(
    rahmen, textvariable=abteilung, values=ABTEILUNGEN, state="readonly"
  ).pack(fill=tk.X, pady=(0, 8))

  ttk.Label(rahmen, text="Passwort:").pack(anchor=tk.W)
  pw = tk.Entry(rahmen, show="*")  # Eingabe als *
  pw.pack(fill=tk.X, pady=(0, 8))
  pw.focus()

  def pruefe_login(_event=None):
    if pw.get() != abteilung.get():
      messagebox.showerror("Login fehlgeschlagen", "Falsches Passwort.")
      return
    print("Login erfolgreich")
    rahmen.destroy()
    lade_tools(parent, abteilung.get())

  ttk.Button(rahmen, text="Login", command=pruefe_login).pack()
  pw.bind("<Return>", pruefe_login)  # Enter = Login


if __name__ == "__main__":
  root = tk.Tk()
  root.title("LF8 – Hauptprogramm")
  create_dropdown_login(root)
  root.mainloop()

# Meilenstein 1.4: Datenbankdaten tabellarisch in einem Tkinter-Fenster anzeigen

import mariadb
import tkinter as tk
from tkinter import ttk, messagebox

SQL_ARTIKEL = (
  "SELECT ArtikelNr, Artikelname, Lagerbestand, Einzelpreis, Liefereinheit "
  "FROM artikel ORDER BY ArtikelNr"
)


def read_from_database():
  # Schritt 1: Verbindung wie in 01_ConnectionTest.py, Abfrage ausführen, Verbindung schließen
  db = mariadb.connect(
    host="localhost",
    user="root",
    password="123",
    database="heiner_it"
  )
  try:
    cur = db.cursor()
    cur.execute(SQL_ARTIKEL)
    spalten = [d[0] for d in cur.description]
    return spalten, cur.fetchall()
  finally:
    db.close()


def darstellung_tabelle():
  # Schritt 2: Hauptfenster anlegen
  root = tk.Tk()
  root.title("Meilenstein 1.4 – Lager (Artikel, Auszug)")

  try:
    spalten, zeilen = read_from_database()
  except mariadb.Error as e:
    messagebox.showerror("Datenbankfehler", str(e), parent=root)
    root.destroy()
    return

  # Schritt 3: Tabelle (Treeview) mit Überschriften und Scrollbar
  frm = ttk.Frame(root, padding=8)
  frm.pack(fill=tk.BOTH, expand=True)
  tree = ttk.Treeview(frm, columns=spalten, show="headings", height=20)
  for s in spalten:
    tree.heading(s, text=s)
    tree.column(s, width=130, minwidth=70)
  sy = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=tree.yview)
  tree.configure(yscrollcommand=sy.set)
  tree.grid(row=0, column=0, sticky="nsew")
  sy.grid(row=0, column=1, sticky="ns")
  frm.rowconfigure(0, weight=1)
  frm.columnconfigure(0, weight=1)

  # Schritt 4: Zeilen einfügen (Werte als Text, damit z. B. Decimal angezeigt werden kann)
  for z in zeilen:
    werte = tuple("" if v is None else str(v) for v in z)
    tree.insert("", tk.END, values=werte)

  # Schritt 5: Fenster anzeigen (Ereignisschleife)
  root.mainloop()


darstellung_tabelle()

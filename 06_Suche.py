# Meilenstein 1.6 – Erweiterung: Mitarbeitersuche
#
# Zweck: Zusätzlich zur reinen Anzeige (Meilenstein 1.4) können Mitarbeiter
#        aus der Tabelle personal gezielt per Nachname oder Vorname gesucht
#        werden. Leeres Suchfeld zeigt wieder die vollständige Liste.
#
# Technik: Tkinter-Oberfläche wie 04_DBausgabeFenster.py; Abfrage mit LIKE
#          und Platzhaltern (%s), um SQL-Injection zu vermeiden.

import mariadb
import tkinter as tk
from tkinter import ttk, messagebox


def personal_laden(suchtext):
  """Lädt Spaltennamen und Zeilen aus personal – mit oder ohne Suchfilter."""
  # Verbindung wie in 01_ConnectionTest.py / 04_DBausgabeFenster.py
  db = mariadb.connect(
    host="localhost",
    user="root",
    password="123",
    database="heiner_it",
  )
  try:
    cur = db.cursor()
    t = suchtext.strip()

    if not t:
      # Kein Suchbegriff: alle Datensätze sortiert nach PersonalNr
      cur.execute("SELECT * FROM personal ORDER BY PersonalNr")
    else:
      # Suchbegriff: LIKE auf Nachname und Vorname (Teiltreffer möglich)
      muster = f"%{t}%"
      cur.execute(
        "SELECT * FROM personal WHERE Nachname LIKE %s OR Vorname LIKE %s ORDER BY PersonalNr",
        (muster, muster),
      )

    spalten = [d[0] for d in cur.description]
    return spalten, cur.fetchall()
  finally:
    db.close()


def mitarbeiter_suche_fenster():
  # Hauptfenster der Erweiterung
  root = tk.Tk()
  root.title("Mitarbeitersuche (personal)")

  # --- Suchleiste (Eingabe + Aktion) ---
  kopf = ttk.Frame(root, padding=8)
  kopf.pack(fill=tk.X)
  ttk.Label(kopf, text="Mitarbeiter suchen:").pack(side=tk.LEFT, padx=(0, 8))
  eingabe = ttk.Entry(kopf, width=32)
  eingabe.pack(side=tk.LEFT, padx=(0, 8))

  # --- Bereich für die Ergebnistabelle ---
  frm = ttk.Frame(root, padding=8)
  frm.pack(fill=tk.BOTH, expand=True)

  tree = None  # wird beim ersten erfolgreichen Laden angelegt

  def tabelle_fuellen(zeilen):
    # Alte Zeilen entfernen, neue aus der aktuellen Abfrage einfügen
    for k in tree.get_children():
      tree.delete(k)
    for z in zeilen:
      werte = tuple("" if v is None else str(v) for v in z)
      tree.insert("", tk.END, values=werte)

  def suchen(_event=None):
    """Sucht auslösen: Daten holen, Treeview anlegen oder nur Inhalt aktualisieren."""
    nonlocal tree
    try:
      spalten, zeilen = personal_laden(eingabe.get())
    except mariadb.Error as e:
      messagebox.showerror("Datenbankfehler", str(e), parent=root)
      return

    if tree is None:
      # Erstes Mal: Spalten aus der Datenbank, Scrollbar, Gitterlayout
      tree = ttk.Treeview(frm, columns=spalten, show="headings", height=18)
      for s in spalten:
        tree.heading(s, text=s)
        tree.column(s, width=110, minwidth=60)
      sy = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=tree.yview)
      tree.configure(yscrollcommand=sy.set)
      tree.grid(row=0, column=0, sticky="nsew")
      sy.grid(row=0, column=1, sticky="ns")
      frm.rowconfigure(0, weight=1)
      frm.columnconfigure(0, weight=1)

    tabelle_fuellen(zeilen)

  ttk.Button(kopf, text="Suchen", command=suchen).pack(side=tk.LEFT)
  eingabe.bind("<Return>", suchen)  # Suche auch mit Enter starten

  # Beim Start: vollständige Liste ohne Filter
  suchen()

  root.mainloop()


mitarbeiter_suche_fenster()

# Meilenstein 2.3: QR-Code Generator für Mitarbeiterdaten aus der DB
# mariadb = Datenbankverbindung (wie 01_ConnectionTest.py)
# qrcode  = QR-Code aus Text erzeugen
# PIL     = QR-Bild im Tkinter-Fenster anzeigen

import mariadb
import qrcode
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

# Verbindungsdaten – identisch mit 01_ConnectionTest.py
DB_CONFIG = {"host": "localhost", "user": "root", "password": "123", "database": "heiner_it"}


def mitarbeiter_laden(suchtext=""):
  # Ohne Suchtext: alle; mit Suchtext: Treffer in Vorname oder Nachname (LIKE)
  db = mariadb.connect(**DB_CONFIG)
  try:
    cur = db.cursor()
    if not suchtext.strip():
      cur.execute(
        "SELECT PersonalNr, Vorname, Nachname, Position FROM personal ORDER BY PersonalNr"
      )
    else:
      m = f"%{suchtext.strip()}%"
      cur.execute(
        "SELECT PersonalNr, Vorname, Nachname, Position "
        "FROM personal WHERE Nachname LIKE %s OR Vorname LIKE %s ORDER BY PersonalNr",
        (m, m),
      )
    return cur.fetchall()
  finally:
    db.close()


def qr_text(m):
  # QR-Inhalt: Firma + Name + Abteilung – kein Tupel, nur reiner Text
  return f"Heiner IT\nName: {m[2] or ''} {m[1] or ''}\nAbteilung: {m[3] or '-'}"


def qr_bild(text):
  # box_size=6 → kleinerer QR; ERROR_CORRECT_H → hohe Fehlertoleranz für Handy-Scanner
  qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=6, border=4)
  qr.add_data(text)
  qr.make(fit=True)
  return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def qr_code_fenster():
  root = tk.Tk()
  root.title("QR-Code Generator (personal)")

  rahmen = ttk.Frame(root, padding=10)
  rahmen.pack(fill=tk.BOTH, expand=True)

  # Suchzeile: Eingabefeld + Suchen-Button (Enter ebenfalls möglich)
  zeile = ttk.Frame(rahmen)
  zeile.pack(fill=tk.X, pady=(0, 8))
  ttk.Label(zeile, text="Suchen:").pack(side=tk.LEFT, padx=(0, 6))
  suchfeld = ttk.Entry(zeile, width=28)
  suchfeld.pack(side=tk.LEFT, padx=(0, 6))

  # Anzahl gefundener Mitarbeiter
  anzahl = ttk.Label(rahmen, text="")
  anzahl.pack(anchor=tk.W, pady=(0, 4))

  # Scrollbare Namensliste
  frm = ttk.Frame(rahmen)
  frm.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
  liste = tk.Listbox(frm, height=12, width=48)
  sb = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=liste.yview)
  liste.configure(yscrollcommand=sb.set)
  liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  sb.pack(side=tk.RIGHT, fill=tk.Y)

  # QR-Bild wird in diesem Label angezeigt
  qr_label = tk.Label(rahmen, bg="white")
  qr_label.pack(pady=8)
  foto = []  # Referenz halten – sonst löscht Python das Bild aus dem Speicher

  alle = []  # aktuell angezeigte Mitarbeiter-Tupel

  def liste_fuellen():
    nonlocal alle
    try:
      alle = list(mitarbeiter_laden(suchfeld.get()))
    except mariadb.Error as e:
      messagebox.showerror("Datenbankfehler", str(e), parent=root)
      return
    liste.delete(0, tk.END)
    for m in alle:
      liste.insert(tk.END, f"{m[0]}: {m[1]} {m[2]}")
    anzahl.configure(text=f"{len(alle)} Mitarbeiter")
    if alle:
      liste.selection_set(0)  # ersten Eintrag vorauswählen

  def generieren(_event=None):
    # Ausgewählten Mitarbeiter aus der Liste lesen
    sel = liste.curselection()
    if not sel:
      messagebox.showwarning("Auswahl", "Bitte einen Mitarbeiter wählen.", parent=root)
      return
    bild = qr_bild(qr_text(alle[sel[0]]))
    img = ImageTk.PhotoImage(bild)
    foto.clear()
    foto.append(img)
    qr_label.configure(image=img, width=bild.width, height=bild.height)

  ttk.Button(zeile, text="Suchen", command=liste_fuellen).pack(side=tk.LEFT)
  suchfeld.bind("<Return>", lambda _: liste_fuellen())
  ttk.Button(rahmen, text="QR-Code generieren", command=generieren).pack()
  liste.bind("<Double-Button-1>", generieren)  # Doppelklick = QR generieren

  liste_fuellen()  # Beim Start alle Mitarbeiter sofort laden
  root.mainloop()


if __name__ == "__main__":
  qr_code_fenster()

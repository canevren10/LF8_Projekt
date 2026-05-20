# ==============================================================================
# Meilenstein 2.3 – QR-Code-Generator für Mitarbeiterdaten
# Zweck: Mitarbeiterdaten aus der DB werden in einer Liste angezeigt.
#        Per Klick wird ein QR-Code für den ausgewählten Mitarbeiter generiert
#        und direkt im Fenster angezeigt.
# Bibliotheken:
#   mariadb    – Datenbankzugriff (Mitarbeiterliste laden)
#   qrcode     – QR-Code-Bild aus Text erzeugen
#   tkinter    – GUI-Fenster und Widgets
#   PIL/ImageTk – QR-Bild in Tkinter-kompatibles Format (PhotoImage) umwandeln
# ==============================================================================

import mariadb
import qrcode
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk  # ImageTk: wandelt PIL-Bilder in Tkinter-PhotoImage um

# Datenbankverbindungsdaten als Dictionary – wiederverwendbar mit **DB_CONFIG
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123",
    "database": "heiner_it"
}


def mitarbeiter_laden(suchtext=""):
    """
    Lädt Mitarbeiterdaten aus der Tabelle 'personal'.

    Parameter:
        suchtext – Suchbegriff (leer = alle Mitarbeiter)
    Rückgabe:
        Liste von Tupeln: (PersonalNr, Vorname, Nachname, Position)
    """
    db = mariadb.connect(**DB_CONFIG)  # ** entpackt das Dictionary als Schlüsselwortargumente
    try:
        cur = db.cursor()
        if not suchtext.strip():
            # Kein Suchbegriff: alle Mitarbeiter laden
            cur.execute(
                "SELECT PersonalNr, Vorname, Nachname, Position "
                "FROM personal ORDER BY PersonalNr"
            )
        else:
            # Mit Suchbegriff: LIKE-Suche in Vor- und Nachname (Teiltreffer möglich)
            m = f"%{suchtext.strip()}%"  # % = Platzhalter für beliebige Zeichen
            cur.execute(
                "SELECT PersonalNr, Vorname, Nachname, Position "
                "FROM personal WHERE Nachname LIKE %s OR Vorname LIKE %s "
                "ORDER BY PersonalNr",
                (m, m),
            )
        return cur.fetchall()  # Alle Treffer als Liste zurückgeben
    finally:
        db.close()  # Verbindung immer freigeben


def qr_text(m):
    """
    Erstellt den Textinhalt des QR-Codes für einen Mitarbeiter.

    Parameter:
        m – Tupel (PersonalNr, Vorname, Nachname, Position)
    Rückgabe:
        Mehrzeiliger String für den QR-Code-Inhalt
    """
    # Reihenfolge: Nachname (Index 2), Vorname (Index 1) – None wird zu leerem String
    return f"Heiner IT\nName: {m[2] or ''} {m[1] or ''}\nAbteilung: {m[3] or '-'}"


def qr_bild(text):
    """
    Erzeugt ein QR-Code-Bild aus einem Text.

    Parameter:
        text – Inhalt des QR-Codes
    Rückgabe:
        PIL-Image-Objekt im RGB-Format
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Hohe Fehlertoleranz (30 %)
        box_size=6,   # Pixelgröße pro QR-Modul (kleiner = kompakteres Bild)
        border=4      # Ruhige Zone um den QR-Code (4 Module – ISO-Standard)
    )
    qr.add_data(text)  # Textinhalt hinzufügen
    qr.make(fit=True)  # QR-Version automatisch wählen (kleinste passende)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def qr_code_fenster():
    """Erstellt das Hauptfenster mit Suche, Mitarbeiterliste und QR-Code-Anzeige."""
    root = tk.Tk()
    root.title("QR-Code Generator (personal)")

    rahmen = ttk.Frame(root, padding=10)
    rahmen.pack(fill=tk.BOTH, expand=True)

    # --- Suchzeile: Label + Eingabefeld + Suchen-Button ---
    zeile = ttk.Frame(rahmen)
    zeile.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(zeile, text="Suchen:").pack(side=tk.LEFT, padx=(0, 6))
    suchfeld = ttk.Entry(zeile, width=28)  # Eingabefeld für den Suchbegriff
    suchfeld.pack(side=tk.LEFT, padx=(0, 6))

    # --- Trefferanzeige: Anzahl gefundener Mitarbeiter ---
    anzahl = ttk.Label(rahmen, text="")
    anzahl.pack(anchor=tk.W, pady=(0, 4))

    # --- Scrollbare Namensliste ---
    frm = ttk.Frame(rahmen)
    frm.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
    liste = tk.Listbox(frm, height=12, width=48)  # Listbox: einfache Auswahlliste
    sb = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=liste.yview)
    liste.configure(yscrollcommand=sb.set)  # Scrollbar mit Liste verknüpfen
    liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)

    # --- Label für die QR-Code-Anzeige ---
    qr_label = tk.Label(rahmen, bg="white")
    qr_label.pack(pady=8)

    # foto als Liste, damit die Referenz erhalten bleibt
    # (ohne Referenz löscht Pythons Garbage Collector das Bild aus dem Speicher)
    foto = []
    alle = []  # Aktuelle Mitarbeiterliste (Tupel) – synchron zur Listbox

    def liste_fuellen():
        """Datenbankabfrage starten und Listbox befüllen."""
        nonlocal alle
        try:
            alle = list(mitarbeiter_laden(suchfeld.get()))
        except mariadb.Error as e:
            messagebox.showerror("Datenbankfehler", str(e), parent=root)
            return
        liste.delete(0, tk.END)  # Alte Einträge aus der Listbox entfernen
        for m in alle:
            liste.insert(tk.END, f"{m[0]}: {m[1]} {m[2]}")  # "Nr: Vorname Nachname"
        anzahl.configure(text=f"{len(alle)} Mitarbeiter")
        if alle:
            liste.selection_set(0)  # Ersten Eintrag vorauswählen

    def generieren(_event=None):
        """QR-Code für den ausgewählten Mitarbeiter erzeugen und anzeigen."""
        sel = liste.curselection()  # Index des markierten Listeneintrags
        if not sel:
            messagebox.showwarning("Auswahl", "Bitte einen Mitarbeiter wählen.", parent=root)
            return
        bild = qr_bild(qr_text(alle[sel[0]]))  # QR-Bild erzeugen
        img = ImageTk.PhotoImage(bild)          # In Tkinter-kompatibles Format umwandeln
        foto.clear()
        foto.append(img)  # Referenz speichern – verhindert Garbage Collection des Bildes
        qr_label.configure(image=img, width=bild.width, height=bild.height)

    ttk.Button(zeile, text="Suchen", command=liste_fuellen).pack(side=tk.LEFT)
    suchfeld.bind("<Return>", lambda _: liste_fuellen())  # Enter = Suche starten
    ttk.Button(rahmen, text="QR-Code generieren", command=generieren).pack()
    liste.bind("<Double-Button-1>", generieren)  # Doppelklick = QR-Code generieren

    liste_fuellen()  # Beim Programmstart alle Mitarbeiter sofort laden
    root.mainloop()  # Ereignisschleife – Fenster bleibt geöffnet


if __name__ == "__main__":
    qr_code_fenster()

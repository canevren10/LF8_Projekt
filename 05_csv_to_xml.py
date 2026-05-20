# ==============================================================================
# Meilenstein 1.5 – CSV-Datei in XML-Datei umwandeln
# Zweck: Die in Meilenstein 1.3 erzeugte lagerbestand.csv wird eingelesen und
#        als strukturierte XML-Datei (lagerbestand.xml) gespeichert.
# Bibliotheken:
#   csv                   – Einlesen der CSV-Datei
#   xml.etree.ElementTree – Erstellen und Schreiben der XML-Struktur
# ==============================================================================

import csv
import xml.etree.ElementTree as ET  # ET: Kurzname für die XML-Bibliothek


def csv_to_xml(eingabe_datei, ausgabe_datei):
    """
    Wandelt eine CSV-Datei in eine XML-Datei um.

    Die erste Zeile der CSV wird als XML-Elementnamen (Tags) verwendet.
    Jede weitere Zeile entspricht einem <Artikel>-Kindelement in der XML.

    Parameter:
        eingabe_datei – Pfad zur Quell-CSV (Semikolon-getrennt, UTF-8)
        ausgabe_datei – Pfad zur Ziel-XML
    """
    # Schritt 1: CSV einlesen – Semikolon und UTF-8 wie in 03_DBinCSV.py
    with open(eingabe_datei, newline="", encoding="utf-8") as f:
        zeilen = list(csv.reader(f, delimiter=";"))  # Alle Zeilen in eine Liste laden

    if not zeilen:
        raise ValueError("CSV-Datei ist leer.")  # Abbruch bei leerer Datei

    kopf = zeilen[0]   # Erste Zeile = Spaltennamen (werden zu XML-Tags)
    daten = zeilen[1:] # Alle weiteren Zeilen = Datensätze

    # Schritt 2: XML-Wurzelelement anlegen; enthält alle Artikel als Kindelemente
    root = ET.Element("Lagerbestand")  # <Lagerbestand> ist das Wurzelelement

    for zeile in daten:
        # Zeile auf Länge der Kopfzeile auffüllen (fehlende Zellen werden leer)
        zelle = (zeile + [""] * len(kopf))[: len(kopf)]

        artikel = ET.SubElement(root, "Artikel")  # <Artikel> für jeden Datensatz

        for name, wert in zip(kopf, zelle):
            # Spaltennamen als XML-Tag: Leerzeichen → Unterstrich, leerer Name → "Feld"
            tag = name.strip().replace(" ", "_") or "Feld"
            feld = ET.SubElement(artikel, tag)  # z. B. <ArtikelNr>
            feld.text = wert                    # Textwert des Elements setzen

    # Schritt 3: XML-Baum einrücken (lesbar) und in Datei schreiben
    baum = ET.ElementTree(root)
    ET.indent(baum, space="  ")  # 2 Leerzeichen Einrückung (ab Python 3.9)
    baum.write(
        ausgabe_datei,
        encoding="utf-8",
        xml_declaration=True,    # <?xml version='1.0' encoding='utf-8'?> am Anfang
    )


if __name__ == "__main__":
    # Standardaufruf mit den Dateien aus Meilenstein 1.3
    csv_to_xml("lagerbestand.csv", "lagerbestand.xml")
    print("XML-Datei gespeichert: lagerbestand.xml")

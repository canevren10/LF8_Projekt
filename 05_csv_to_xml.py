# Meilenstein 1.5: CSV-Datei einlesen und als XML speichern

import csv
import xml.etree.ElementTree as ET


def csv_to_xml(input_file, output_file):
  """Liest eine CSV (Kopfzeile = Elementnamen) und schreibt eine XML-Datei."""
  # Schritt 1: CSV einlesen (wie 03_DBinCSV: Semikolon, UTF-8)
  with open(input_file, newline="", encoding="utf-8") as f:
    zeilen = list(csv.reader(f, delimiter=";"))

  if not zeilen:
    raise ValueError("CSV-Datei ist leer.")

  kopf = zeilen[0]
  daten = zeilen[1:]

  # Schritt 2: Wurzelelement; jede Datenzeile wird ein Kindelement
  root = ET.Element("Lagerbestand")

  for zeile in daten:
    # Zeile auf gleiche Länge wie Spalten bringen (fehlende Zellen = leer)
    zelle = (zeile + [""] * len(kopf))[: len(kopf)]
    artikel = ET.SubElement(root, "Artikel")
    for name, wert in zip(kopf, zelle):
      # XML-Tag aus Spaltenname (Leerzeichen durch Unterstrich)
      tag = name.strip().replace(" ", "_") or "Feld"
      feld = ET.SubElement(artikel, tag)
      feld.text = wert

  # Schritt 3: formatiert speichern (Einrückung ab Python 3.9)
  baum = ET.ElementTree(root)
  ET.indent(baum, space="  ")
  baum.write(
    output_file,
    encoding="utf-8",
    xml_declaration=True,
  )


if __name__ == "__main__":
  # Standard: Lager-CSV aus Meilenstein 1.3
  csv_to_xml("lagerbestand.csv", "lagerbestand.xml")
  print("XML-Datei gespeichert: lagerbestand.xml")

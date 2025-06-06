import pandas as pd
import os

# Pfade
basis_pfad = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA"
excel_pfad = os.path.join(basis_pfad, "Daten für Projekt/Einspeiseanlagen Bremen SAP Export (important)/Anlagen_Bremen_30kW_FIX.xlsx")
malo_csv_pfad = os.path.join(basis_pfad, "Daten für Projekt/Generators.csv + einspeiseprofile/malo_liste.csv")

# Sheetnamen
sheet_malo = "malo tabelle"
sheet_anlagen = "sap export"

# 1. Lade die Liste der gewünschten Malos
malo_liste = pd.read_csv(malo_csv_pfad)
malo_liste["malo"] = malo_liste["malo"].astype(str).str.strip()

# 2. Lade Malo-Zuordnung aus Excel
malo_tabelle = pd.read_excel(excel_pfad, sheet_name=sheet_malo)
malo_tabelle = malo_tabelle[["Anlage", "Zählpunktbezeichnung (Malo)"]]
malo_tabelle.columns = ["Anlage", "Malo"]
malo_tabelle["Anlage"] = malo_tabelle["Anlage"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
malo_tabelle["Malo"] = malo_tabelle["Malo"].astype(str).str.strip()

# ➤ Filtere nur die Zeilen, deren Malo in malo_liste.csv enthalten ist
malo_tabelle = malo_tabelle[malo_tabelle["Malo"].isin(malo_liste["malo"])]

print("Einmalige Malo-Zählung:", malo_tabelle["Malo"].nunique())
print("Anzahl Malo-Zeilen nach Filterung:", len(malo_tabelle))


# 3. Lade Anlagendaten
anlagen_tabelle = pd.read_excel(excel_pfad, sheet_name=sheet_anlagen)
anlagen_tabelle = anlagen_tabelle[[
    "Anlagennummer", "Energiebezeichnung", "Anlagenart",
    "Breitengrad", "Längengrad", "Nennwirkleistung"
]]
anlagen_tabelle.columns = ["Anlage", "carrier", "type", "lat", "lon", "p_nom"]
anlagen_tabelle["Anlage"] = anlagen_tabelle["Anlage"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)

# 4. Merge mit den gefilterten Malos
merged = pd.merge(malo_tabelle, anlagen_tabelle, on="Anlage", how="left")
merged = merged.dropna(subset=["lat", "lon", "p_nom", "type", "carrier"])

# 5. Zusätzliche PyPSA-Spalten
merged["bus"] = "unzugeordnet"
merged["name"] = "Gen_" + merged["Malo"].astype(str)

# 6. Endgültige Datei schreiben
generators = merged[["name", "bus", "p_nom", "type", "carrier", "lat", "lon"]]
ausgabe_pfad = os.path.join(os.path.dirname(__file__), "generators.csv")
generators.to_csv(ausgabe_pfad, index=False)

print(f"{len(generators)} Generatoren (gefiltert nach malo_liste.csv) gespeichert in:\n{ausgabe_pfad}")
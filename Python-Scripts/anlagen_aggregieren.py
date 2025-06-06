import pandas as pd
import os

# Aktueller Ordner (dort, wo das Skript liegt)
ordner = os.path.dirname(__file__)

# Pfad zur originalen generators.csv
eingabe_pfad = os.path.join(ordner, "generators.csv")

# CSV einlesen
df = pd.read_csv(eingabe_pfad)

# Gruppierung nach 'name' (z. B. Gen_51402672129)
aggregiert = df.groupby("name").agg({
    "p_nom": "sum",
    "type": "first",
    "carrier": "first",
    "lat": "first",
    "lon": "first",
    "bus": "first"
}).reset_index()

# Spaltenreihenfolge
final_df = aggregiert[["name", "bus", "p_nom", "type", "carrier", "lat", "lon"]]

# Pfad zur neuen Datei
ausgabe_pfad = os.path.join(ordner, "generators_aggregated.csv")
final_df.to_csv(ausgabe_pfad, index=False)

print(f"{len(final_df)} aggregierte Generatoren gespeichert in:\n{ausgabe_pfad}")
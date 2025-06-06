import pandas as pd
from geopy.distance import geodesic

# Verbindungen zwischen Knotenpunkten
verbindungen = [
    ("Farge", "Bremen/Nord"),
    ("Bremen/Nord", "Rönnebeck"),
    ("Rönnebeck", "Blumenthal"),
    ("Blumenthal", "Vulkan"),
    ("Vulkan", "UW Lesum"),
    ("Vulkan", "Grambke"),
    ("Vulkan", "Vegesack"),
    ("Vulkan", "Gröpelingen"),
    ("Vulkan", "UW Oslebshausen"),
    ("UW Lesum", "UW Oslebshausen"),
    ("UW Oslebshausen", "Gröpelingen"),
    ("Gröpelingen", "Umspannwerk Plantage"),
    ("Gröpelingen", "Blockland"),
    ("Gröpelingen", "Neuenland"),
    ("Vegesack", "Grambke"),
    ("UW Lesum", "Grambke"),
    ("Grambke", "Grambke 2"),
    ("Grambke", "Kraftwerk Hafen"),
    ("Grambke", "Mittelsbüren"),
    ("Grambke", "Niedervieland"),
    ("Niedervieland", "Mittelsbüren"),
    ("Grambke", "Blockland"),
    ("Umspannwerk Plantage", "Blockland"),
    ("Umspannwerk Plantage", "Neuenland"),
    ("Neuenland", "Warturm"),
    ("Warturm", "Warturm 2"),
    ("Warturm", "Niedervieland"),
    ("Warturm", "Huchting"),
    ("Umspannwerk Süd", "Umspannwerk Lange Wieren"),
    ("Umspannwerk Süd", "Kraftwerk Vahr"),
    ("Umspannwerk Lange Wieren", "Kraftwerk Vahr"),
    ("Kraftwerk Vahr", "UW Kirchbachstraße"),
    ("UW Kirchbachstraße", "Umspannwerk Plantage"),
    ("UW Kirchbachstraße", "Blockland"),
]

# Datei-Pfade
input_csv = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/pypsa-env/Netz_modell/Daten für Projekt/Knoten+Leitungen (important)/pypsa_substations_110kV_filtered_cleaned.csv"
output_csv = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/pypsa-env/Netz_modell/Daten für Projekt/Knoten+Leitungen (important)/lines.csv"

# Daten einlesen
df = pd.read_csv(input_csv)
knoten_coords = dict(zip(df["name"], zip(df["y"], df["x"])))

# Leitungseigenschaften
r_ohm_per_km = 0.03
x_ohm_per_km = 0.4
s_nom_default = 150  # MVA

lines = []

for bus0, bus1 in verbindungen:
    coord0 = knoten_coords.get(bus0)
    coord1 = knoten_coords.get(bus1)

    if coord0 is None or coord1 is None:
        print(f"FATAL ERROR: Koordinaten fehlen für Verbindung {bus0} - {bus1}")
        continue

    dist_km = geodesic(coord0, coord1).km

    lines.append({
        "name": f"Line_{bus0}_{bus1}",
        "bus0": bus0,
        "bus1": bus1,
        "length_km": round(dist_km, 3),
        "r": round(dist_km * r_ohm_per_km, 4),
        "x": round(dist_km * x_ohm_per_km, 4),
        "s_nom": s_nom_default
    })

# Speichern
df_lines = pd.DataFrame(lines)
df_lines.to_csv(output_csv, index=False)

print("Datei 'lines.csv' wurde erfolgreich erstellt!")

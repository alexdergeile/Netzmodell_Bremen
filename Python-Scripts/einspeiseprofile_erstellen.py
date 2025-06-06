import pandas as pd
import os

# Pfade
profilordner = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Lastgänge/Lastgangdaten"
generators_csv = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Daten für Projekt/Generators.csv + einspeiseprofile/generators_with_bus.csv"
output_p = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Daten für Projekt/Generators.csv + einspeiseprofile/generators-p.csv"

# Lade die Generatorenliste
gens = pd.read_csv(generators_csv)
malos = gens["name"].str.replace("Gen_", "", regex=False)

# Dictionary zum Speichern aller Zeitscheiben
profile_dict = {}

# Listen für Zusammenfassung
fehlende_dateien = []
fehlerhafte_dateien = []

# Schleife über alle Malos
for malo in malos:
    dateipfad = os.path.join(profilordner, f"{malo}.csv")
    if not os.path.isfile(dateipfad):
        fehlende_dateien.append(malo)
        continue

    try:
        df = pd.read_csv(dateipfad, sep=";", encoding="utf-8")

        # Prüfen auf Spaltennamen
        if {"Ab-Datum", "Ab-Zeit", "Profilwert"}.issubset(df.columns):
            # Zeitstempel erstellen
            df["snapshot"] = pd.to_datetime(df["Ab-Datum"] + " " + df["Ab-Zeit"], dayfirst=True)

            # Profilwert in deutschem Zahlenformat bereinigen und umwandeln
            df["Profilwert"] = df["Profilwert"].astype(str)  # falls numerisch gemischt
            df["Profilwert"] = df["Profilwert"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
            df["mw"] = df["Profilwert"].astype(float) / 1000  # kW → MW

            df.set_index("snapshot", inplace=True)
            profile_dict[f"Gen_{malo}"] = df["mw"]
        else:
            fehlerhafte_dateien.append(malo)
            print(f"Unerwartete Spalten in Datei {malo}: {list(df.columns)}")

    except Exception as e:
        fehlerhafte_dateien.append(malo)
        print(f"Fehler beim Verarbeiten von {malo}: {e}")

# Alles zusammenführen zu einem DataFrame
gesamtprofil = pd.DataFrame(profile_dict)
gesamtprofil.reset_index(inplace=True)
gesamtprofil.rename(columns={"snapshot": "snapshot"}, inplace=True)

# Speichern
gesamtprofil.to_csv(output_p, index=False)
print(f"\n generators-p.csv erfolgreich gespeichert unter:\n{output_p}")

# Zusammenfassung
print("\n Zusammenfassung:")
print(f"Fehlende Dateien: {len(fehlende_dateien)}")
if fehlende_dateien:
    print("  ->", ", ".join(fehlende_dateien[:10]) + ("..." if len(fehlende_dateien) > 10 else ""))

print(f"Fehlerhafte Dateien: {len(fehlerhafte_dateien)}")
if fehlerhafte_dateien:
    print("  ->", ", ".join(fehlerhafte_dateien[:10]) + ("..." if len(fehlerhafte_dateien) > 10 else ""))
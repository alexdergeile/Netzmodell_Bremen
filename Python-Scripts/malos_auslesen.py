import os
import pandas as pd

# Pfad zum Ordner mit den Lastgangdateien
ordner_pfad = "/home/slatty/Uni/M.Sc/Master SEM III/Masterprojekt/PyPSA/Lastgänge/Lastgangdaten"

# Liste aller .csv-Dateien im Ordner
dateien = [f for f in os.listdir(ordner_pfad) if f.endswith(".csv")]

# Extrahiere die Malo aus dem Dateinamen (alles vor .csv)
malos = [os.path.splitext(f)[0] for f in dateien]

# Erstelle ein DataFrame
df_malos = pd.DataFrame({"malo": malos})

# Speichere das als CSV
ausgabe_pfad = os.path.join(ordner_pfad, "malo_liste.csv")
df_malos.to_csv(ausgabe_pfad, index=False)

print(f"{len(malos)} Malos gespeichert in: {ausgabe_pfad}")
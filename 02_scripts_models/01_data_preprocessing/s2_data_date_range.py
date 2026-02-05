# Dieses Script filtert die S2 Datensätze hinsichtlich der festgelegten PI-Zeiträume aus der PI-Basisdatei

import pandas as pd
from pathlib import Path

# Logging Module einbinden
import logging

logging.basicConfig(
    level=logging.INFO,  # ERROR?
    format="%(asctime)s - [%(filename)s] - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    filename="logbuch.log",
    filemode="a",  # 'a' = append (anhängen), 'w' = write immer neu
    encoding="utf-8",
)

# PI-Datei vorbereiten

pi_file = pd.read_csv(
    r"/project/01_data/01_csv_data/00_pi_basics/01_pi_final_final.csv",
    header=0,
    sep=",",
    encoding="utf-8",
)

# Nur PI Namen und start und end date nehmen
pi_file_small = pi_file[["nachname", "start_date", "end_date"]].sort_values("nachname")

pi_file_small["start_date"] = pd.to_datetime(
    pi_file_small["start_date"], errors="coerce"
)
pi_file_small["end_date"] = pd.to_datetime(pi_file_small["end_date"], errors="coerce")

pi_file_small["start_date"] = pi_file_small["start_date"].dt.year
pi_file_small["end_date"] = pi_file_small["end_date"].dt.year

pi_file_small["end_date"] = pi_file_small["end_date"].fillna(3000).astype(int)
pi_file_small["start_date"] = pi_file_small["start_date"].fillna(1900).astype(int)

# print(pi_file_small.head(10))
# exit()

# Dateiensuche, Filterung und Speicherung für die S2-Dateien

folder_path = r"/project/01_data/01_csv_data/98_s2/unsorted_data/"
pfad = Path(folder_path)

# Alle CSVs finden
found_files = list(pfad.glob("*.csv"))

# Wir gehen durch jede Datei im Ordner
for file in found_files:
    # Umwandlung des Dateinamens in reinen Text für den Vergleich
    dateiname_text = file.name  # z.B. "pubs_Müller.csv"

    # Wir prüfen für jede Datei jede Person in deiner Liste
    # index=False, damit wir direkt auf die Spalten zugreifen können
    for row in pi_file_small.itertuples(index=False):
        # 1. KORREKTUR: Einfacher Text-Vergleich
        # "Ist der Nachname im Dateinamen enthalten?"
        if str(row.nachname) in dateiname_text:
            try:
                # Datei laden
                df = pd.read_csv(file, sep=";", encoding="utf-8")

                # 2. KORREKTUR: Filter-Logik für Pandas
                # Wir müssen zwei Bedingungen mit & verknüpfen
                # Und wichtig: Klammern um jede Bedingung!
                maske = (df["year"] >= row.start_date) & (df["year"] <= row.end_date)

                # 3. KORREKTUR: Eckige Klammern zum Anwenden des Filters
                df_filtered = df[maske]

                # Dateinamen zusammenbauen (f-String bereinigt)
                # Tipp: Nutze keine Pfade wie /project/ unter Windows, nimm relative Pfade oder r"..."
                speicher_name = f"/project/01_data/01_csv_data/98_s2/publications_{row.nachname}_{row.start_date}_{row.end_date}.csv"

                # Speichern (index=False ist meistens besser, um keine 0,1,2... Spalte zu haben)
                df_filtered.to_csv(speicher_name, sep=";", index=False)

                print(f"Datei korrekt erstellt als {speicher_name}.")
                logging.info(f"Datei korrekt erstellt als {speicher_name}.")

            except Exception as e:
                error = f"Fehler bei Datei {file.name}: {e}"
                print(error)
                logging.error(error)

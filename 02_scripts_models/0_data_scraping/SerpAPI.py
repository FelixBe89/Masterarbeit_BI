#################################################
# Dieser Code läuft so wie er ist und zieht über SerpAPI
# die Publikationen aller PIs mit Scholar_ID aus der PI-Basisdatei.
# Die Daten werden in Rohform und gefiltert (ab 2015) gespeichert.
#################################################

import serpapi
from serpapi import GoogleSearch
import os
import json
import pandas as pd
import sys

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

apikey = os.environ["SERPAPI_KEY"]

# Aufsetzen des Loops, um alle PIs mit Scholar_ID zu fetchen
try:
    df0 = pd.read_csv(
        "/project/01_data/01_csv_data/00_pi_basics/00_pi_final.csv", sep=";"
    )
except FileNotFoundError as e:
    print("Beim Einlesen der PI-Datei ist etwas schief gelaufen: {}!".format(e))
    logging.error("Die Basisdatei konnte nicht eingelesen werden!")
    sys.exit(1)

df1 = df0[["nachname", "scholar_id"]]

df2 = df1[~df1["scholar_id"].isin(["PubMed", "über Website"])]

# Test für  Datensätze! -- die ersten beiden sind erfolgreich gelaufen, jetzt folgen alle Verbliebenen!
df2 = df2.iloc[2:]

erfolgreiche_fetches = 0

for idx, row in df2.iterrows():
    try:
        # Zentrale Paramter von SerpAPI, um die Daten zu finden -- hier Artikel!
        params = {
            "engine": "google_scholar_author",
            "author_id": row["scholar_id"],
            "api_key": apikey,
            # "as_ylo":2015,
            # "as_yhi":2025,
            "sort": "pubdate",
            "num": 20,
        }

        # Initialisierung der leeren Liste, in der die Artikel gespeichert werden
        all_articles = []
        start_val = 0

        while True:
            params["start"] = start_val

            search = GoogleSearch(params)
            results = search.get_dict()

            articles = results.get("articles", [])

            if not articles:
                print(
                    "Keine weiteren Ergebnisse zu den schon bestehenden mehr gefunden."
                )
                break
            else:
                all_articles.extend(articles)
                logging.info(
                    "Seite {} abgerufen. Gesamtanzahl Artikel: {}".format(
                        (start_val // 20) + 1, len(all_articles)
                    )
                )
                start_val += 20

        print(
            "Insgesamt {} Artikel bei {} gefunden.".format(
                len(all_articles), row["nachname"]
            )
        )  # herausgenommen: , "\n", 30*"===", "\n", all_articles)

        # Artikel aus JSON in neues Dataframe-Format bringen und sowohl komplett als auch gefiltert speichern
        df = pd.json_normalize(all_articles, sep="_")

        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        df.to_csv(
            f"/project/01_data/01_csv_data/01_publications/{row['nachname']}_raw.csv",
            sep=";",
        )

        df_filtered = df[df["year"] >= 2015].copy()

        print(
            f"Gesamtanzahl aller Artikel bei {row['nachname']}: {len(df)}. Nach Filter (≥2015): {len(df_filtered)}"
        )

        df_filtered.to_csv(
            f"/project/01_data/01_csv_data/01_publications/{row['nachname']}_2015-2025.csv",
            sep=";",
        )

        logging.info(
            f"Hat geklappt: {row['nachname']}: {len(df)} gesamt, "
            f"{len(df_filtered)} ab 2015"
        )

        erfolgreiche_fetches += 1

    except Exception as e:
        logging.error(
            "Fehler: Im Auslesen der Daten bei {} über die Scholar ID hat etwas nicht geklappt.".format(
                row["nachname"]
            )
        )
        continue

logging.info(
    "Insgesamt wurden {} PIs über Scholar komplett in ihren Pubs exportiert.".format(
        erfolgreiche_fetches
    )
)

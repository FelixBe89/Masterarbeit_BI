# Dieses Skript fetcht noch einmal die Autorendetails zu h-index, Anzahl Publikationen und Zitation von Semantic Scholar

# Die Daten werden in einer csv gespeichert und dann in die finale Datei gemerged!

import requests
import pandas as pd
import time

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

# Dict erstellen, in dem alle Daten gespeichert werden

all = {}


# Funktion zum Fetchen der Daten basierend auf der AutorenIDs
def get_author_metrics(author_id, api_key=None):

    base_url = "https://api.semanticscholar.org/graph/v1"
    fields = "hIndex,citationCount,paperCount,papers.citationCount"
    headers = {"x-api-key": api_key} if api_key else {}

    try:
        response = requests.get(
            f"{base_url}/author/{author_id}", params={"fields": fields}, headers=headers
        )

        if response.status_code != 200:
            print(f"Fehler bei {author_id}!")
            logging.error(f"Fehler bei {author_id}!")
            return None

        data = response.json()

        daten = {
            "h_index": data.get("hIndex"),
            "zitationen_gesamt": data.get("citationCount"),
            "publikationen_gesamt": data.get("paperCount"),
        }

        logging.info(f"Autorendaten für {author_id} erfolgreich geholt!")
        print(f"Autorendaten für {author_id} erfolgreich geholt!")

    except Exception as e:
        print(f"Fehler {e}")
        logging.error(f"Fehler bei {author_id}!")

    finally:
        time.sleep(1)

    return daten


# Daten einlesen und Funktion aufrufen

df0 = pd.read_csv(
    r"/project/01_data/01_csv_data/00_pi_basics/01_pi_final_final.csv",
    sep=",",
    encoding="utf-8",
)

s2_ids = df0["s2_id"].tolist()

for x in s2_ids:
    daten = get_author_metrics(x)
    all[x] = daten

print(60 * "=")
print("Gesamtes Dict der Rohdaten:", "\n", all)
print(60 * "=")

# Daten schreiben und ausgeben
try:
    df1 = (
        pd.DataFrame.from_dict(all)
        .fillna(0)
        .T.reset_index()
        .rename(columns={"index": "author_id"})
    )
    df1.to_csv(
        r"/project/01_data/01_csv_data/00_pi_basics/02_pi_pub_metrics.csv",
        sep=";",
        encoding="utf-8",
        index=False,
    )
except Exception as e:
    print(f"Fehler beim Schreiben des Dict: {e}.")
    logging.error(f"Fehler beim Schreiben des Dict: {e}.")

print(f"Länge der Datensätze = {len(all)}.", "\n\n", all)

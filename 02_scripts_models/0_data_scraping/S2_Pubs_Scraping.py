# Dieses Script fetcht die PI-Publikationsdaten von semantic scholar

# Version ohne API-Key!

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


def get_semantic_scholar_papers(author_id, api_key=None):

    base_url = "https://api.semanticscholar.org/graph/v1"
    headers = {"x-api-key": api_key} if api_key else {}

    try:
        fields = "paperId,title,year,abstract,citationCount,authors,fieldsOfStudy"
        response = requests.get(
            f"{base_url}/author/{author_id}/papers",
            params={"fields": fields, "limit": 100},
            headers=headers,
        )
        logging.info(f"S2-API-Zugriff war erfolgreich für {author_id}.")
    except Exception as e:
        print(
            f"Es ist ein Fehler beim Fetchen aufgetreten! Author ID {author_id}.",
            "\n",
            e,
        )
        logging.error(
            f"Es ist ein Fehler beim Fetchen aufgetreten! Author ID {author_id}.",
            "\n",
            e,
        )

    if response.status_code != 200:
        return pd.DataFrame()

    papers = response.json().get("data", [])

    processed = []
    for paper in papers:
        processed.append(
            {
                "paper_id": paper.get("paperId"),
                "title": paper.get("title"),
                "year": paper.get("year"),
                "abstract": paper.get("abstract"),
                "citation_count": paper.get("citationCount", 0),
                "authors": [a["name"] for a in paper.get("authors", [])],
                "keywords": paper.get("fieldsOfStudy", []),
                "source": "semantic_scholar",
            }
        )

    time.sleep(1)

    return pd.DataFrame(processed)


# Author ID für einzelne Person
# papers = get_semantic_scholar_papers("2080244021")
# papers.to_csv(r"/project/01_data/01_csv_data/99_pubmed/publications_Heuckmann_2015-3000.csv", sep=";", encoding="utf-8")

# Für mehrere Autoren aus der PI-Liste
df_pi = pd.read_csv(
    r"/project/01_data/01_csv_data/00_pi_basics/01_pi_final_final.csv",
    sep=",",
    encoding="utf-8",
)
author_ids = df_pi[["nachname", "s2_id"]]
# print(author_ids)

for lbl, row in author_ids.iterrows():
    # print(row["s2_id"], " ", row["nachname"])
    df = get_semantic_scholar_papers(row["s2_id"])
    df.to_csv(
        f"/project/01_data/01_csv_data/98_s2/publications_{row['nachname']}_raw.csv",
        sep=";",
        encoding="utf-8",
    )
    logging.info(
        "S2-Zugriff bei {} hat geklappt, CSV-Datei wurde gespeichert.".format(
            row["nachname"]
        )
    )
    time.sleep(1)

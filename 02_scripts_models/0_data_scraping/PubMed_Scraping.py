# ###################### Info ######################
# Das Skript fetcht und speichert korrekt!
# Die Ergebnisqualität ist gut und kann so verwendet werden!
# ##################################################

from pymed import PubMed
import pandas as pd
import os

# Logging Module einbinden
import logging

logging.basicConfig(
    level=logging.INFO,  # ERROR?
    format="%(asctime)s - [%(filename)s] - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    filename="logbuch.log",
    filemode="a",  # "a" = append (anhängen), "w" = write immer neu
    encoding="utf-8",
)

# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/


def pubmed_search(
    first_name: str,
    last_name: str,
    start_date: str,
    end_date: int = "3000",
    max_results: int = 1000,
    orcid_id: str = None,
) -> pd.DataFrame:
    """Diese Funktion durchsucht PubMed nach Artikeln eines bestimmten Autors innerhalb
    eines Datumsbereichs. Es wird explizit nicht die ORCID ID verwendet, weil diese gerade bei
    älteren Artikeln noch **nicht** referenziert ist und deswegen die Ergebnismenge deutlich einschränkt.

    Args:
        first_name (str): Vorname des Autors (Umlaute sind kein Problem)
        last_name (str): Nachname des Autors
        start_date (str): Startdatum für die Suche im Format "YYYY/MM/DD"
        end_date (str, optional): Enddatum ist optional und ebenfalls im Format "YYYY/MM/DD" anzugeben.
            Standardwert ist "3000", weil sich das zu "bis heute" übersetzt.
        max_results (int, optional): Maximale Anzahl der anzuzeigenden Ergebnisse. Standard ist auf 1000 gesetzt.

    Returns:
        pd.DataFrame: Relationaler DataFrame mit den Suchergebnissen
    """
    try:
        # Initiierung des PubMed Objekts
        pubmed = PubMed(tool="MyTool")

        # Erstellen der Standard-Suchanfrage, wie sie auf PubMed möglich ist (https://pubmed.ncbi.nlm.nih.gov/advanced/)
        query = f"({last_name}, {first_name}[Author]) AND (({start_date}[Date - Publication] : {end_date}[Date - Publication]))"

        # Ausführen der Suche
        results = pubmed.query(query, max_results=max_results)

        # Liste zur Speicherung der Ergebnisse
        list_results = []

        # Loop für die Ergebnismenge
        for idx, article in enumerate(results):
            # print(article.toDict()) # Möglichkeit, alle verfügabren Attribute zu sehen
            # article_id = article.pubmed_id
            list_results.append(
                {
                    "title": article.title,
                    "keywords": article.keywords,
                    "publication_date": article.publication_date,
                    "co_authors": article.authors,
                    "abstract": article.abstract if article.abstract else "no abstract",
                }
            )

        # Prüfung der Ergebnismenge auf Inhalte
        if len(list_results) == 0:
            print(
                "Keine Ergebnisse für {} {} im angegebenen Zeitraum.".format(
                    first_name, last_name
                )
            )
            logging.error(
                "Keine Ergebnisse für {} {} im angegebenen Zeitraum auf PubMed.".format(
                    first_name, last_name
                )
            )
            return

        # ORCID ID hinzufügen, wenn angegeben
        if orcid_id:
            print("ORCID funktioniert schlecht, deswegen ganz herausgenommen!")
            pass
            # list_results2 = []
            # query2 = f"({orcid_id}[auid]) AND (({start_date}[Date - Publication] : {end_date}[Date - Publication]))"
            # results2 = pubmed.query(query2, max_results=max_results)
            # for article in results2:
            #     list_results2.append(
            #         {
            #             "title": article.title,
            #             "keywords": article.keywords,
            #             "publication_date": article.publication_date,
            #             "co_authors": article.authors,
            #             "abstract": article.abstract
            #             if article.abstract
            #             else "no abstract",
            #         }
            #     )
        else:
            pass

        # df erstellen
        df = pd.DataFrame(list_results)

        # Datei öffnen
        # os.startfile("pubmed_results.xlsx")

        # Datei speichern
        rel_path = "01_data/01_csv_data/99_pubmed/"
        df.to_csv(
            f"{rel_path}publications_{last_name}_{start_date[:4]}-{end_date[:4]}.csv",
            index=False,
        )

        print("{} fertig mit {} Einträgen :)".format(last_name, len(df)))
        logging.info(
            "{} fertig mit {} Einträgen über PubMed :)".format(last_name, len(df))
        )
        if orcid_id:
            print(
                "Zusätzlich wurden {} Einträge über die ORCID ID gefunden.".format(
                    len(list_results2)
                )
            )
            logging.info(
                "Zusätzlich wurden {} Einträge über die ORCID ID gefunden.".format(
                    len(list_results2)
                )
            )

        return df

    except Exception as e:
        print("Es ist ein Fehler aufgetreten:", e)
        logging.error("Es ist ein Fehler aufgetreten:", e)


#############################################################
# Daten aus PI-Frame einlesen, um **alle** PIs zu fetchen
#############################################################

# try:
#     pi_frame = pd.read_csv(r"/project/01_data/01_csv_data/00_pi_basics/01_pi_final_final.csv", header=0, sep=",", encoding="utf-8")

#     pi_frame.astype({"pi_id": "int64", "nach_und_vorname": "str",
#             "scholar_id": "str", "vorname": "str",
#             "nachname": "str", "start_date": "str",
#             "end_date": "str"})

#     pi_frame["start_date"] = pi_frame["start_date"].str.replace("-", "/")
#     pi_frame["end_date"] = pi_frame["end_date"].str.replace("-", "/").str.replace(" 00:00:00", "")

#     # print(pi_frame)

#     for lbl, row in pi_frame.iterrows():
#         pubmed_search(row[4], row[5], row[6], row[7])

# except FileNotFoundError as f:
#     print("Date konnte nicht eingelesen werden: {}.".format(f))
#     logging.error("Date konnte nicht eingelesen werden: {}.".format(f))

#############################################################
# Für **einzelne** Suchen, um Personen und Daten nachzuladen
#############################################################
pubmed_search("vorname", "nachname", "2015/01/01")

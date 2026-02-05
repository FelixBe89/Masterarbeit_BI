# Dieses Skript erstellt eine finale Auswertung aller Analyseergebnisse pro PI
# und inkludiert die Faktorscores, die Themencluster aus Publikationen und Drittmitteln
# sowie die Netzwerkmetriken.

# Importieren der notwendigen Bibliotheken
import pandas as pd
from pathlib import Path
import openpyxl
import os

# Pfade definieren
base_dir = Path().parent.parent
pi_data_dir = base_dir / "01_data" / "04_efa"
tm_data_dir = base_dir / "01_data" / "03_topic_modeling" / "02_topic_results"
net_dir = base_dir / "01_data" / "05_network"
output_dir = base_dir / "01_data"

# Einlesen der Ergebnisse
try:
    pi_df = pd.read_csv(
        pi_data_dir / "efa_pi_data_with_factors.csv", encoding="utf-8", sep=";"
    )

    pub_tm_df = pd.read_csv(
        tm_data_dir / "pi_publication_metrics_all-MiniLM_03.02.26.csv", encoding="utf-8"
    )
    tpf_tm_df = pd.read_csv(
        tm_data_dir / "pi_tpf_metrics_LaBSE_03.02.26.csv", encoding="utf-8"
    )

    nw_df = pd.read_csv(net_dir / "network_metrics_pis_03.02.26.csv", encoding="utf-8")
except FileNotFoundError as e:
    print(f"Fehler beim Einlesen der Datei: {e}")

# Zusammenführen der Datenframes basierend auf "pi_id"
final_df = pi_df.merge(
    pub_tm_df, left_on="pi_name_hashed", right_on="source", how="left"
)
final_df = final_df.merge(
    tpf_tm_df, left_on="pi_name_hashed", right_on="nachname", how="left"
)
final_df = final_df.merge(
    nw_df, left_on="pi_name_hashed", right_on="pi_name_hashed", how="left"
)

# Sortieren der Spalten
final_df = final_df[
    [
        "pi_name_hashed",
        "s2_citations",
        "h_index",
        "publikationen_gesamt",
        "drittmittel_gesamt",
        "drittmittel_volumen",
        "EFA_Faktor_Pubs",
        "EFA_Faktor_TPF",
        "topic_count_x",
        "total_pubs",
        "top3_topics_nr_x",
        "top3_topics_title_x",
        "topic_count_y",
        "total_tpfs",
        "top3_topics_nr_y",
        "top3_topics_title_y",
        "degree_centrality",
        "betweenness_centrality",
        "closeness_centrality",
    ]
]

final_df.rename(
    columns={
        "pi_name_hashed": "pi_name",
        "s2_citations": "anzahl_zitationen",
        # "h_index",
        # "publikationen_gesamt",
        # "drittmittel_gesamt",
        # "drittmittel_volumen",
        # "EFA_Faktor_Pubs",
        # "EFA_Faktor_TPF",
        "topic_count_x": "topic_count_publications",
        # "total_pubs",
        "top3_topics_nr_x": "top3_topics_nr_publications",
        "top3_topics_title_x": "top3_topics_title_publications",
        "topic_count_y": "topic_count_tpf",
        # "total_tpfs",
        "top3_topics_nr_y": "top3_topics_nr_tpf",
        "top3_topics_title_y": "top3_topics_title_tpf",
        # "degree_centrality",
        # "betweenness_centrality",
        # "closeness_centrality"
    },
    inplace=True
)

# Speichern des finalen DataFrames
final_df.to_csv(
    output_dir / "final_evaluation_per_pi.csv", index=False, encoding="utf-8"
)
final_df.to_excel(
    output_dir / "final_evaluation_per_pi.xlsx", index=False, engine="openpyxl"
)

try:
    os.startfile(output_dir / "final_evaluation_per_pi.xlsx")
except Exception as e:
    print(f"Konnte die Datei nicht automatisch öffnen: {e}")

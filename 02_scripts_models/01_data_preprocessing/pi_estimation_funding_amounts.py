# In diesem Skript werden die Drittmittelvolumina auf Schätzbasis als Kennzahl für die PIs erstellt.

# Import der Module
import pandas as pd
from pathlib import Path

# Definition der relativen Pfade
base_dir = Path.cwd().parent

data_dir_tpf = base_dir / "01_data" / "01_csv_data"

# Einlesen der Rohdaten
df_tpf_raw = pd.read_excel(
    f"{data_dir_tpf}/raw_data_projects_2003-2025.xlsx", engine="openpyxl"
)

# Check
print(df_tpf_raw.head(3))

# Features eingrenzen
df_tpf_raw = df_tpf_raw[
    [
        "Person: Nachname",
        "Projekt: Art des Projekts",
        "Projekt: Titel des Projekts Deutsch",
        "Projekt: Titel des Projekts Englisch (GB)",
        "Projekt: Stichwörter Deutsch",
        "Projekt: Stichwörter Englisch (GB)",
        "Projekt: Projektstart an der Universität Münster",
        "Projekt: Projektende an der Universität Münster",
        "Projekt: Kurzzusammenfassung Englisch (GB)",
        "Projekt: Kurzzusammenfassung Deutsch",
        "Projekt: Langbeschreibung Englisch (GB)",
        "Projekt: Langbeschreibung Deutsch",
    ]
].copy()

# Features umbenennen
df_tpf_raw.rename(
    columns={
        "Person: Nachname": "nachname",
        "Projekt: Art des Projekts": "project_type",
        "Projekt: Titel des Projekts Deutsch": "title_de",
        "Projekt: Titel des Projekts Englisch (GB)": "titel_en",
        "Projekt: Stichwörter Deutsch": "keywords_de",
        "Projekt: Stichwörter Englisch (GB)": "keywords_en",
        "Projekt: Projektstart an der Universität Münster": "start_date",
        "Projekt: Projektende an der Universität Münster": "end_date",
        "Projekt: Kurzzusammenfassung Englisch (GB)": "short_abstract_en",
        "Projekt: Kurzzusammenfassung Deutsch": "short_abstract_de",
        "Projekt: Langbeschreibung Englisch (GB)": "long_abstract_en",
        "Projekt: Langbeschreibung Deutsch": "long_abstract_de",
    },
    inplace=True,
)

# Check
print(df_tpf_raw.info())


# Schätzung der Drittmittelvolumina auf Basis der Angaben des DFG-Förderatlas 2024
# (Quelle: https://foerderatlas.dfg.de/daten/universitaet-muenster/)

# Es wird eine Schätzung vorgenommen, um den verschiedenen Projektarten ein Drittmittelvolumen zuzuordnen.


def estimated_project_funding(df_tpf: pd.DataFrame) -> pd.DataFrame:
    """Diese Funktion schätzt das Drittmittelvolumen basierend auf der Projektart und dem Dreijahreszuweisungen der DFG von 2020 bis 2022, was
    bei 31,8 Mio. Euro lag.

    Args:
        df_tpf (pd.DataFrame): Eingabedaten mit Projektarten.

    Returns:
        pd.DataFrame: Ursprünglicher DataFrame erweitert um die geschätzten Drittmittelvolumen.
    """

    # Basissatz
    total_three_years = 31800000  # in Euro

    # Aufteilung auf alle DFG-Projekte des Fachbereichs im Zeitraum 2020-2022
    filter_mask = (df_tpf["project_type"].str.contains("DFG|individual", na=False)) & (
        (df_tpf["start_date"].dt.year >= 2020) | (df_tpf["end_date"].dt.year <= 2022)
    )
    num_dfg_projects = df_tpf[filter_mask].shape[0]
    if num_dfg_projects == 0:
        raise ValueError("Keine DFG-Projekte im angegebenen Zeitraum gefunden.")
    average_funding_per_project = total_three_years / num_dfg_projects

    # Checks
    print(
        f"Anzahl der im Dreijahreszeitraum gefundenen DFG-Projekte: {num_dfg_projects}.\n"
    )
    print(
        f"Durchschnittsvolumen pro Projekt: {round(average_funding_per_project, 0):.0f} Euro.\n"
    )

    # Gewichtung einführen
    def assign_funding(row):
        if pd.isna(row["project_type"]):
            return 0
        elif "dfg" in row["project_type"]:
            return average_funding_per_project * 1.0
        elif "individual" in row["project_type"]:
            return average_funding_per_project * 1.0
        elif "eu" in row["project_type"]:
            return average_funding_per_project * 2.0
        elif "bmbf" in row["project_type"]:
            return average_funding_per_project * 1.5
        elif "event" in row["project_type"]:
            return average_funding_per_project * 0.3
        else:
            return average_funding_per_project * 1.0

    df_tpf["estimated_funding_amount"] = df_tpf.apply(assign_funding, axis=1)

    return df_tpf


# Filterung der Projekte auf den Zeitraum 2015-2025
mask = (
    (df_tpf_raw["start_date"].dt.year >= 2015)
    & (df_tpf_raw["end_date"].dt.year >= 2015)
    & (df_tpf_raw["end_date"].dt.year <= 2025)
)
df_tpf_filtered = df_tpf_raw[mask].copy()

print(
    f"Anzahl Datensätze des nach den Jahresangaben gefilterten Df: {len(df_tpf_filtered)}.\n"
)

# F Funktionsuafruf
df_tpf_filtered = estimated_project_funding(df_tpf_filtered)

# Check der geschätzten Drittmittelvolumina in Summe
print(
    f"Summe der geschätzten Drittmittelvolumina insgesamt: {round(df_tpf_filtered['estimated_funding_amount'].sum(), 0):.0f} €.\n"
)

# Drittmittelvolumina pro PI erstellen

print(df_tpf_filtered.columns)

print(
    df_tpf_filtered.groupby("nachname")["estimated_funding_amount"]
    .sum()
    .sort_values(ascending=False)
)

# Zuschreibung an den Dataframe
df_pi = pd.read_csv(
    r"C:\Users\felix\OneDrive\Desktop\masterarbeit\01_data\01_csv_data\00_pi_basics\Archiv\FINALLY_ALL_pi_data.csv",
    encoding="utf-8",
)
print(df_pi.columns)

df_tpf_sums = (
    df_tpf_filtered.groupby("nachname")["estimated_funding_amount"]
    .sum()
    .sort_values(ascending=False)
)

# Zuschreibung der neuen Werte
df_pi["estimated_total_third_party_funding"] = df_pi["nachname"].map(df_tpf_sums)
print(
    df_pi[
        ["nachname", "drittmittel_volumen", "estimated_total_third_party_funding"]
    ].head(10)
)

# Datenverarbeitung abschließen
df_pi["estimated_total_third_party_funding"].fillna(0, inplace=True)
df_pi.drop(columns=["drittmittel_volumen"], inplace=True)
df_pi.rename(
    columns={"estimated_total_third_party_funding": "drittmittel_volumen"}, inplace=True
)

# Daten speichern
df_pi.to_csv(
    rf"{data_dir_tpf}/00_pi_basics/FINALLY_ALL_pi_data.csv",
    index=False,
    encoding="utf-8",
)
df_pi.to_excel(
    rf"{data_dir_tpf}/00_pi_basics/FINALLY_ALL_pi_data.xlsx",
    index=False,
    engine="openpyxl",
)

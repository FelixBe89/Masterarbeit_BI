# Dieses Skript anonymisiert die persönlichen Angaben der PIs für die Verwendung der Daten im Code
# (Quelle: https://www.peterbe.com/plog/best-hashing-function-in-python)

import pandas as pd
import base64
import hashlib
from pathlib import Path


# Diese Funktion wurde mit Hilfe von Copilot komplettiert [KI]
def name_hashing(name: str) -> str:
    """
    Diese Funktion hasht einen String und erstellt einen anderen.

    Args:
        name (str): _description_

    Returns:
        str: _description_
    """

    # h = hashlib.md5(name.encode("utf-8"))

    # return h.digest().encode("base64").decode("utf-8").rstrip("=\n")[:5]

    h = hashlib.md5(name.encode("utf-8"))

    return base64.b64encode(h.digest()).decode("utf-8").rstrip("=\n")[:5]


# Funktion auf die Namen der PIs anwenden und in einer neuen Spalte sowie einem Dict speichern

# Einlesen der Datei
base_dir = Path.cwd().parent
data_dir = base_dir / "01_data" / "01_csv_data" / "00_pi_basics"

df_pi = pd.read_csv(f"{data_dir}/FINALLY_ALL_pi_data.csv", encoding="utf-8")

# Hashing der Namen
df_pi["pi_name_hashed"] = df_pi["nachname"].apply(name_hashing)

# Check
print(df_pi[["nachname", "pi_name_hashed"]].head(3))
print(
    f"Vergleich auf Duplikate:\nAnzahl eindeutiger Hashes: {df_pi['pi_name_hashed'].nunique()}."
    f"\nAnzahl der ursprünglichen Namen: {df_pi['nachname'].nunique()}."
)

# %%
# Speichern der Hashes in den Dataframe

df_pi.to_csv(f"{data_dir}/FINALLY_ALL_pi_data.csv", index=False, encoding="utf-8")
df_pi.to_excel(f"{data_dir}/FINALLY_ALL_pi_data.xlsx", index=False, engine="openpyxl")

# Speichern der Hashes in einem Dict
hashes_dict = dict(zip(df_pi["nachname"], df_pi["pi_name_hashed"]))
print(hashes_dict)

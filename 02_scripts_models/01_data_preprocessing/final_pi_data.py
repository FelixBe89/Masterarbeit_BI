# Skript, um die PI-Daten in einem ersten Schritt zusammenzuführen 
# Es gibt auch noch eine zweite Datei, die das mit den S2-Daten macht! 

import pandas as pd 
import openpyxl

# Logging Module einbinden 
import logging

logging.basicConfig(
    level=logging.INFO,  # ERROR?
    format='%(asctime)s - [%(filename)s] - %(levelname)s - %(message)s', 
    datefmt='%d-%m-%Y %H:%M:%S', 
    filename='logbuch.log', 
    filemode='a', # 'a' = append (anhängen), 'w' = write immer neu
    encoding='utf-8'
)

path1=r"/project/01_data/list_of_project_pis.xlsx"

path2=r"/project/01_data/01_csv_data/00_pi_basics/00_pi_final.csv"

try:
    df1=pd.read_excel(path1, engine="openpyxl")

    df2=pd.read_csv(path2, sep=";", encoding="utf-8")

except FileNotFoundError as f: 
    logging.error("Fehler {}".format(f))

# Daten zusammenführen in finalem Frame 
 
df1.drop_duplicates(subset="vorname from_file", inplace=True)

df1 = df1[["vorname", "nachname", "vorname from_file", "start_date", "end_date"]]

df2 = df2[["pi_id", "nach_und_vorname", "scholar_id"]]

df3 = pd.merge(df2, df1, how="left", left_on="nach_und_vorname", right_on="vorname from_file")

df3 = df3[["pi_id", "nach_und_vorname", "scholar_id", "vorname", "nachname", "start_date", "end_date"]]

df3.astype({"pi_id": "int64", "nach_und_vorname": "str", 
            "scholar_id": "str", "vorname": "str", 
            "nachname": "str", "start_date": "datetime64[ns]", 
            "end_date": "object"})

print(df3.info())

df3.to_csv(r"/project/01_data/01_csv_data/00_pi_basics/01_pi_final_final.csv")
logging.info("Die finalen Stammdaten der PIs wurden gespeichert!")


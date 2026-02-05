# Masterarbeit: 

Dieses Repo enthält die Codebasis der Masterarbeit im Bereich Business Intelligence Solutions auf der Basis von Forschungsdaten -- die Daten und die Auswertungen sind hier nicht zu finden (s.u. "Daten").  

> Ziel der Arbeit war die Analyse von Publikations- und Drittmitteldaten zur Gewinnung von faktenbasierten Informationen für strategische Entscheidungssituationen in der Forschungssteuerung. Dazu wurden eine _explorative factor analysis_, ein _topic modeling_ und eine Netzwerkanalyse durchgeführt. Die Ergebnisse der Analysen umfassen (i) einen Faktorscore, der Publikations- und Drittmittelpotentiale identifiziert, (ii) über einen Zeitraum von 10 Jahren (2015-2025) gebildete Themencluster (statisch und dynamisch) sowie Themenclusterzuordnungen für die jeweiligen Wissenschaftler:innen und (iii) eine Darstellung von Kollaborationsstrukturen im Fachbereich.


## Der Aufbau des Repos 

```
- Skripte                            # Code für die Datenakquise und (kleinere) Hilfsfunktionen 
--- 0_data_scraping
----- PubMed_Scraping.py             # Zieht die Daten von PubMed
----- S2_Author_Scraping.py          # Zieht die Daten von Semantic Scholar 
----- S2_Pubs_Scraping               # s.o. 
----- SerpAPI.py                     # Zieht die Daten über SerpAPI von Google Scholar
- 01_data_preprocessing
--- final_evaluation_per_pi.py          # Erstellt die finale Auswertungsübersicht aller Analysen 
--- final_pi_data.py                    # Erstellt den finalen Dataframe zu den PIs 
--- hashing_for_anonymous_pis.py        # Hashed die Namen
--- pi_estimation_funding_amounts.py    # Schätzt die Drittmittelvolumina 
--- s2_date_range.py                    # Bearbeitet die Datumsangaben in den Semantic Scholar Daten 
- Notebooks                             # Hier sind alle wesentlichen Analyseschritte in je einem Notebook enthalten
--- full_explorative_data_analysis.ipynb        
--- explorative_factor_analysis.ipynb
--- topic_modeling_publications.ipynb
--- topic_modeling_third_party_funding.ipynb
--- network_modeling.ipynb
- pyproject.toml                            # Übersicht aller Python-Packages des Projektes
- uv.lock                                   # Hilfsdatei der Versionen für Reproduzierbarkeit 
- README.md                                 # Einführung in das Projekt
```

## Hinweise zur Installation 

Das Projekt verwendet den Paketmanager [uv](https://github.com/astral-sh/uv), der über den Befehl 

```bash
pip install uv
```
installiert werden kann. Danach sollte man das Projekt klonen und, gemäß der uv-Dokumentation, synchronisieren: 

```bash
git clone NAME

cd repo_folder

uv sync
```

Dabei stellt die uv.lock-Datei sicher, dass die gleichen Versionen durchgehend verwendet werden. 

## Daten und Auswertungen

Die der Masterarbeit zugrundeliegenden **Daten** sind nicht Teil dieses Repos. Da diese zwar öffentlch sind, aber dennoch personenbezogene Angaben enthalten, sind sie nur über einen passwortgeschützten Bereich in der Cloud der Uni Münster (Sciebo) erreichbar und auf dem elektronischen Datenträger. Angaben dazu stehen in der Masterarbeit selbst. 
Die Auswertungen sind ebenfalls in der Masterarbeit enthalten und auf dem elektronischen Datenträger zu finden.  

## Erwartete Projektordnerstruktur 

Die lokale Struktur der Projektordner sollte, damit der Code reibungslos laufen kann, wie folgt sein: 

```
- masterarbeit
--- 01_data
----- 01_csv_data
------- 00_pi_basics
------- 01_publications 
------- 98_s2
------- 99_pubmed
----- 03_topic_modeling
------- 01_embeddings
------- 02_topic_results
------- 03_topic_visuals
------- 04_grid_search 
------- 05_models 
----- 04_efa
----- 05_network 
----- 06_full_eda
--- 02_scripts_models
----- 0_data_scraping
----- 01_data_preprocessing 
--- 03_notebooks
--- .gitignore
```

## Ergebnisse 

Die Ergebnisse sind in ihrer graphischen und tabellarischen Form im Anhang der Masterarbeit zu finden. Bei Ausführung des Codes werden die Ergebnisse lokal in den jeweiligen Auswertungsordnern gespeichert. 

## Kontakt

Bei Fragen oder Anmerkungen freue ich mich über eine Nachricht! 

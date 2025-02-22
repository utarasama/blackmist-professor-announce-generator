import pandas as pd
from pandas import DataFrame
from datetime import datetime
from fastapi import FastAPI, HTTPException
from enum import Enum
from dotenv import load_dotenv
from os import getenv


app = FastAPI()
load_dotenv()
MAINTENANCE = getenv("MAINTENANCE")


def get_planning_from_dataframe(data: DataFrame, columns: tuple[str], jour: str, trimestre) -> str:
    # Récupération de la date du jour
    courses: str = ""
    présence: str = "Obligatoire"
    if trimestre == 3:
        présence = "Rattrapage"
    elif jour.lower() == 'samedi':
        présence = 'Optionnel'

    index_col_to_check: int = None
    index_first_col: int = data.columns.get_loc(columns[0])
    for col_index in range(index_first_col + 1, index_first_col + 9):
        if str(data.iloc[2, col_index]).lower() == jour.lower():
            index_col_to_check = col_index
            break
    reduced_data = data.iloc[:, [index_first_col, index_col_to_check]]
    for course_line in range(4, 21, 4):
        if reduced_data.iloc[course_line, 1] != "COURS":
            horaire: str = str(reduced_data.iloc[course_line, 0]).replace('\n', " ")
            courses += f"- {horaire}"
            courses += '\n'
            courses += f'{reduced_data.iloc[course_line, 1]} | Pr. {reduced_data.iloc[course_line + 2, 1]}'
            courses += '\n'
            salle = reduced_data.iloc[course_line + 3, 1]
            if salle != salle: # Les NaN sont différents de toutes les valeurs, y compris eux-mêmes
                salle = ''
            courses += reduced_data.iloc[course_line + 1, 1]
            if salle != '':
                courses += f' - {salle}'
            courses += f' | {présence}'
            courses += '\n'
    return courses

@app.get("/blackmist/get_courses_announce",
         summary="Générer l'annonce des cours",
         tags=["Black Mist RP"],
         response_description="Un texte en Markdown prêt à être envoyé sur Discord")
def get_prof_announce(trimestre: int, jour: str):
    if MAINTENANCE == "true":
        raise HTTPException(status_code=503, detail="Désolé l'équipe mais flemme de me réorganiser pour le moment.")
    jours_de_cours: list[str] = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    if jour.lower() not in jours_de_cours:
        raise HTTPException(status_code=422, detail='Le jour de la semaine entré est incorrect.')
    planning_urls: dict[str, str] = { 
        "1e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=1894291823&single=true&output=csv",
        "2e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=2135775316&single=true&output=csv",
        "3e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=1753681858&single=true&output=csv",
        "4e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=1231779423&single=true&output=csv",
        "5e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=1145597278&single=true&output=csv"
    }
    columns_per_trimestre: dict = {
        1: ("Unnamed: 0", "Unnamed: 7"),
        2: ("Unnamed: 9", "Unnamed: 16"),
        3: ("Unnamed: 19", "Unnamed: 26")
    }
    complete_announce: str = f'# 📅 Cours du {datetime.now().strftime("%d/%m")}'
    complete_announce += '\n'
    for year, planning_url in planning_urls.items():
        data = pd.read_csv(planning_url)
        ## Fix d'un bug dont j'ignore la nature qui change le nom de la 1e colonne du CSV de 2e année
        if year == "2e année":
            columns_per_trimestre[1] = ('v', 'Unnamed: 7')
        else:
            columns_per_trimestre[1] = ('Unnamed: 0', 'Unnamed: 7')
        planning: str = get_planning_from_dataframe(data, columns_per_trimestre[trimestre], jour, trimestre)
        complete_announce += f'## {year}'
        complete_announce += '\n'
        complete_announce += planning
    complete_announce += '|| <@&1278414481785098340> ||'
    return {"announce": complete_announce}


"""
if __name__ == "__main__":
    print(get_prof_announce(trimestre=1, jour="vendredi"))
"""

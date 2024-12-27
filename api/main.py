import pandas as pd
from pandas import DataFrame
from datetime import datetime
from fastapi import FastAPI
from enum import Enum
from models.blackmist.course import Cours


class TrimestreEnum(int, Enum):
    trimestre1 = 1
    trimestre2 = 2
    trimestre3 = 3


class JourEnum(str, Enum):
    MONDAY = "LUNDI"
    TUESDAY = "MARDI"
    WEDNESDAY = "MERCREDI"
    THURSDAY = "JEUDI"
    #FRIDAY = "VENDREDI"
    SATURDAY = "SAMEDI"
    #SUNDAY = "DIMANCHE"


app = FastAPI()


def get_planning_from_dataframe(data: DataFrame, columns: tuple[str, str], jour: JourEnum) -> list[Cours]:
    # Récupération de la date du jour
    #courses: str = ""
    liste_de_cours = list()
    index_col_to_check: int = 0
    index_first_col = data.columns.get_loc(columns[0])
    for col_index in range(index_first_col + 1, index_first_col + 9):
        if data.iloc[2, col_index] == jour.value:
            index_col_to_check = col_index
            break
    reduced_data = data.iloc[:, [index_first_col, index_col_to_check]]
    for course_line in range(4, 21, 4):
        if reduced_data.iloc[course_line, 1] != "COURS":
            horaire: str = str(reduced_data.iloc[course_line, 0]).replace('\n', " ")
            matière: str = reduced_data.iloc[course_line, 1]
            professeur: str = f'Pr. {reduced_data.iloc[course_line + 2, 1]}'
            batiment: str = reduced_data.iloc[course_line + 1, 1]
            salle: str = reduced_data.iloc[course_line + 3, 1]
            cours: Cours = Cours(horaire, matière, professeur, batiment, salle)
            liste_de_cours.append(cours)
    return liste_de_cours

@app.get("/blackmist/get_courses_announce",
         summary="Générer l'annonce des cours",
         tags=["Black Mist RP"],
         response_description="Un objet JSON détaillant tous les cours de la soirée")
def get_prof_announce(trimestre: TrimestreEnum, jour: JourEnum) -> dict:
    planning_urls: dict[str, str] = { 
        "1e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?output=csv",
        "2e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=2135775316&single=true&output=csv",
        "3e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=1753681858&single=true&output=csv",
    }
    columns_per_trimestre: dict = {
        1: ("Unnamed: 0", "Unnamed: 7"),
        2: ("Unnamed: 9", "Unnamed: 16"),
        3: ("Unnamed: 19", "Unnamed: 26")
    }
    complete_announce: dict = {"title": f'# 📅 Cours du {datetime.now().strftime("%d/%m")}'}
    all_courses: list[dict] = list()
    for year, planning_url in planning_urls.items():
        data = pd.read_csv(planning_url)
        planning: list[Cours] = get_planning_from_dataframe(data, columns_per_trimestre[trimestre.value], jour)
        courses_for_year = {
            "title": f'## {year}',
            "courses": planning
        }
        all_courses.append(courses_for_year)
    complete_announce['planning'] = all_courses
    return complete_announce

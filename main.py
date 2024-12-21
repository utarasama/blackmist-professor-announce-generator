import pandas as pd
from pandas import DataFrame
from datetime import datetime
import locale
import pyperclip


def input_trimestre() -> int:
    trimestre: int = 0
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"
    while trimestre == 0:
        try:
            trimestre = int(input("Trimestre en cours (1, 2, 3) : "))
            if trimestre < 0 or trimestre > 3:
                trimestre = 0
                print(f"{RED}La valeur entrée n'est pas comprise entre 1 et 3. Veuillez réessayer.{RESET}")
            else:
                print(f"{BLUE}Traitement du planning du trimestre {trimestre} en cours...{RESET}")
                return trimestre
        except ValueError:
            print(f"{RED}La valeur entrée n'est pas un nombre. Veuillez réessayer.{RESET}")

def get_planning_from_dataframe(data: DataFrame, columns: tuple[str]) -> str:
    # Récupération de la date du jour
    courses: str = ""
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    today: str = datetime.now().strftime("%A").upper()  # "LUNDI", "MARDI", etc. en français

    index_col_to_check: int = None
    index_first_col: int = data.columns.get_loc(columns[0])
    for col_index in range(index_first_col + 1, index_first_col + 9):
        if data.iloc[2, col_index] == today:
            index_col_to_check = col_index
            break
    reduced_data = data.iloc[:, [index_first_col, index_col_to_check]]
    for course_line in range(4, 21, 4):
        if reduced_data.iloc[course_line, 1] != "COURS":
            courses += f"- {str(reduced_data.iloc[course_line, 0]).replace("\n", " ")}" \
                    f"\n{reduced_data.iloc[course_line, 1]} | Pr. {reduced_data.iloc[course_line + 2, 1]}" \
                    f"\n{reduced_data.iloc[course_line + 1, 1]} - {reduced_data.iloc[course_line + 3, 1]} | Obligatoire\n\n"
    return courses

def main():
    planning_urls: dict[str, str] = { 
        "1e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?output=csv",
        "2e année": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSj_SKPhUacbANqBmPyJp2f9Rq7J7vtqzx5vvVfKOkTl3IUbBjBrrucgiktiFu1pLoudDPG4PwqsR-j/pub?gid=2135775316&single=true&output=csv",
    }
    trimestre: int = input_trimestre()
    columns_per_trimestre: dict = {
        1: ("Unnamed: 0", "Unnamed: 7"),
        2: ("Unnamed: 9", "Unnamed: 16"),
        3: ("Unnamed: 19", "Unnamed: 26")
    }
    GREEN = "\033[32m"
    RESET = "\033[0m"
    complete_announce: str = f"# 📅 Cours du {datetime.now().strftime("%d/%m")}\n"
    for year, planning_url in planning_urls.items():
        data = pd.read_csv(planning_url)
        planning: str = get_planning_from_dataframe(data, columns_per_trimestre[trimestre])
        complete_announce += f"## {year}\n{planning}\n"
    pyperclip.copy(complete_announce)
    print(complete_announce, f"{GREEN}Texte copié dans le presse-papier.{RESET}", sep="\n")


if __name__ == "__main__":
    main()

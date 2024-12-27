from dataclasses import dataclass


@dataclass(slots=True)
class Cours:
    horaire: str
    matière: str
    professeur: str
    batiment: str
    salle: str
    présence: str = "Obligaoire"

    def __str__(self):
        cours: str = f"- {self.horaire}"
        cours += "\n"
        cours += f"{self.matière} | {self.professeur}"
        cours += "\n"
        cours += f"{self.batiment} - {self.salle} | {self.présence}"
        cours += "\n"


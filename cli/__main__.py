from .utils import display
from .managers import students, books, loans

actions = [
    "Ajouter un élève",
    "Supprimer un élève",
    "Ajouter un livre",
    "Suprimer un livre",
    "Vérifier un élève",
    "Ajouter un emprumt",
    "Retour d'un livre",
    "Quitter",
]

stop = 0
def main():
    choix = display.menu("Choisissez une option : ", actions)
    if choix == 1:
        students.main("add")
    elif choix == 2:
        students.main("delete")
    elif choix == 3:
        books.main("add")
    elif choix == 4:
        books.main("delete")
    elif choix == 5:
        students.main("verify")
    elif choix == 6:
        loans.main("add")
    elif choix == 7:
        loans.main("return")
    elif choix == 8:
        return 1

while not stop:
    stop = main()
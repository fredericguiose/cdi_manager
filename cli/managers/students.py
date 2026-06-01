from api.routes import students
from cli.utils import display
from typing import Literal
from data.models import MODELS
from data.schemas import students as students_db
from data.utils.types import string_to_type
from data.schemas import loans as loans_db
from data.schemas import books as books_db

MODEL = MODELS["STUDENTS"]
NAME_PRIMARY = list(MODEL.keys())[0]

def add_student():
    """Form : Add a student
    """
    display.title("Ajouter un élève")
    display.header("Rentrez les informations concernant l'élève :")
    first_name = input("Entrez le prénom de l'élève : ")
    last_name = input("Entrez le nom de l'élève : ")
    if not first_name or not last_name:
        display.error("Le prénom et le nom sont obligatoires.")
        return
    entries = students_db.create([{"first_name": first_name, "last_name": last_name}])
    if not entries:
        display.error("Impossible d'ajouter l'élève.")
    else:
        student = entries[0]
        display.success(f"Elève {student['first_name']} {student['last_name']} ajouté avec succès")
    display.separator()
    display.pause()


def delete_student():
    """Form delete a student
    """
    display.title("Supprimer un élève")
    student_to_delete = string_to_type(typ=MODEL[NAME_PRIMARY],value=input("ID de l'élève à supprimer : ")) # Convert the type
    if student_to_delete:
        drows = students_db.delete({NAME_PRIMARY:student_to_delete})
    else:
        display.error("Une erreur s'est produite")
    if len(drows) == 1:
        student_deleted = drows[0]
        display.success(f"Elève {student_deleted["first_name"]} {student_deleted["last_name"]} supprimé avec succès")
    elif len(drows) == 0:
        display.error(f"L'élève avec l'id {student_deleted} n'existe pas")
    else:
        display.error(f"L'élève avec l'id {student_to_delete} à été trouvé plusieurs fois ils ont tous été supprimer :")
        display.table(["id","Prénom","Nom"],[list(drow.values()) for drow in drows])
    display.separator()
    display.pause()

def verify_student():
    """Verify the loans of a student and the state
    """
    display.header("Vérifier un élève")
    student_id = string_to_type(typ=MODEL[NAME_PRIMARY],value=input("Entre l'id : "))
    loans = loans_db.get(query={"student_id":student_id})
    loans_primary_key = list(MODELS["LOANS"].keys())[0]
    if len(loans) == 0:
        display.error("L'élève n'a pas de livres emprutés ou n'as pas été trouver")
        display.pause()
        return
    rows = []
    for loan in loans:
        students = students_db.get(primary_key_value=loan["student_id"])
        books = books_db.get(primary_key_value=loan["isbn"])
        row = [
            loan[loans_primary_key],
            students[0]["first_name"] if students else loan["student_id"],
            books[0]["title"] if books else loan["isbn"],
            "Oui" if loan["status"] else "Non",
        ]
        rows.append(row)
    display.table(["id", "Prénom", "Titre du livre", "Disponible"], rows)
    display.pause()



def main(action: Literal["add", "delete", "verify"]):
    display.clear()
    if action == "add":
        return add_student()
    elif action == "delete":
        return delete_student()
    elif action == "verify":
        return verify_student()

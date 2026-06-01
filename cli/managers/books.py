from typing import Literal
from cli.utils import display
from data.models import MODELS
from data.schemas import books
from data.utils.types import string_to_type

MODEL = MODELS["BOOKS"]
NAME_PRIMARY = list(MODEL.keys())[0]

def add_book():
    """Form add a book
    """
    display.title("Ajouter un livre")
    display.header("Rentrez les informations concernant le livre :")
    isbn = string_to_type(MODEL[NAME_PRIMARY], input("ISBN : "))
    title = string_to_type(MODEL["title"], input("Titre : "))
    author = string_to_type(MODEL["author"],input("Auteur : "))
    year_published = string_to_type(MODEL["year_published"], input("Année de publication : "))
    if not isbn or not title or not author or not year_published:
        display.error("Tous doivent être correctemment remplies.")
        display.pause()
        return
    entries = books.create([{"isbn":isbn,"title":title, "author":author,"year_published":year_published,"status":True}])
    if not entries:
        display.error(f"Une erreur s'est produite")
    else:
        display.success(f"Livre {entries[0]["title"]} ajouté avec succès.")
    display.pause()

def delete_book():
    """Form delete a book
    """
    display.title("Supprimer un livre")
    book_to_delete = string_to_type(typ=MODEL[NAME_PRIMARY],value=input("ID du livre à supprimer : ")) # Convert the type
    if book_to_delete:
        drows = books.delete({NAME_PRIMARY:book_to_delete})
    else:
        display.error("Une erreur s'est produite")
    if len(drows) == 1:
        book_deleted = drows[0]
        display.success(f"Livre {book_deleted["title"]} {book_deleted["year_published"]} supprimé avec succès")
    elif len(drows) == 0:
        display.error(f"Le Livre avec l'id {book_deleted} n'existe pas")
    else:
        display.error(f"Livre avec l'id {book_to_delete} à été trouvé plusieurs fois ils ont tous été supprimer :")
        display.table(["Isbn","Titre","Auteur","Année de publication","Rendu"],[list(drow.values()) for drow in drows])
    display.separator()
    display.pause()



def main(action:Literal["add","delete"]):
    if action == "add":
        add_book()
    elif action == "delete":
        delete_book()


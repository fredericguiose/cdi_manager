from typing import Literal
from cli.utils import display
from data.models import MODELS
from data.schemas import books, loans, students
from data.utils.types import string_to_type

MODEL = MODELS["LOANS"]
NAME_PRIMARY = list(MODEL.keys())[0]

def add_loan():
    """Form add a loan"""
    display.title("Ajouter un emprumt")
    display.header("Rentrez les informations concernant l'emprumt :")
    student_id = string_to_type(MODELS["STUDENTS"][list(MODELS["STUDENTS"].keys())[0]], input("ID de l'étudiant : "))
    book_isbn = string_to_type(MODELS["BOOKS"][list(MODELS["BOOKS"].keys())[0]], input("ISBN du livre : "))
    if not student_id or not book_isbn:
        display.error("Tous doivent être correctement remplies.")
        display.pause()
        return
    
    query_students = students.get(primary_key_value=student_id)
    query_books = books.get(primary_key_value=book_isbn)
    if not query_students or not query_books:
        display.error("L'étudiant ou le livre n'as pas été trouver")
        display.pause()
        return
    student,book = query_students[0],query_books[0]
    # If the student have a loan or if a book are already taken by a other 
    query_student_id_loans = loans.get(query={"student_id": student_id,"status": False})
    query_book_isbn_loans = loans.get(query={"isbn": book_isbn,"status":False})
    if len(query_student_id_loans) > 0:
        display.error("L'élève à déjà emprunté")
        display.pause()
        return
    elif len(query_book_isbn_loans) > 0:
        display.error("Ce livre est déjà emprunté")
        display.pause()
        return

    # Recup for verify the condition
    query_book_student = loans.get(query={"isbn":book_isbn,"student_id": student_id,"status": False})

    entries = []
    # Update the status if the student aleready taken a time
    if len(query_book_student) > 0:
        entries = loans.update(query={}, new_data={"status":True},primary_key_value=query_book_student[0][NAME_PRIMARY])
    else:
        entries = loans.create([{"student_id": student_id, "isbn": book_isbn, "status": True}])
    if not entries:
        display.error("Une erreur s'est produite lors de la création de l'emprunt")
        display.pause()
        return
    books.update(query={}, new_data={"status":False}, primary_key_value=book_isbn)
    display.success(f"L'emprumt a été effectué avec succès, {student["first_name"]} peut prendre {book["title"]}.")

def return_loan():
    """Form return loan"""
    display.title("Retourner un emprunt")
    display.header("Rentrez les infos l'emprumt à retourner : ")
    isbn_book_loan_to_return = string_to_type(MODELS["BOOKS"][list(MODELS["BOOKS"].keys())[0]],input("L'isbn de du livre à retourner :"))
    if not isbn_book_loan_to_return:
        display.error("Le ISBN doit être correctement remplie")
        display.pause()
        return
    
    entries = loans.get({"isbn":isbn_book_loan_to_return,"status":False})
    if not entries:
        display.error(f"Le livre avec l'ISBN {isbn_book_loan_to_return} n'existe pas ou n'es pas emprumté.")
        display.pause()
        return
    loans.update(query={}, new_data={"status":True},primary_key_value=entries[0][list(MODELS["LOANS"].keys())[0]])
    display.success(f"L'emprunt du livre avec l'ISBN {isbn_book_loan_to_return} à retourné avec succès.")
    display.pause()

def main(action:Literal["add","return"]):
    if action == "add":
        add_loan()
    elif action == "return":
        return_loan()
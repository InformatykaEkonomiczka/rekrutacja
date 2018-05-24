#PLIK DO ZAPYTAŃ Z BAZY DANYCH
#NA RAZIE ZWRACA FEJKOWE DANE

import student
import qualification_calculator


def add_student(student, scores):
    #dodaje do bazy studenta z wynikami rekrutacyjnymi na każdym kierunku
    #obiekt klasy student ma dane: imie, nazwisko, pesel
    #
    print("DB ADD RECORD: " + student.get_name() + " " + student.get_pesel() + " " + str(scores))




# Przyklad uzycia
# odpalanie: python db_setter.py

# TO ZOSTANIE STWORZONE Z REJESTRACJI - student się rejestruje i wybiera od 1 do 3 kierunków
student1 = student.Student("Pawel", "Miry", "80091001334")
fields1 = ["economics", "computer_science"]
############################################################################################
scores = {}
for field in fields1:
    scores[field] = qualification_calculator.QualificationCalculator(student1.get_exam_results(), field).get_points()

add_student(student1, scores)

# inny z rejestracji
student2 = student.Student("Twoja", "Matka", "02271409862")
fields2 = ["computer_science", "economics", "management"]
############################################################################################
scores = {}
for field in fields2:
    scores[field] = qualification_calculator.QualificationCalculator(student2.get_exam_results(), field).get_points()

add_student(student2, scores)
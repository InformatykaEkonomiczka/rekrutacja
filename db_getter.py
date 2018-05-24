#PLIK DO ZAPYTAŃ Z BAZY DANYCH
#NA RAZIE ZWRACA FEJKOWE DANE

def get_students(field):
    #zapytanie do bazy danych o wszystkich studentów kierunku "field"
    #posortowanych według liczby punktów
    students = ["Franek", "Piotrek", "Maciek", "Zenek"] #tutaj zapytanie
    return students

def get_students_reserve(field):
    #zapytanie do bazy danych o wszystkich studentów, którzy nie są z kierunku "field"
    #a mają go w rezerwowych
    #(posortowanych według liczby punktów z kierunku "field" - jeśli się da, jeśli nie to trzeba użyć generatora
    students_reserve = ["Staszek", "Zbyszek"] #tutaj zapytanie
    return students_reserve
    
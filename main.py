from flask import Flask, render_template, request, send_from_directory
from flask_mysqldb import MySQL

import db_getter

import student
import qualification_calculator

app = Flask(__name__)
app.debug = True

#CONNECTION TO DB
app.config['MYSQL_HOST'] = 'www.db4free.net'
app.config['MYSQL_USER'] = 'baza_projekt'
app.config['MYSQL_PASSWORD'] = 'baza_projekt1'
app.config['MYSQL_DB'] = 'baza_projekt'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index1.html")

@app.route('/admin',methods=["GET"])
def admin():
    return render_template("admin1.html")

@app.route('/kontakt',methods=["GET"])
def kontakt():
    return render_template("kontakt1.html")

@app.route('/lista',methods=["GET"])
def lista():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nazwa FROM kierunek''')
    rv = cur.fetchall()

    #wybór kierunku w liscie rozwijanej
    # 1 - Zarządzanie
    # 2 - Ekonomia
    # 3 - Informatyka stosowana
    # default: rv(field=1)
    field = 1

    return render_template("lista1.html",
                            field=rv[field][0],
                            students=db_getter.get_students(field),
                            students_reserve=db_getter.get_students_reserve(field))

@app.route('/login',methods=["GET"])
def login():
    return render_template("login1.html")

@app.route('/login_post',methods=["POST"])
def login_post():
    login = request.form["login"]
    haslo = request.form["haslo"]
    print("Zalogowal sie: " + login + " haslo: " + haslo)
    return render_template("index1.html")

@app.route('/rejestracja',methods=["GET"])
def rejestracja():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nazwa FROM kierunek''')
    rv = cur.fetchall()
    fields = [field[0] for field in rv]
    print(fields)

    return render_template("rejestracja1.html", fields=fields)

@app.route('/rejestracja_post',methods=["POST"])
def rejestracja_post():
    pesel = request.form["pesel"]
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT pesel FROM kandydat''')
    rv = cur.fetchall()
    pesels = [pesel[0] for pesel in rv]
    if int(pesel) not in pesels:
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]

        field1 = request.form["field1"]
        field2 = request.form["field2"]
        field3 = request.form["field3"]

        x = student.Student(name,surname,pesel)
        
        cur.execute('''INSERT INTO `kandydat`(`pesel`, `imie`, `nazwisko`, `poziom dostepu`, `haslo`) VALUES (%s, %s, %s, %s, %s)''',
                                            (x.get_pesel(), x.get_name(), x.get_surname(), 1, password))

        field1_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field1)
        field2_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field2)
        field3_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field3)

        cur.execute('''INSERT INTO `kandydatWybory`(`pesel`, `kierunek1`, `wynik1`, `kierunek2`, `wynik2`, `kierunek3`, `wynik3`) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                            (x.get_pesel(), field1, field1_result.get_points(), field2, field2_result.get_points(), field3, field3_result.get_points()))

        mysql.connection.commit()
        print("Stworz usera: " + "HASLO: " + str(password) + "MAIL: " +str(email))
        print("User wybral kierunki: " + str(field1) + str(field2) + str(field3))
    else:
        print("JUZ JEST")
    
    return render_template("login1.html")

@app.route('/rekrutacja',methods=["GET"])
def rekrutacja():
    return render_template("rekrutacja1.html")

@app.route('/styles/<path:path>')
def send_js(path):
    return send_from_directory('styles', path)

if __name__ == '__main__':
    app.run()

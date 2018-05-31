# coding=utf-8
from flask import Flask, render_template, request, send_from_directory
from flask_mysqldb import MySQL

import db_getter

import student
import qualification_calculator

app = Flask(__name__)
app.debug = True

# CONNECTION TO DB
app.config['MYSQL_HOST'] = 'www.db4free.net'
app.config['MYSQL_USER'] = 'baza_projekt'
app.config['MYSQL_PASSWORD'] = 'baza_projekt1'
app.config['MYSQL_DB'] = 'baza_projekt'
mysql = MySQL(app)

# GLOBAL??
loggedin = False
pesel = 0


@app.route('/', methods=["GET"])
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM aktualnosci''')
    rv = cur.fetchall()
    return render_template("index1.html", news=reversed(rv), loggedin=loggedin)


@app.route('/kryteria', methods=["GET"])
def kryteria():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nazwa,liczba_miejsc,prog_punktowy,kryteria FROM kierunek''')
    fields = cur.fetchall()
    print(fields)
    return render_template("kryteria1.html", fields=fields, loggedin=loggedin)


@app.route('/kontakt', methods=["GET"])
def kontakt():
    print(loggedin)
    return render_template("kontakt1.html", loggedin=loggedin)


@app.route('/lista', methods=["GET"])
def lista():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nazwa FROM kierunek''')
    rv = cur.fetchall()

    # wybór kierunku w liscie rozwijanej
    # 1 - Zarządzanie
    # 2 - Ekonomia
    # 3 - Informatyka stosowana
    # default: rv(field=1)
    field = 1

    return render_template("lista1.html",
                           field=rv[field][0],
                           students=db_getter.get_students(field),
                           students_reserve=db_getter.get_students_reserve(field))


@app.route('/login', methods=["GET"])
def login():
    return render_template("login1.html", loggedin=loggedin)


@app.route('/login_post', methods=["POST"])
def login_post():
    login = request.form["login"]
    haslo = request.form["haslo"]
    # print("Zalogowal sie: " + login + " haslo: " + haslo)
    global loggedin
    loggedin = True
    global pesel
    pesel = login
    return render_template("login1.html", loggedin=loggedin)


@app.route('/logout', methods=["GET"])
def logout():
    global loggedin
    loggedin = False
    return render_template("login1.html", loggedin=loggedin)


@app.route('/rejestracja', methods=["GET"])
def rejestracja():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nazwa FROM kierunek''')
    rv = cur.fetchall()
    fields = [""] + [field[0] for field in rv]
    print(fields)

    return render_template("rejestracja1.html", fields=fields)


@app.route('/rejestracja_post', methods=["POST"])
def rejestracja_post():
    pesel = request.form["pesel"]
    errormsg = ""
    personal_data = ("", "")

    cur = mysql.connection.cursor()
    cur.execute('''SELECT pesel FROM kandydat''')
    rv = cur.fetchall()
    pesels = [pesel[0] for pesel in rv]
    if int(pesel) not in pesels:
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        #email = request.form["email"]

        field1 = request.form["field1"]
        field2 = request.form["field2"]
        field3 = request.form["field3"]

        x = student.Student(name, surname, pesel)
        #personal_data = (name, surname)

        if x.get_exam_results().get_pass_result():
            cur.execute('''INSERT INTO `kandydat`(`pesel`, `imie`, `nazwisko`, `poziom dostepu`, `haslo`) VALUES (%s, %s, %s, %s, %s)''',
                        (x.get_pesel(), x.get_name(), x.get_surname(), 1, password))

            cur.execute('''INSERT INTO `matura`(`pesel`, `Matematyka`, `Fizyka`, `Informatyka`, `Polski`, `Angielski`) VALUES (%s, %s, %s, %s, %s, %s)''',
                        (x.get_pesel(), x.get_exam_results().get_results()["maths"], x.get_exam_results().get_results()["physics"],
                        x.get_exam_results().get_results()["it"], x.get_exam_results().get_results()["polish"], x.get_exam_results().get_results()["english"]))

            field1_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field1).get_points() if field1 else 0
            field2_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field2).get_points() if field2 else 0
            field3_result = qualification_calculator.QualificationCalculator(x.get_exam_results(), field3).get_points() if field3 else 0

            cur.execute('''INSERT INTO `kandydatWybory`(`pesel`, `kierunek1`, `wynik1`, `kierunek2`, `wynik2`, `kierunek3`, `wynik3`) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (x.get_pesel(), field1, field1_result, field2, field2_result, field3, field3_result))

            mysql.connection.commit()
        else:
            errormsg = "Nie zdałeś matury! Nie zostajesz dopuszczony do studiów!"
    else:
        errormsg = "Użytkownik o identyfikatorze " + str(pesel) + " już istnieje!"

    return render_template("rejestracja1_post.html", loggedin=loggedin, errormsg=errormsg)


@app.route('/rekrutacja', methods=["GET"])
def rekrutacja():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT imie,nazwisko FROM kandydat WHERE pesel=%s''' % str(pesel))
    personal_data = cur.fetchall()[0]

    cur.execute('''SELECT Matematyka,Fizyka,Informatyka,Polski,Angielski FROM matura WHERE pesel=%s''' % str(pesel))
    points = cur.fetchall()[0]

    cur.execute('''SELECT kierunek1,wynik1,kierunek2,wynik2,kierunek3,wynik3 FROM kandydatWybory WHERE pesel=%s''' % str(pesel))
    fields = cur.fetchall()[0]

    return render_template("rekrutacja1.html", loggedin=loggedin, personal_data=personal_data, points=points, fields=fields)


@app.route('/aktualnosci',methods=["GET"])
def aktualnosci():
    return render_template("aktualnosci.html", loggedin=loggedin)

@app.route('/styles/<path:path>')
def send_js(path):
    return send_from_directory('styles', path)


if __name__ == '__main__':
    app.run()

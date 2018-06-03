# coding=utf-8
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_mysqldb import MySQL

import student
import qualification_calculator

import functions

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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", loggedin=loggedin)


@app.route('/aktualnosci', methods=["GET"])
def aktualnosci():
    news = functions.get_news(mysql.connection.cursor())
    return render_template("aktualnosci.html", news=news, loggedin=loggedin)


@app.route('/kryteria', methods=["GET"])
def kryteria():
    fields = functions.get_criteria(mysql.connection.cursor())
    return render_template("kryteria.html", fields=fields, loggedin=loggedin)


@app.route('/kontakt', methods=["GET"])
def kontakt():
    return render_template("kontakt.html", loggedin=loggedin)


@app.route('/lista/<field>', methods=["GET"])
def lista(field):
    fieldnr = int(field)+1
    all_fields = functions.get_all_fields(mysql.connection.cursor())
    students_data = functions.get_students_data(mysql.connection.cursor())
    field_data = functions.get_field_data(mysql.connection.cursor(), fieldnr)
    qualification_results = functions.get_qualification_results(
        mysql.connection.cursor())
    choices = functions.get_choices(qualification_results)
    allowed = functions.get_allowed(field_data, choices)
    students = functions.get_students_list(allowed, students_data)
    qualified_students = students[:field_data["limit"]]
    reserved_students = students[field_data["limit"]:]

    return render_template("lista.html",
                           ind=field,
                           field_data=field_data,
                           all_fields=all_fields,
                           qualified_students=qualified_students,
                           reserved_students=reserved_students,
                           loggedin=loggedin)


@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html", loggedin=loggedin)


@app.route('/login_post', methods=["POST"])
def login_post():
    login = request.form["login"]
    password = request.form["haslo"]
    if functions.check_password(login,password, mysql.connection.cursor()):
        global loggedin
        loggedin = True
        global pesel
        pesel = login
        personal_data = functions.get_personal_data(pesel, mysql.connection.cursor())
        return render_template("login.html", loggedin=loggedin, personal_data=personal_data)
    else:
        return render_template("login.html", loggedin=False)


@app.route('/logout', methods=["GET"])
def logout():
    global loggedin
    loggedin = False
    return render_template("login.html", loggedin=loggedin)


@app.route('/rejestracja', methods=["GET"])
def rejestracja():
    fields = functions.get_all_fields(mysql.connection.cursor())
    fields = [""] + [field[0] for field in fields]
    return render_template("rejestracja.html", fields=fields, loggedin=loggedin)


@app.route('/rejestracja_post', methods=["POST"])
def rejestracja_post():
    pesel = request.form["pesel"]
    errormsg = ""
    exists = functions.check_pesel_existance(pesel, mysql.connection.cursor())

    if not exists:
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]

        field1 = request.form["field1"]
        field2 = request.form["field2"]
        field3 = request.form["field3"]

        x = student.Student(name, surname, pesel)

        if x.get_exam_results().get_pass_result():
            functions.register_user(
                x, password, field1, field2, field3, email, mysql.connection.cursor())
            mysql.connection.commit()
        else:
            errormsg = "Nie zdałeś matury! Nie zostajesz dopuszczony do studiów!"
    else:
        errormsg = "Użytkownik o identyfikatorze " + \
            str(pesel) + " już istnieje!"

    return render_template("rejestracja_post.html", loggedin=loggedin, errormsg=errormsg)


@app.route('/rekrutacja', methods=["GET"])
def rekrutacja():
    personal_data = functions.get_personal_data(
        pesel, mysql.connection.cursor())
    points = functions.get_exam_points(pesel, mysql.connection.cursor())
    fields = functions.get_chosen_fields(pesel, mysql.connection.cursor())

    return render_template("rekrutacja.html", loggedin=loggedin, personal_data=personal_data, points=points, fields=fields)


@app.route('/edycja', methods=["GET"])
def edycja():
    (name,surname,email,password) = functions.get_full_user_data(pesel, mysql.connection.cursor())
    return render_template("edycja.html", loggedin=loggedin, pesel=pesel, password=password, name=name, surname=surname, email=email)


@app.route('/edycja_post', methods=["POST"])
def edycja_post():
    password = request.form["password"]
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]

    functions.change_user_data(pesel, name, surname, email, password, mysql.connection.cursor())
    mysql.connection.commit()

    return render_template("edycja_post.html", loggedin=loggedin)

@app.route('/styles/<path:path>')
def send_js(path):
    return send_from_directory('styles', path)


@app.route('/lista/styles/<path:path>')
def send_js1(path):
    return send_from_directory('styles', path)


if __name__ == '__main__':
    app.run()

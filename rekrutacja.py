from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index1.html",a="dupa")

@app.route('/admin',methods=["GET"])
def admin():
    return render_template("admin1.html")

@app.route('/kontakt',methods=["GET"])
def kontakt():
    return render_template("kontakt1.html")

@app.route('/lista',methods=["GET"])
def lista():
    return render_template("lista1.html")

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
    return render_template("rejestracja1.html")

@app.route('/rekrutacja',methods=["GET"])
def rekrutacja():
    return render_template("rekrutacja1.html")

@app.route('/styles/<path:path>')
def send_js(path):
    return send_from_directory('styles', path)

if __name__ == '__main__':
    app.run()

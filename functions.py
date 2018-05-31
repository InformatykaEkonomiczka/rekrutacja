import qualification_calculator


def get_news(cur):
    cur.execute('''SELECT * FROM aktualnosci''')
    news = cur.fetchall()
    return reversed(news)


def get_criteria(cur):
    cur.execute(
        '''SELECT nazwa,liczba_miejsc,prog_punktowy,kryteria FROM kierunek''')
    fields = cur.fetchall()
    return fields


def get_all_fields(cur):
    cur.execute('''SELECT nazwa FROM kierunek''')
    all_fields = cur.fetchall()
    return all_fields


def get_students_data(cur):
    cur.execute('''SELECT pesel,imie,nazwisko FROM kandydat''')
    students_records = cur.fetchall()

    students_data = {}
    for record in students_records:
        students_data[record[0]] = str(record[1] + " " + record[2])

    return students_data


def get_field_data(cur, fieldnr):
    cur.execute(
        '''SELECT nazwa,prog_punktowy,liczba_miejsc FROM kierunek WHERE id=%s''' % fieldnr)
    field_record = cur.fetchall()[0]
    field_data = {
        "name": field_record[0], "threshold": field_record[1], "limit": field_record[2]}

    return field_data


def get_qualification_results(cur):
    cur.execute(
        '''SELECT pesel,kierunek1,wynik1,kierunek2,wynik2,kierunek3,wynik3 FROM kandydatWybory''')
    qualification_results = cur.fetchall()

    return qualification_results


def get_choices(qualification_results):
    choices = {}
    for res in qualification_results:
        choices[res[0]] = {}
        if res[1]:
            choices[res[0]][res[1]] = res[2]
        if res[3]:
            choices[res[0]][res[3]] = res[4]
        if res[5]:
            choices[res[0]][res[5]] = res[6]

    return choices


def get_allowed(field_data, choices):
    allowed = {}
    for person in choices:
        if field_data["name"] in choices[person]:
            if choices[person][field_data["name"]] >= field_data["threshold"]:
                allowed.update({person: choices[person][field_data["name"]]})

    return allowed


def get_students_list(allowed, students_data):
    students = []
    for pesel, result in sorted(allowed.items(), key=lambda x: x[1], reverse=True):
        students.append((students_data[pesel], result))

    return students


def check_pesel_existance(pesel, cur):
    cur.execute('''SELECT pesel FROM kandydat''')
    rv = cur.fetchall()
    pesels = [pesel[0] for pesel in rv]
    if int(pesel) in pesels:
        return True
    else:
        return False


def register_user(x, password, field1, field2, field3, cur):
    cur.execute('''INSERT INTO `kandydat`(`pesel`, `imie`, `nazwisko`, `poziom dostepu`, `haslo`) VALUES (%s, %s, %s, %s, %s)''',
                (x.get_pesel(), x.get_name(), x.get_surname(), 1, password))

    cur.execute('''INSERT INTO `matura`(`pesel`, `Matematyka`, `Fizyka`, `Informatyka`, `Polski`, `Angielski`) VALUES (%s, %s, %s, %s, %s, %s)''',
                (x.get_pesel(), x.get_exam_results().get_results()["maths"], x.get_exam_results().get_results()["physics"],
                 x.get_exam_results().get_results()["it"], x.get_exam_results().get_results()["polish"], x.get_exam_results().get_results()["english"]))

    field1_result = qualification_calculator.QualificationCalculator(
        x.get_exam_results(), field1).get_points() if field1 else 0
    field2_result = qualification_calculator.QualificationCalculator(
        x.get_exam_results(), field2).get_points() if field2 else 0
    field3_result = qualification_calculator.QualificationCalculator(
        x.get_exam_results(), field3).get_points() if field3 else 0

    cur.execute('''INSERT INTO `kandydatWybory`(`pesel`, `kierunek1`, `wynik1`, `kierunek2`, `wynik2`, `kierunek3`, `wynik3`) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (x.get_pesel(), field1, field1_result, field2, field2_result, field3, field3_result))


def get_personal_data(pesel, cur):
    cur.execute(
        '''SELECT imie,nazwisko FROM kandydat WHERE pesel=%s''' % str(pesel))
    personal_data = cur.fetchall()[0]
    return personal_data


def get_exam_points(pesel, cur):
    cur.execute(
        '''SELECT Matematyka,Fizyka,Informatyka,Polski,Angielski FROM matura WHERE pesel=%s''' % str(pesel))
    points = cur.fetchall()[0]
    return points


def get_chosen_fields(pesel, cur):
    cur.execute(
        '''SELECT kierunek1,wynik1,kierunek2,wynik2,kierunek3,wynik3 FROM kandydatWybory WHERE pesel=%s''' % str(pesel))
    fields = cur.fetchall()[0]
    return fields

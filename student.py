import datetime
import exam_generator

class Student:
    def __init__(self, name, surname, pesel):
        self.name = surname + " " + name
        self.pesel = str(pesel)
        self.birthdate = self.__calculate_birthdate()
        self.age = self.__calculate_age()
        self.sex = self.__calculate_sex()
        self.exam_results = exam_generator.ExamGenerator(self)

    def __calculate_age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year
        if today.month < self.birthdate.month or today.month == self.birthdate.month and today.day < self.birthdate.day:
            age -= 1
        return age

    def __calculate_birthdate(self):
        year = int(self.pesel[0]) * 10 + int(self.pesel[1])
        month = int(self.pesel[2]) * 10 + int(self.pesel[3])
        day = int(self.pesel[4]) * 10 + int(self.pesel[5])
        if month > 12:
            month -= 20
            year += 2000
        else:
            year += 1900

        return datetime.date(day=day, month=month, year=year)

    def __calculate_sex(self):
        sex_digit = int(self.pesel[9])
        if sex_digit % 2:
            return "Male"
        else:
            return "Female"

    def get_name(self):
        return self.name

    def get_exam_results(self):
        return self.exam_results

    def __str__(self):
        return "Student: " + self.name + ", age: " + str(self.age) + ", sex: " + self.sex + "\n" + \
                "Exam results: " + str(self.exam_results) + \
                ("\nEXAMS FAILED!" if not self.exam_results.get_pass_result() else "")



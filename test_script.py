import student
import qualification_calculator

x = student.Student("Pawel", "Miry", "91081001334")
print(x)
res = qualification_calculator.QualificationCalculator(x.get_exam_results(), "Informatyka Stosowana")
print(res.get_points())
print(qualification_calculator.QualificationCalculator(x.get_exam_results(), "Informatyka Stosowana"))
print(qualification_calculator.QualificationCalculator(x.get_exam_results(), "Ekonomia"))
print(qualification_calculator.QualificationCalculator(x.get_exam_results(), "Zarzadzanie"))

print("#####################################################")

#y = student.Student("Twoja", "Matka", "02271409862")
#print(y)
#print(qualification_calculator.QualificationCalculator(y.get_exam_results(), "computer_science"))
#print(qualification_calculator.QualificationCalculator(y.get_exam_results(), "economics"))
#print(qualification_calculator.QualificationCalculator(y.get_exam_results(), "management"))

import random
import student

class ExamGenerator:
    def __init__(self, student):
        self.student = student
        self.student_avg = 0
        self.sigma = 10

        self.maths = 0
        self.physics = 0
        self.it = 0
        self.polish = 0
        self.english = 0

        self.__draw_avg()
        self.__generate_results()

    def __draw_avg(self):
        self.student_avg = int(random.uniform(30, 100))
        return self.student_avg

    def __generate_results(self):
        self.polish = self.__generate_result_subject()
        self.english = self.__generate_result_subject()
        self.maths = self.__generate_result_subject()
        self.physics = self.__generate_result_subject()
        self.it = self.__generate_result_subject()

    def __generate_result_subject(self):
        subject_result = int(random.gauss(self.student_avg, self.sigma))
        if subject_result < 0:
            return 0
        elif subject_result > 100:
            return 100
        else:
            return subject_result

    def get_pass_result(self):
        if self.polish < 30 or self.english < 30 or self.maths < 30:
            return False
        else:
            return True

    def get_results(self):
        results = \
            {
                "polish": self.polish,
                "english": self.english,
                "maths": self.maths,
                "physics": self.physics,
                "it": self.it
            }
        return results
        
    def __str__(self):
        return "Maths: " + str(self.maths) + \
               " Physics: " + str(self.physics) + \
               " IT: " + str(self.it) + \
               " Polish: " + str(self.polish) + \
               " English: " + str(self.english)
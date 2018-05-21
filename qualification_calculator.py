import exam_generator


class QualificationCalculator:
    def __init__(self, exam_results, field_of_study):
        self.exam_results = exam_results
        self.field_of_study = field_of_study

    def __calculate_qualification_result(self):
        if not self.exam_results.get_pass_result():
            return 0

        results = self.exam_results.get_results()

        if self.field_of_study == "management":
            return 4*results["english"] + results["polish"]
        elif self.field_of_study == "computer_science":
            science_better = max(results["physics"], results["it"])
            return 4*results["maths"] + science_better
        elif self.field_of_study == "economics":
            best_subjects = sorted(results.items(), key=lambda x: x[1], reverse=True)
            return 4*best_subjects[0][1] + best_subjects[1][1]

    def get_points(self):
        return self.__calculate_qualification_result()

    def __str__(self):
        return "Points in " + self.field_of_study + " : " + str(self.get_points())




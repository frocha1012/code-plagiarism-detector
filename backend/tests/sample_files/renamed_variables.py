def compute_mean_mark(marks):
    sum_of_marks = 0

    for mark in marks:
        sum_of_marks += mark

    mean_mark = sum_of_marks / len(marks)

    if mean_mark >= 50:
        return "pass"

    return "fail"


exam_marks = [72, 65, 81, 49]
outcome = compute_mean_mark(exam_marks)
print(outcome)

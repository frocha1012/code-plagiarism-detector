def calculate_average_grade(grades):
    total_score = 0

    for grade in grades:
        total_score += grade

    average_score = total_score / len(grades)

    if average_score >= 50:
        return "pass"

    return "fail"


student_grades = [72, 65, 81, 49]
result = calculate_average_grade(student_grades)
print(result)

def calculate_average(numbers):
    if not numbers:
        return 0

    total = 0
    for number in numbers:
        total += number

    return total / len(numbers)


def assign_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def add_student(records, student_id, name):
    if student_id not in records:
        records[student_id] = {
            "name": name,
            "grades": [],
            "attendance": [],
        }


def add_grade(records, student_id, subject, score):
    if student_id not in records:
        return False
    records[student_id]["grades"].append({"subject": subject, "score": score})
    return True


def mark_attendance(records, student_id, week, present):
    if student_id not in records:
        return False
    records[student_id]["attendance"].append({"week": week, "present": present})
    return True


def get_student_average(student):
    scores = []
    for grade in student["grades"]:
        scores.append(grade["score"])
    return calculate_average(scores)


def get_attendance_rate(student):
    if not student["attendance"]:
        return 0

    present_count = 0
    for entry in student["attendance"]:
        if entry["present"]:
            present_count += 1

    return present_count / len(student["attendance"])


def build_subject_summary(records):
    subjects = {}
    for student in records.values():
        for grade in student["grades"]:
            subject = grade["subject"]
            if subject not in subjects:
                subjects[subject] = []
            subjects[subject].append(grade["score"])

    summary = {}
    for subject, scores in subjects.items():
        summary[subject] = {
            "average": calculate_average(scores),
            "highest": max(scores),
            "lowest": min(scores),
        }
    return summary


def find_students_at_risk(records):
    at_risk = []
    for student_id, student in records.items():
        average = get_student_average(student)
        attendance = get_attendance_rate(student)
        if average < 60 or attendance < 0.75:
            at_risk.append({
                "id": student_id,
                "name": student["name"],
                "average": average,
                "attendance": attendance,
            })
    return at_risk


def print_student_report(records):
    print("STUDENT PERFORMANCE REPORT")
    print("-" * 45)
    for student_id, student in records.items():
        average = get_student_average(student)
        grade = assign_grade(average)
        attendance = get_attendance_rate(student)
        print(f"{student_id}: {student['name']}")
        print(f"Average Score: {average:.2f}")
        print(f"Final Grade: {grade}")
        print(f"Attendance Rate: {attendance:.0%}")
        print()


def print_subject_report(summary):
    print("SUBJECT SUMMARY")
    print("-" * 45)
    for subject, data in summary.items():
        print(subject)
        print(f"Average: {data['average']:.2f}")
        print(f"Highest: {data['highest']}")
        print(f"Lowest: {data['lowest']}")
        print()


def print_risk_report(students):
    print("STUDENTS AT RISK")
    print("-" * 45)
    if not students:
        print("No students currently at risk.")
        return
    for student in students:
        print(f"{student['name']} ({student['id']})")
        print(f"Average: {student['average']:.2f}")
        print(f"Attendance: {student['attendance']:.0%}")
        print()


def main():
    class_records = {}

    add_student(class_records, "S001", "Alice")
    add_student(class_records, "S002", "Ben")
    add_student(class_records, "S003", "Clara")
    add_student(class_records, "S004", "David")

    subjects = ["Math", "Programming", "Databases"]
    scores = {
        "S001": [88, 94, 81],
        "S002": [55, 62, 58],
        "S003": [74, 79, 83],
        "S004": [91, 86, 89],
    }

    for student_id, student_scores in scores.items():
        for index, score in enumerate(student_scores):
            add_grade(class_records, student_id, subjects[index], score)

    for week in range(1, 6):
        mark_attendance(class_records, "S001", week, True)
        mark_attendance(class_records, "S002", week, week < 4)
        mark_attendance(class_records, "S003", week, week != 2)
        mark_attendance(class_records, "S004", week, True)

    print_student_report(class_records)
    subject_summary = build_subject_summary(class_records)
    print_subject_report(subject_summary)
    risky_students = find_students_at_risk(class_records)
    print_risk_report(risky_students)


if __name__ == "__main__":
    main()

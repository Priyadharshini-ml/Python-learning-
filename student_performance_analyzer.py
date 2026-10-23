"""Student Performance Analyzer.

A command-line tool for analyzing student marks.
"""

from statistics import mean


def calculate_grade(average: float) -> str:
    """Return a grade based on the average mark."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    return "F"


def main() -> None:
    """Collect marks and display a performance report."""
    student_name = input("Enter student name: ").strip()

    if not student_name:
        print("Error: Student name cannot be empty.")
        return

    try:
        count = int(input("Number of subjects: "))

        if count <= 0:
            print("Error: Enter at least one subject.")
            return

        marks = []

        for index in range(count):
            mark = float(input(f"Enter mark for subject {index + 1}: "))

            if not 0 <= mark <= 100:
                print("Error: Marks must be between 0 and 100.")
                return

            marks.append(mark)

    except ValueError:
        print("Error: Please enter valid numeric values.")
        return

    average = mean(marks)
    highest = max(marks)
    lowest = min(marks)

    print("\n" + "=" * 35)
    print("      STUDENT PERFORMANCE REPORT")
    print("=" * 35)
    print(f"Student : {student_name}")
    print(f"Subjects: {count}")
    print(f"Average : {average:.2f}")
    print(f"Highest : {highest:.2f}")
    print(f"Lowest  : {lowest:.2f}")
    print(f"Grade   : {calculate_grade(average)}")
    print("=" * 35)


if __name__ == "__main__":
    main()
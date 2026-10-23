
from statistics import mean


def calculate_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def main():
    name = input("Student name: ").strip()

    if not name:
        print("Error: Name cannot be empty.")
        return

    try:
        count = int(input("Number of subjects: "))
        if count <= 0:
            print("Error: Enter a positive subject count.")
            return
    except ValueError:
        print("Error: Subject count must be a whole number.")
        return

    marks = []

    for i in range(count):
        try:
            mark = float(input(f"Mark for subject {i + 1}: "))
        except ValueError:
            print("Error: Enter a numeric mark.")
            return

        if not 0 <= mark <= 100:
            print("Error: Marks must be between 0 and 100.")
            return

        marks.append(mark)

    average = mean(marks)

    print("\n--- Student Performance Report ---")
    print(f"Student: {name}")
    print(f"Subjects: {count}")
    print(f"Average: {average:.2f}")
    print(f"Highest: {max(marks):.2f}")
    print(f"Lowest: {min(marks):.2f}")
    print(f"Grade: {calculate_grade(average)}")


if __name__ == "__main__":
    main()

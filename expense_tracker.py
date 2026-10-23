import csv
from pathlib import Path
from datetime import date

FILE = Path("expenses.csv")

def add_expense():
    category = input("Category: ").strip()

    try:
        amount = float(input("Amount (₹): "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Enter a valid amount.")
        return

    description = input("Description: ").strip()

    file_exists = FILE.exists()

    with FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                ["date", "category", "amount", "description"]
            )

        writer.writerow([
            date.today().isoformat(),
            category,
            amount,
            description,
        ])

    print("Expense saved successfully!")

def view_summary():
    if not FILE.exists():
        print("No expenses recorded yet.")
        return

    totals = {}

    with FILE.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            category = row["category"]
            totals[category] = (
                totals.get(category, 0) + float(row["amount"])
            )

    print("\n--- Expense Summary ---")
    for category, total in sorted(totals.items()):
        print(f"{category}: ₹{total:.2f}")

    print(f"Total spent: ₹{sum(totals.values()):.2f}")

def main():
    while True:
        print("\n1. Add expense")
        print("2. View summary")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
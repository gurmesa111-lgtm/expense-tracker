from datetime import datetime
from pathlib import Path
import json
#=============================================
#An expense tracker created by Gurmesa Borana
#=============================================
path = Path('expense.json')

if not path.exists():
    datas = []
else:
    try:
        datas = json.loads(path.read_text())

        if not isinstance(datas, list):
            raise ValueError("Expense data must be a list.")

        if not all(isinstance(data, dict) for data in datas):
            raise ValueError("Each expense must be a dictionary.")

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Cannot load {path}: {error}. "
            "Fix or restore the file before continuing."
        ) from error

categories = [
    'food', 'transport', 'housing',
    'utilities', 'shopping', 'entertainment',
    'health', 'education', 'others'
]

#Handles adding new expenses.
def add_expense():
    while True:
        expense_info = {}

        try:
            amount = float(input("\nEnter expense amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            print("Choose a category for your expense:")
            for i, category in enumerate(categories, start=1):
                print(f"\t{i}. {category.title()}")

            while True:
                try:
                    choose = int(input(f"Enter your choice(1-{len(categories)}): "))

                    if choose <= 0 or choose > len(categories):
                        print(f"Please enter a number between 1 and {len(categories)}")
                        continue

                    break
                except ValueError:
                    print("Please choose a category!")

            category = categories[choose - 1]

            while True:
                date = input("Enter date (YYYY-MM-DD): ")

                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date! Use YYYY-MM-DD format.")

            description = input("Enter description (optional): ").strip()

            if not category or not date:
                print("Category and date are required.")
                continue

            expense_info['amount'] = amount
            expense_info['category'] = category
            expense_info['date'] = date
            expense_info['description'] = description

            datas.append(expense_info)
            path.write_text(json.dumps(datas, indent=4))

        except ValueError:
            print("Please enter a valid numeric amount.")
            continue

        while True:
            ch = input("\nAre you done (y-for yes/n-for no): ").strip().lower()

            if ch == 'y':
                print("\n")
                return
            elif ch == 'n':
                break
            else:
                print("Enter y-for yes/n-for no!")

#Used to view the expenses stored in the file.
def view_expenses():
    if not datas:
        print("You don't have any expense information.")
    else:
        for num, data in enumerate(datas, start=1):
            print(f"\n{num})"
                  f"\tAmount: {data['amount']}")
            print(f"\tCategory: {data['category']}")
            print(f"\tDate: {data['date']}")
            print(f"\tDescription: {data['description']}")
        print("\n")

#Displays the sum of all the spending.
def total_spending():
    if not datas:
        print("You don't have an expense information.")
    else:
        total = 0
        for data in datas:
            total += data['amount']
        print(f"Total spending: {total:.2f}\n")

#Displays the total of expense under each and every category.
def spending_by_category():
        if not datas:
            print("No expenses recorded yet.")
            return

        category_totals = {}

        for data in datas:
            category = data['category']
            amount = data['amount']

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += amount

        for category, total in category_totals.items():
            print(f"\tCategory: {category.title()}")
            print(f"\tTotal spending: {total:.2f}\n")

#To remove/delete a stored expense from the file.
def delete_expense():
    if not datas:
        print("There is no expense to be deleted.\n")
        return

    view_expenses()

    while True:
        try:
            choice1 = int(input(
                "Which expense do you want to remove? (Enter a number): "
            ))

            if choice1 < 1 or choice1 > len(datas):
                print(f"Please enter a number between 1 and {len(datas)}.")
                continue

            break

        except ValueError:
            print("Invalid input! Please enter a number.")

    datas.pop(choice1 - 1)
    path.write_text(json.dumps(datas, indent=4))
    print("You have successfully removed the expense!\n")

#Lets the user make change to an existing expense information.
def edit_expense():
    if not datas:
        print("There are no expenses to edit.\n")
        return

    view_expenses()

    while True:
        try:
            choice3 = int(input("Which expense do you want to edit? "))

            if choice3 < 1 or choice3 > len(datas):
                print(f"Please enter a number between 1 and {len(datas)}.")
                continue

            break

        except ValueError:
            print("Invalid input! Please enter a number.")

    expense = datas[choice3 - 1]
    edited_expense = expense.copy()

    print("Press Enter to keep the current value.")

    while True:
        try:
            amount = input(f"Amount ({expense['amount']}): ")

            if amount:
                amount = float(amount)

                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue

                edited_expense['amount'] = amount

            break

        except ValueError:
            print("Please enter a valid amount.")

    print("\nCategories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.title()}")

    while True:
        category_choice = input(
            f"Category ({expense['category']}): "
        )

        if not category_choice:
            break

        if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
            edited_expense['category'] = categories[int(category_choice) - 1]
            break

        print(f"Please select a number between 1 and {len(categories)}.")

    while True:
        date = input(f"Enter date (YYYY-MM-DD) ({expense['date']}): ")

        if not date:
            break

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")
    if date:
        edited_expense['date'] = date

    description = input(
        f"Description ({expense['description']}): "
    )
    if description:
        edited_expense['description'] = description

    if edited_expense == expense:
        print("No changes were made.\n")
    else:
        datas[choice3 - 1] = edited_expense
        path.write_text(json.dumps(datas, indent=4))
        print("Expense updated successfully!\n")

#Lets the user choose an expense category and displays every data under that category.
def search_expenses():
    if not datas:
        print("There are no expenses to search.\n")
        return

    print("\nSearch an expense by a category:")
    for i, category in enumerate(categories, start=1):
        print(f"\t{i}. {category.title()}")

    while True:
        try:
            choice2 = int(input("Choose a category: "))

            if choice2 < 1 or choice2 > len(categories):
                print(f"Please choose a number between 1 and {len(categories)}.")
                continue

            break

        except ValueError:
            print("Invalid input! Please enter a number.")

    category = categories[choice2 - 1]
    found = False

    for i, data in enumerate(datas, start=1):
        if data['category'] == category:
            print(f"\nExpense #{i}")
            print(f"\tAmount: {data['amount']:.2f}")
            print(f"\tCategory: {data['category'].title()}")
            print(f"\tDate: {data['date']}")
            print(f"\tDescription: {data['description']}")
            found = True
    print("\n")

    if not found:
        print(f"No expenses found in {category.title()}.\n")

#Displays expenses within a particular range of date.
def filter_expenses_by_date():
    if not datas:
        print("There are no expenses to filter.\n")
        return

    while True:
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            end_date = input("Enter end date (YYYY-MM-DD): ")
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date > end_date:
                print("Start date cannot be later than end date.\n")
                continue

            break

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format and enter a valid date.\n")

    found = False

    for i, data in enumerate(datas, start=1):
        try:
            expense_date = datetime.strptime(
                data['date'], "%Y-%m-%d"
            ).date()
        except ValueError:
            continue

        if start_date <= expense_date <= end_date:
            print(f"\nExpense #{i}")
            print(f"\tAmount: {data['amount']:.2f}")
            print(f"\tCategory: {data['category'].title()}")
            print(f"\tDate: {data['date']}")
            print(f"\tDescription: {data['description']}")
            found = True
    print("\n")

    if not found:
        print("No expenses found within that date range.\n")

#A menu.
print("====== Expense Tracker ======")
while True:
    print("\t1. Add expense")
    print("\t2. View expenses")
    print("\t3. View total spending")
    print("\t4. View spending by category")
    print("\t5. Edit expense")
    print("\t6. Delete expense")
    print("\t7. Search expenses")
    print("\t8. Filter expenses by date")
    print("\t9. Quit")

    try:
        choice = int(input("Choose an option: "))
    except ValueError:
        print("Please choose one of the given options!")
        continue

    if choice == 1:
        add_expense()
    elif choice == 2:
        view_expenses()
    elif choice == 3:
        total_spending()
    elif choice == 4:
        spending_by_category()
    elif choice == 5:
        edit_expense()
    elif choice == 6:
        delete_expense()
    elif choice == 7:
        search_expenses()
    elif choice == 8:
        filter_expenses_by_date()
    elif choice == 9:
        print("Goodbye!")
        break
    else:
        print("Please choose only one of the given options!")
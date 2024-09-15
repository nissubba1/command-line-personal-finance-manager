from user_entry_manager import UserEntryManager
from csv_manager import CSVManager
from update_log_manager import UpdateLogManager
from report_manager import ReportManager
from ascii_art import print_ascii_art

def main():
    """
    Main function to run the transaction tracker system.

    Provides a menu for the user to perform various operations including:
        - Adding a new transaction
        - Viewing transactions and summary/trend within a date range
        - Modifying a transaction
        - Deleting a transaction
        - Viewing transactions and logs
        - Viewing summary balance
        - Viewing income and expense reports
        - Exiting the program

    Initializes the CSV files and provides a loop to handle user input and execute the corresponding functions.

    Returns:
        None
    """
    print("//////////////////// File Status ////////////////////")
    CSVManager.initialize_csv()
    print("//////////////////// End of Program ////////////////////")

    print_ascii_art()

    while True:
        print("\n1. Add a new transaction")
        print("2. View Transactions And Summary/Trend Within A Date Range")
        print("3. Modify A Transaction")
        print("4. Delete A Transaction")
        print("5. View Transactions And Logs")
        print("6. View Summary Balance")
        print("7. View Income Expense Report")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            UpdateLogManager.add()
        elif choice == "2":
            start_date = UserEntryManager.get_date("Enter the start date (mm-dd-yyyy): ")
            end_date = UserEntryManager.get_date("Enter the end date (mm-dd-yyyy): ")
            df = CSVManager.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                ReportManager.plot_transactions(df)
        elif choice == "3":
            UpdateLogManager.modify()
        elif choice == "4":
            UpdateLogManager.delete()
        elif choice == "5":
            ReportManager.view_logs()
        elif choice == "6":
            ReportManager.view_summary()
        elif choice == "7":
            ReportManager.view_income_expense_report()
        elif choice == "8":
            print("Exiting ....")
            break
        else:
            print("Invalid choice. Enter 1 - 8.")

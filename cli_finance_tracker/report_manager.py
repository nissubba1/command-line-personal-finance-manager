import pandas as pd
import matplotlib.pyplot as plt
from csv_manager import CSVManager


class ReportManager:
    """
    Manages the generation and viewing of various reports and logs.

    Methods:
        view_logs: Displays available log records for different types of logs.
        view_summary: Displays a summary of transactions including net amounts.
        plot_transactions: Plots income and expenses over time.
        view_income_expense_report: Generates and displays income or expense reports.
    """

    @staticmethod
    def view_logs():
        """
        Displays a menu for the user to select which log to view.

        Options include:
            - Transactions Log
            - New Entry Log
            - Update Log
            - Delete Log
            - Cancel

        Returns:
            None
        """
        while True:
            print("\nWhich log do you want to view: ")
            print("1. Transactions Log")
            print("2. New Entry Log")
            print("3. Update Log")
            print("4. Delete Log")
            print("5. Cancel")
            choice = input("Enter your choice: ")

            if choice == "1":
                CSVManager.view_records(0)
            elif choice == "2":
                CSVManager.view_records(1)
            elif choice == "3":
                CSVManager.view_records(3)
            elif choice == "4":
                CSVManager.view_records(2)
            elif choice == "5":
                print("Exiting ...")
                break
            else:
                print("Invalid choice please try again. Enter 1 - 5: ")

    @staticmethod
    def view_summary():
        """
        Displays a summary of transactions, including net amounts.

        Reads transaction data from the CSV file and generates a summary of income and expenses.

        Returns:
            None
        """
        df = pd.read_csv(CSVManager.CSV_FILES_DICT[0]["csv_file"])
        CSVManager.net_amount(df)

    @staticmethod
    def plot_transactions(df):
        """
        Plots income and expenses over time.

        Args:
            df (pandas.DataFrame): DataFrame containing transaction data with columns 'date', 'category', and 'amount'.

        Returns:
            None
        """
        df_grouped = df.groupby(["date", "category"])["amount"].sum().reset_index()
        df_grouped.set_index("date", inplace=True)
        plt.figure(figsize=(10, 6))

        plot_income_data = df_grouped[df_grouped["category"] == "Income"]
        plt.plot(plot_income_data.index, plot_income_data["amount"], "o-", label="Income", color="green")

        plot_expense_data = df_grouped[df_grouped["category"] == "Expense"]
        plt.plot(plot_expense_data.index, plot_expense_data["amount"], "o-", label="Expense", color="red")

        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expenses Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def view_income_expense_report():
        """
        Displays a menu for the user to select which income or expense report to view.

        Options include:
            - Income Report
            - Expense Report
            - Cancel

        Returns:
            None
        """
        while True:
            print("\nWhich report do you want to view: ")
            print("1. Income Report")
            print("2. Expense Report")
            print("3. Cancel")
            choice = input("Enter your choice (1 - 2): ")

            if choice == "1":
                CSVManager.expense_income_report("income")
            elif choice == "2":
                CSVManager.expense_income_report("expense")
            elif choice == "3":
                print("Exiting ...")
                break
            else:
                print("Invalid choice please try again. Enter 1 - 2")

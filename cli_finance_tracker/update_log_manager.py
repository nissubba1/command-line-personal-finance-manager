from user_entry_manager import UserEntryManager
from csv_manager import CSVManager


class UpdateLogManager:
    """
    Manages the addition, modification, and deletion of transaction records.

    Methods:
        add: Adds a new transaction entry.
        modify: Modifies an existing transaction entry.
        delete: Deletes a transaction entry.
    """

    @staticmethod
    def add():
        """
        Prompts the user to enter transaction details and adds a new entry to the CSV file.

        Gets the following details from the user:
            - Date of the transaction
            - Amount
            - Category
            - Description

        Returns:
            None
        """
        date = UserEntryManager.get_date("Enter the date of the transaction (mm-dd-yyyy) or enter for today's date: ",
                                         allow_default=True)
        amount = UserEntryManager.get_amount()
        category = UserEntryManager.get_category()
        description = UserEntryManager.get_description()
        CSVManager.add_entry(date, amount, category, description)

    @staticmethod
    def modify():
        """
        Modifies an existing transaction entry based on user input.

        The user can choose to modify:
            - Date
            - Category
            - Amount
            - Description
            - Or cancel the operation

        Returns:
            None
        """
        transaction_id = UserEntryManager.get_transaction_id()
        if CSVManager.verify_transaction_id(transaction_id):
            while True:
                print("\nWhich do you want to modify: ")
                print("1. Date")
                print("2. Category")
                print("3. Amount")
                print("4. Description")
                print("5. Cancel")
                choice = input("Enter your choice: ")
                if choice == "1":
                    new_date = UserEntryManager.get_date("Enter the new date (mm-dd-yyyy): ")
                    CSVManager.update_transactions(transaction_id, CSVManager.which_update_field(0), new_date)
                elif choice == "2":
                    new_category = UserEntryManager.get_category()
                    CSVManager.update_transactions(transaction_id, CSVManager.which_update_field(1), new_category)
                elif choice == "3":
                    new_amount = UserEntryManager.get_amount()
                    CSVManager.update_transactions(transaction_id, CSVManager.which_update_field(2), new_amount)
                elif choice == "4":
                    new_description = UserEntryManager.get_description()
                    CSVManager.update_transactions(transaction_id, CSVManager.which_update_field(3), new_description)
                elif choice == "5":
                    print("Exiting ... ")
                    break
                else:
                    print("Invalid choice please try again. Enter 1 - 5: ")

    @staticmethod
    def delete():
        """
        Deletes a transaction entry based on the provided transaction ID.

        The method verifies if the transaction ID exists before attempting to delete.

        Returns:
            None
        """
        transaction_id = UserEntryManager.get_transaction_id()
        if CSVManager.verify_transaction_id(transaction_id):
            CSVManager.delete_transaction(transaction_id)

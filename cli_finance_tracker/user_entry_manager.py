from datetime import datetime


class UserEntryManager:
    """
    Manages user entry for transactions, including date, amount, category, and description.

    Attributes:
        DATE_FORMAT (str): The format used for parsing and displaying dates.
        CATEGORIES (dict): Mapping of input to transaction categories ('I' for Income, 'E' for Expense).
    """

    DATE_FORMAT = "%m-%d-%Y"
    CATEGORIES = {
        "I": "Income",
        "E": "Expense"
    }

    @staticmethod
    def get_transaction_id():
        """
        Prompts the user to input a transaction ID.

        Returns:
            int: The transaction ID entered by the user.
        """
        return int(input("Enter a transaction ID: "))

    @classmethod
    def get_date(cls, prompt, allow_default=False):
        """
        Prompts the user for a date in the format 'mm-dd-yyyy'. Optionally allows defaulting to today's date.

        Args:
            prompt (str): The prompt message for the user.
            allow_default (bool): If True, the user can leave the date blank to default to today's date.

        Returns:
            str: A valid date string in 'mm-dd-yyyy' format.
        """
        date_str = input(prompt)

        if allow_default and not date_str:
            return datetime.today().strftime(cls.DATE_FORMAT)

        try:
            valid_date = datetime.strptime(date_str, cls.DATE_FORMAT)
            return valid_date.strftime(cls.DATE_FORMAT)
        except ValueError:
            print("Invalid date format. Please enter the date in mm-dd-yyyy format.")
            return cls.get_date(prompt, allow_default)

    @classmethod
    def get_amount(cls):
        """
        Prompts the user to input a valid amount for the transaction.

        Returns:
            float: A valid transaction amount entered by the user.

        Raises:
            ValueError: If the entered amount is less than or equal to zero.
        """
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                raise ValueError("Amount must be a non-negative non-zero value")
            return amount
        except ValueError as e:
            print(e)
            return cls.get_amount()

    @classmethod
    def get_category(cls):
        """
        Prompts the user to input a category ('I' for Income, 'E' for Expense).

        Returns:
            str: The corresponding category (Income/Expense) based on the user's input.

        Raises:
            ValueError: If an invalid category is entered.
        """
        category = input("Enter the category ('I' for Income, 'E' for Expense): ").upper()
        if category in cls.CATEGORIES:
            return cls.CATEGORIES[category]

        print("Invalid category entered. Please enter 'I' for Income, 'E' for Expense.")
        return cls.get_category()

    @staticmethod
    def get_description():
        """
        Prompts the user for an optional description of the transaction.

        Returns:
            str: The description entered by the user, or an empty string if not provided.
        """
        return input("Enter a description (optional): ")

import pandas as pd
import csv
from datetime import datetime


class CSVManager:
    """
    Manages CSV files related to financial transactions and logs various updates.

    Attributes:
        CSV_FILES_DICT (list of dict): Configuration of CSV files with their names, paths, and columns.
        MODIFICATIONS (list of str): Types of modifications that can be logged.
        FORMAT (str): Date format used for date columns.
        UPDATE_FIELD_CHOICES (list of str): Fields that can be updated in transactions.
    """
    CSV_FILES_DICT = [
        {
            "name": "transaction records",
            "csv_file": "finance_data.csv",
            "columns": [
                "transaction_id",
                "date",
                "category",
                "amount",
                "description"
            ]
        },
        {
            "name": "new entry log records",
            "csv_file": "new_entry_log.csv",
            "columns": [
                "timestamp",
                "transaction_id",
                "update_type",
                "success",
                "message"
            ]
        },
        {
            "name": "deleted log records",
            "csv_file": "delete_log.csv",
            "columns": [
                "timestamp",
                "transaction_id",
                "update_type",
                "message",
                "success",
                "del_record_date",
                "del_record_category",
                "del_record_amount",
                "del_record_description"
            ]
        },
        {
            "name": "update log records",
            "csv_file": "update_log.csv",
            "columns": [
                "timestamp",
                "transaction_id",
                "update_type",
                "field_update",
                "success",
                "old_value",
                "new_value"
            ]
        }
    ]

    MODIFICATIONS = ["updated", "deleted", "new entry"]
    FORMAT = "%m-%d-%Y"
    UPDATE_FIELD_CHOICES = ["date", "category", "amount", "description"]

    @classmethod
    def initialize_csv(cls):
        """
        Initializes CSV files if they do not already exist by creating empty files with the appropriate columns.

        Returns:
            None
        """
        for config in cls.CSV_FILES_DICT:
            csv_file = config["csv_file"]
            columns = config["columns"]
            try:
                pd.read_csv(csv_file)
                print(f"Successfully read {csv_file}")
            except FileNotFoundError:
                df = pd.DataFrame(columns=columns)
                df.to_csv(csv_file, index=False)
                print(f"Initialized CSV file: {csv_file}")

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Adds a new transaction entry to the transaction records CSV file.

        Args:
            date (str): The date of the transaction.
            amount (float): The amount of the transaction.
            category (str): The category of the transaction.
            description (str): A description of the transaction.

        Returns:
            None
        """
        try:
            df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
            if df.empty:
                transaction_id = 1
            else:
                transaction_id = df["transaction_id"].max() + 1

            new_entry = {
                "transaction_id": transaction_id,
                "date": date,
                "amount": amount,
                "category": category,
                "description": description
            }

            with open(cls.CSV_FILES_DICT[0]["csv_file"], "a", newline="") as csv_file:
                csv_write = csv.DictWriter(csv_file, fieldnames=cls.CSV_FILES_DICT[0]["columns"])
                csv_write.writerow(new_entry)

            print("\nEntry added successfully")

            cls.update_new_entry_log(cls.get_current_time(), transaction_id, cls.MODIFICATIONS[2].title(), True,
                                     "Entry added")
        except Exception as e:
            print(f"\nFailed to add entry: Error: {e}")

    @classmethod
    def write_to_logs(cls, index_of_file, entry, update_type_index):
        """
        Writes a log entry to the specified log file.

        Args:
            index_of_file (int): The index of the CSV_FILES_DICT for the target log file.
            entry (dict): The log entry to be written.
            update_type_index (int): Index of the update type in MODIFICATIONS.

        Returns:
            None
        """
        with open(cls.CSV_FILES_DICT[index_of_file]["csv_file"], "a", newline="") as csv_file:
            write_to_csv = csv.DictWriter(csv_file, fieldnames=cls.CSV_FILES_DICT[index_of_file]["columns"])
            write_to_csv.writerow(entry)
            print(f"\nUpdated {cls.MODIFICATIONS[update_type_index].title()} Log. Timestamp: {cls.get_current_time()}")
            print("\n//////////////////// End of Program ////////////////////")

    @classmethod
    def write_to_csv(cls, data_frame):
        """
        Writes a DataFrame to the transaction records CSV file.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be written to CSV.

        Returns:
            None
        """
        try:
            data_frame.to_csv(cls.CSV_FILES_DICT[0]["csv_file"], index=False)
            print("\nData successfully written to CSV.")
        except Exception as e:
            print(f"\nFailed to write to CSV file: {e}")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Retrieves transactions within a specified date range.

        Args:
            start_date (str): The start date of the range.
            end_date (str): The end date of the range.

        Returns:
            pd.DataFrame: DataFrame containing transactions within the date range.
        """
        df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("\nNo transactions found in the given date range.")
        else:
            print(
                f"\n//////////////////// Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)} ////////////////////")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))
            print("\n//////////////////// End of Records ////////////////////")
            cls.net_amount(filtered_df)
        return filtered_df

    @classmethod
    def net_amount(cls, df):
        """
        Prints a summary of financial transactions, including the number of entries, average income and expense,
        total income, total expense, and net savings.

        Args:
            df (pd.DataFrame): DataFrame containing transaction data.

        Returns:
            None
        """
        print("\n//////////////////// Summary ////////////////////")
        print("//////////////////// Number of Entries ////////////////////")
        num_of_entries = df.groupby("category")["amount"].count()
        print(num_of_entries.to_string())
        avg_transactions = df.groupby("category")["amount"].mean().round(2)
        avg_transactions = avg_transactions.apply(lambda x: f"${x:.2f}")
        print("\n//////////////////// Average Income and Expense ////////////////////")
        print(avg_transactions.to_string())
        total_income = df[df["category"] == "Income"]["amount"].sum()
        total_expense = df[df["category"] == "Expense"]["amount"].sum()
        print(f"\nTotal Income ${total_income:.2f}")
        print(f"Total Expense ${total_expense:.2f}")
        print("////////////////////////////////////////////////////////////")
        print(f"Net Saving: ${total_income - total_expense:.2f}")
        print("////////////////////////////////////////////////////////////")
        print("\n//////////////////// End of Program ////////////////////")

    @classmethod
    def verify_transaction_id(cls, transaction_id):
        """
        Verifies if a given transaction ID exists in the transaction records.

        Args:
            transaction_id (int): The transaction ID to be verified.

        Returns:
            bool: True if the transaction ID is found, False otherwise.
        """
        df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
        if transaction_id not in df["transaction_id"].values:
            print("\nTransaction ID NOT FOUND. Please enter a valid transaction id.")
            return False
        else:
            print("\nTransaction ID found successfully.")
            return True

    @classmethod
    def update_transactions(cls, transaction_id, update_field, new_value):
        """
        Updates a specific field of a transaction record with a new value.

        Args:
            transaction_id (int): The transaction ID of the record to update.
            update_field (str): The field to be updated.
            new_value (str or float): The new value to set for the field.

        Returns:
            None
        """
        try:
            df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
            old_value = df[df["transaction_id"] == transaction_id][update_field].iloc[0]
            df.loc[df["transaction_id"] == transaction_id, update_field] = new_value
            cls.write_to_csv(df)
            cls.updates_type(0)
            print("********** New Updated Record **************")
            print(df[df["transaction_id"] == transaction_id].to_string(index=False))
            cls.update_update_log(cls.get_current_time(), transaction_id, cls.MODIFICATIONS[0], update_field, True,
                                  old_value, new_value)
        except Exception as e:
            print(f"\nFailed to update a transaction amount. Error {e}")

    @classmethod
    def get_current_time(cls):
        """
        Retrieves the current time formatted according to the class date format.

        Returns:
            str: The current time as a formatted string.
        """
        return datetime.now().strftime(f"{cls.FORMAT} %I:%M:%S %p")

    @classmethod
    def delete_transaction(cls, transaction_id):
        """
        Deletes a transaction record based on the provided transaction ID.

        Args:
            transaction_id (int): The transaction ID of the record to delete.

        Returns:
            None
        """
        try:
            df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
            deleted_transaction = df[df["transaction_id"] == transaction_id]
            del_rec_date = deleted_transaction["date"].iloc[0]
            del_rec_category = deleted_transaction["category"].iloc[0]
            del_rec_amount = deleted_transaction["amount"].iloc[0]
            del_rec_description = deleted_transaction["description"].iloc[0]

            if deleted_transaction.empty:
                print("\nTransaction ID NOT FOUND. No record deleted.")
                return

            df = df[df["transaction_id"] != transaction_id]
            cls.write_to_csv(df)
            cls.updates_type(1)
            print("//////////////////// Deleted Record ////////////////////")
            print(deleted_transaction.to_string(index=False))
            cls.update_delete_log(cls.get_current_time(), transaction_id, cls.MODIFICATIONS[1], "Deleted entry", True,
                                  del_rec_date, del_rec_category, del_rec_amount, del_rec_description)
        except Exception as e:
            print(f"\nFailed to delete a transaction. Error {e}")

    @classmethod
    def updates_type(cls, index_of_modification):
        """
        Prints the update type and the current time.

        Args:
            index_of_modification (int): Index of the modification type in MODIFICATIONS.

        Returns:
            None
        """
        print(f"Transaction {cls.MODIFICATIONS[index_of_modification]} successfully.")
        print(
            f"\n//////////////////// Here is {cls.MODIFICATIONS[index_of_modification].title()} Transaction ////////////////////")
        print(f"Updated Time: {cls.get_current_time()}")

    @classmethod
    def update_new_entry_log(cls, timestamp, transaction_id, update_type, success, message):
        """
        Logs the addition of a new entry to the new entry log records CSV file.

        Args:
            timestamp (str): The timestamp of the log entry.
            transaction_id (int): The transaction ID associated with the log entry.
            update_type (str): The type of update (e.g., "New Entry").
            success (bool): Indicates whether the operation was successful.
            message (str): A message regarding the log entry.

        Returns:
            None
        """
        try:
            new_log = {
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "update_type": update_type,
                "success": success,
                "message": message
            }

            cls.write_to_logs(1, new_log, 2)
        except Exception as e:
            print(f"\nFailed to write to CSV Change Log File. Timestamp: {cls.get_current_time()}.  Error {e}")

    @classmethod
    def update_delete_log(cls, timestamp, transaction_id, update_type, message, success, del_record_date,
                          del_record_category, del_record_amount, del_record_description):
        """
        Logs the deletion of a transaction to the deleted log records CSV file.

        Args:
            timestamp (str): The timestamp of the log entry.
            transaction_id (int): The transaction ID associated with the log entry.
            update_type (str): The type of update (e.g., "Deleted").
            message (str): A message regarding the log entry.
            success (bool): Indicates whether the operation was successful.
            del_record_date (str): The date of the deleted record.
            del_record_category (str): The category of the deleted record.
            del_record_amount (float): The amount of the deleted record.
            del_record_description (str): The description of the deleted record.

        Returns:
            None
        """
        try:
            new_log = {
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "update_type": update_type,
                "message": message,
                "success": success,
                "del_record_date": del_record_date,
                "del_record_category": del_record_category,
                "del_record_amount": del_record_amount,
                "del_record_description": del_record_description
            }

            cls.write_to_logs(2, new_log, 1)
        except Exception as e:
            print(f"\nFailed to write to CSV Change Log File. Timestamp: {cls.get_current_time()}.  Error {e}")

    @classmethod
    def update_update_log(cls, timestamp, transaction_id, update_type, field_update, success, old_value, new_value):
        """
        Logs the update of a transaction field to the update log records CSV file.

        Args:
            timestamp (str): The timestamp of the log entry.
            transaction_id (int): The transaction ID associated with the log entry.
            update_type (str): The type of update (e.g., "Updated").
            field_update (str): The field that was updated.
            success (bool): Indicates whether the operation was successful.
            old_value (str or float): The old value of the updated field.
            new_value (str or float): The new value of the updated field.

        Returns:
            None
        """
        try:
            new_log = {
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "update_type": update_type,
                "field_update": field_update,
                "success": success,
                "old_value": old_value,
                "new_value": new_value
            }
            cls.write_to_logs(3, new_log, 0)
        except Exception as e:
            print(f"\nFailed to write to CSV Change Log File. Timestamp: {cls.get_current_time()}.  Error {e}")

    @classmethod
    def view_records(cls, index):
        """
        Displays records from the specified CSV file.

        Args:
            index (int): The index of the CSV file configuration in CSV_FILES_DICT.

        Returns:
            None
        """
        try:
            df = pd.read_csv(cls.CSV_FILES_DICT[index]["csv_file"])
            record_name = cls.CSV_FILES_DICT[index]["name"]
            print(f"\n//////////////////// {record_name.title()} ////////////////////")

            if df.empty:
                print("\nThere is no records currently available. You should add new records")
                return
            else:
                df = df.to_string(index=False)
                print(df)
                print("\n//////////////////// End of Program ////////////////////")
                print(f"Completed Timestamp: {cls.get_current_time()}")
        except Exception as e:
            print(f"\nFailed to view records. Error {e}")

    @classmethod
    def expense_income_report(cls, report_type):
        """
        Generates a report of expenses or income, grouped by description and ordered by amount.

        Args:
            report_type (str): The type of report to generate ("Expense" or "Income").

        Returns:
            None
        """
        df = pd.read_csv(cls.CSV_FILES_DICT[0]["csv_file"])
        df_report = df[df["category"] == report_type.title()].copy()
        df_report["description"] = df_report["description"].str.lower()

        df_report_group = df_report.groupby("description")["amount"].sum()
        df_report_group.sort_values(ascending=False, inplace=True)

        df_report_group = df_report_group.reset_index()
        df_report_group.columns = ["description", "amount"]
        df_report_group["rank"] = df_report_group["amount"].rank(method="min", ascending=False)
        print(f"//////////////////// Here is {report_type.title()} Report ////////////////////")
        print(df_report_group.to_string())
        print("//////////////////// End of Report ////////////////////")

    @classmethod
    def which_update_field(cls, field_index):
        """
        Retrieves the field name based on the provided index.

        Args:
            field_index (int): The index of the field in UPDATE_FIELD_CHOICES.

        Returns:
            str: The name of the field corresponding to the index.
        """
        return cls.UPDATE_FIELD_CHOICES[field_index]

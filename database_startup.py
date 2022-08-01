import layouts
from layouts import *
from database_handler import DataBaseFunctions


class DatabaseSetUp:
    def __init__(self, database):
        """
        init
        :param database: The main Database
        """
        self.database = database
        self.dbf = DataBaseFunctions(database)

    def __str__(self):
        """Initial setup for the whole database"""

    @staticmethod
    def fetch_default_tables():
        """
        Gets all layouts from the layouts.py
        :return: a list of tables that needs to be created.
        """

        tables = []

        for index, method in enumerate(dir(layouts)):
            if index > 7:
                tables.append(method)

        return tables

    def tables(self):
        """
        Create all tables from layouts.py in the main database.
        :return: None
        """
        tables = self.fetch_default_tables()
        conn = self.dbf.create_connection()
        if conn is not None:
            for table in tables:
                print(table)
                self.dbf.submit_update(eval(table))
        else:
            print("Error! cannot create the database connection.")


if __name__ == "__main__":
    database_dib = "SCore.db"
    dbs = DatabaseSetUp(database_dib)
    dbs.tables()

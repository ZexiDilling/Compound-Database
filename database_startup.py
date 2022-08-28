import configparser

import table_layouts
from table_layouts import *
from database_handler import DataBaseFunctions
from config_writer import ConfigWriter


class DatabaseSetUp:
    def __init__(self, config, database):
        """
        init
        :param config: The config for the config file
        :type config: configparser.Configparser
        """
        # self.database = config["Database"]["database"]
        self.config = config
        self.database = database
        self.cw = ConfigWriter(self.config)

    def __str__(self):
        """Initial setup for the whole database"""

    def _check_database(self):
        try:
            if self.database != self.config["Database"]["database"]:
                setting_dict = {"Database": {"database": self.database}}
                self.cw.run(setting_dict, "simple_settings", True)
        except KeyError:
            setting_dict = {"Database": {"database": self.database}}
            self.cw.run(setting_dict, "simple_settings", True)

    def _fetch_default_tables(self):
        """
        Gets all layouts from the table_layouts.py

        :return: a list of tables that needs to be created.
        :rtype; list
        """
        headline = "Tables"
        simple_setting_ditch = {headline: {}}
        tables = []

        for index, method in enumerate(dir(table_layouts)):
            if index > 7:
                temp_str = eval(method)
                temp_str = temp_str.split(" ")
                temp_str = temp_str[6].strip("\n").strip("(")
                simple_setting_ditch["Tables"][method] = temp_str
                tables.append(method)

        self.cw.run(simple_setting_ditch, "simple_settings", True)
        return tables

    def controller(self):
        """
        Create all tables from table_layouts.py in the main database.

        :return: A Database with tables
        """
        self._check_database()
        tables = self._fetch_default_tables()
        dbf = DataBaseFunctions(self.config)

        conn = dbf.create_connection()
        if conn is not None:
            for table in tables:
                dbf.submit_update(eval(table))
        else:
            print("Error! cannot create the database connection. - IN DATABASE STARTUP")


if __name__ == "__main__":
    database_dib = "SCore.db"
    config = configparser.ConfigParser()
    config.read("config.ini")

    #
    dbs = DatabaseSetUp(config, database_dib)
    dbs.fetch_default_tables()
    # dbs.tables()

import sqlite3


class DataBaseFunctions:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.database = "SCore.db"

    def __str__(self):
        """Control all database function, as sqlite3 is terrible for writing to and from"""

    @staticmethod
    def _list_columns(data):
        """
        Genera a list of headlines/keys from a dict.
        :param data: A dict over the data
        :return: a list of headlines/keys from dict
        """
        return [clm for clm in data]

    @staticmethod
    def _add_place_holders(columns):
        """
        make a string of "?" depending on how many columns/headlines/keys a dict have.
        :param columns: list of columns/headlines/keys
        :return: A string of "?" for SQlite3 to use for adding values
        """
        return ",".join("?" for _ in columns)

    @staticmethod
    def _add_layout(table_name, place_holders):
        """
        Makes a string that SQlite3 can use to add data
        :param table_name: name of table
        :param place_holders: String of "?" one "?" per headline the table has
        :return: A string for SQlite to use.
        """
        return f"INSERT INTO {table_name} VALUES({place_holders})"

    @staticmethod
    def _data_layout(data, column_names):
        """
        Formatting a list for SQlite3 to add to the database
        :param data: The data that needs to be added
        :param column_names: List of column names
        :return: List of data and values.
        """
        return [data[name] for name in column_names]

    def _add_data_to_table(self, layout, data):
        """
        Function that adds data to the database
        :param layout: String with table name, and "?" for each value that needs to be added
        :param data: List of values that needs to be added
        :return: Data added to a table
        """
        try:
            self.cursor.execute(layout, data)
        except sqlite3.IntegrityError:
            pass
            #print("ERROR") # NEEDS TO WRITE REPORT OVER ERRORS TO SEE WHY DATA WAS NOT ADDED!!!
            # EITHER DUE TO DUPLICATES OR MISSING REFERENCE(FOREIGN KEY)
        self.conn.commit()
        self.cursor.close()

    def add_records_controller(self, table_name, data):
        """
        Adds data to the database, main access point to multiple functions
        :param table_name: Name of the table where the data needs to be added
        :param data: The data, in dicts form, that needs to be added to the database
        :return: Data added to the database
        """
        self.create_connection()
        list_columns = self._list_columns(data)
        place_holder = self._add_place_holders(list_columns)
        layout = self._add_layout(table_name, place_holder)
        data_layout = self._data_layout(data, list_columns)
        self._add_data_to_table(layout, data_layout)

    def update_vol(self, source_table, vol, barcode_source, row_id):
        """
        Updates volumes in the database
        :param source_table: Where the compound came from
        :param vol: How much compound was taken
        :param barcode_source: Where is the compound going
        :param row_id: The id of the row in the database
        :return: An updated database
        """
        table = f"UPDATE {source_table} SET volume = volume - {vol} WHERE {row_id} = {barcode_source} "
        self.submit_update(table)

    def find_data(self, table, barcode, id_number, barcode_name, id_name):
        """
        Finds data in the database
        :param table: What table the data should be in
        :param barcode: Barcode of the plate
        :param id_number: Compound ID
        :param barcode_name: Headline of the plate-column in the table
        :param id_name: Headline for the compound id in the table
        :return: Data from the database
        """
        find = f"SELECT rowid, * FROM '{table}' WHERE {barcode_name} = '{barcode}' AND {id_name} = '{id_number}'"
        return self.fetch(find)

    def find_plates(self, table, barcode, barcode_name):
        """
        Finds plates in a table from the database
        :param table: What table are the plates in
        :param barcode: Barcode of the plates
        :param barcode_name: Headline for the plates in the table
        :return: Data from the database
        """
        find = f"SELECT rowid, * FROM '{table}' WHERE {barcode_name} = '{barcode}' "

        return self.fetch(find)

    def delete_records(self):
        pass

    def run(self):
        pass

    #table generator... maybe not needed
    # @staticmethod
    # def generate_columns(columns):
    #     return ", ".join(headline for headline in columns)
    #
    # @staticmethod
    # def setup_columns(column_names):
    #     temp_list = []
    #     for index, headline in column_names:
    #         if index != 0:
    #             if headline == "Volume":
    #                 temp_list.append(f"{headline} REAL")
    #             else:
    #                 temp_list.append(f"{headline} TEXT")
    #     return temp_list
    #
    # @staticmethod
    # def setup_name(table_name):
    #     if table_name.isnumeric():
    #         return f"compound_{table_name}"
    #     else:
    #         return table_name
    #
    # @staticmethod
    # def generate_table_layout(table_name, columns_names):
    #     return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_names});"
    #
    # def table_generator(self, dict_data):
    #     try:
    #         table_name = dict_data["DestinationBarcode"]
    #     except KeyError:                                            # Incase a table per compound is needed
    #         table_name = f"compound_{dict_data['barcode']}"
    #     column_list = self.setup_columns(dict_data)
    #     columns = self.generate_columns(column_list)
    #     table = self.generate_table_layout(table_name, columns)
    #     self.submit_update(table)

    def fetch(self, data):
        """
        Create a connection to the database, execute the search and gets data out of  the database
        :param data: The data the user is looking for
        :return: all records that fits the data
        """
        self.create_connection()
        self.cursor.execute(data)
        records = self.cursor.fetchall()
        self.cursor.close()
        return records

    def submit_update(self, data):
        """
        Connect to the database, Updates the database and closes the connection
        :param data: Data that needs  to be updated
        :return:
        """
        self.create_connection()
        try:
            self.cursor.execute(data)
        except sqlite3.IntegrityError:
            pass
        self.conn.commit()
        self.cursor.close()

    def create_connection(self):
        """
        Create a connection to the database
        :return: A connection to the database
        """
        self.conn = sqlite3.connect(self.database)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        return self.conn

    def list_of_all_tables(self):
        """
        Gets a list of all the tables in the database
        :return: A list of all the tables in the database
        """
        return [tables for tables in self.cursor.execute("SELECT name FROM sqlite_master  WHERE type='table';")]

    def number_of_rows(self, table):
        """
        Counts rows in database.
        Missing to check for active samples
        :param table: Table name
        :return: number of rows in table.
        """
        number = f"SELECT COUNT(*) from {table}"
        self.create_connection()
        self.cursor.execute(number)
        return self.cursor.fetchone()[0]

    def join_table_controller(self, min_volume, table_1="compound_main", table_2="compound_mp", shared_data="compound_id"):
        """
        Joins two tables together to create a new temp table
        :param min_volume: Minimum volume needed for a compound
        :param table_1: Table 1 of 2 for joining together
        :param table_2: Table 2 of 2 for joining together
        :param shared_data: The data they share
        :return: Rows of data where the two tables matches.
        """
        sql_join = f"SELECT {table_1}.compound_id, mp_barcode, mp_well, smiles, {table_2}.volume  FROM {table_1} JOIN " \
                   f"{table_2} ON {table_1}.{shared_data} = {table_2}.{shared_data} WHERE {min_volume}<{table_2}.volume;"
        return self._row_creator(sql_join)

    def return_full_table(self, table, min_volume):
        """
        Gets all information from a table, there is over "min_volume" left
        :param table: Table the data needs  to be pulled from
        :param min_volume: Threshold for fecthing data
        :return: Rows of data, based on min_volume
        """
        temp_table = f"SELECT * FROM {table} WHERE {min_volume}<volume"
        return self._row_creator(temp_table)

    def records_to_rows(self, table, data, clm_header):
        temp_table = f"SELECT * FROM {table} WHERE {clm_header} = {data}"
        return self._row_creator(temp_table)

    def _row_creator(self, data):
        """
        Gets data from the database based on criteria
        :param data: Data that needs to be found.
        :return: Rows of data from the database
        """
        rows = {}
        self.create_connection()
        self.cursor.execute(data)
        records = self.cursor.fetchall()
        headers = self.cursor.description

        for data in records:
            rows[data[0]] = {}
            for index, header in enumerate(headers):
                rows[data[0]][header[0]] = data[index]

        self.cursor.close()
        return rows


if __name__ == "__main__":
    database = "SCore.db"
    table = "compound_main"

    dbf = DataBaseFunctions()
    print(dbf.return_full_table(table))

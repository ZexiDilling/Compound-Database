import sqlite3


class DataBaseFunctions:
    def __init__(self, config):
        self.conn = None
        self.cursor = None
        self.database = config["Database"]["database"]

    def __str__(self):
        """Control all database function, as sqlite3 is terrible for writing to and from"""

    @staticmethod
    def _list_columns(data):
        """
        Genera a list of headlines/keys from a dict.

        :param data: A dict over the data
        :type data: dict
        :return: a list of headlines/keys from dict
        :rtype: list
        """
        return [clm for clm in data]

    @staticmethod
    def _add_place_holders(columns):
        """
        make a string of "?" depending on how many columns/headlines/keys a dict have.

        :param columns: list of columns/headlines/keys
        :type columns: list
        :return: A string of "?" for SQlite3 to use for adding values
        :rtype: str
        """
        return ",".join("?" for _ in columns)

    @staticmethod
    def _add_layout(table_name, place_holders):
        """
        Makes a string that SQlite3 can use to add data

        :param table_name: name of table
        :type table_name: str
        :param place_holders: String of "?" one "?" per headline the table has
        :type place_holders: str
        :return: A string for SQlite to use.
        :type: str
        """
        return f"INSERT INTO {table_name} VALUES({place_holders})"

    @staticmethod
    def _data_layout(data, column_names):
        """
        Formatting a list for SQlite3 to add to the database

        :param data: The data that needs to be added
        :type data: dict
        :param column_names: List of column names
        :type column_names: list
        :return: List of data and values.
        :rtype: list
        """
        return [data[name] for name in column_names]

    def _add_data_to_table(self, layout, data):
        """
        Function that adds data to the database

        :param layout: String with table name, and "?" for each value that needs to be added
        :type layout: str
        :param data: List of values that needs to be added
        :type data: list
        :return: Data added to a table
        """
        # try:
        self.cursor.execute(layout, data)
        # except sqlite3.IntegrityError:
        #     pass
            #print("ERROR") # NEEDS TO WRITE REPORT OVER ERRORS TO SEE WHY DATA WAS NOT ADDED!!!
            # EITHER DUE TO DUPLICATES OR MISSING REFERENCE(FOREIGN KEY)
        self.conn.commit()
        self.cursor.close()

    def add_records_controller(self, table_name, data):
        """
        Adds data to the database, main access point to multiple functions

        :param table_name: Name of the table where the data needs to be added
        :type table_name: str
        :param data: The data, in dicts form, that needs to be added to the database
        :type data: dict
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
        :type source_table: str
        :param vol: How much compound was taken
        :type vol: int
        :param barcode_source: Where is the compound going
        :type barcode_source: str
        :param row_id: The id of the row in the database
        :type row_id: str
        :return: An updated database
        """
        table = f"UPDATE {source_table} SET volume = volume - {vol} WHERE {row_id} = {barcode_source} "
        self.submit_update(table)

    def find_data(self, table, barcode, id_number, barcode_name, id_name):
        """
        Finds data in the database

        :param table: What table the data should be in
        :type table: str
        :param barcode: Barcode of the plate
        :type barcode: str
        :param id_number: Compound ID
        :type id_number: int
        :param barcode_name: Headline of the plate-column in the table
        :type barcode_name: str
        :param id_name: Headline for the compound id in the table
        :type id_name: str
        :return: Data from the database
        :rtype: dict
        """
        find = f"SELECT rowid, * FROM '{table}' WHERE {barcode_name} = '{barcode}' AND {id_name} = '{id_number}'"
        return self.fetch(find)

    def find_plates(self, table, barcode, barcode_name):
        """
        Finds plates in a table from the database

        :param table: What table are the plates in
        :type table: str
        :param barcode: Barcode of the plates
        :type barcode: str
        :param barcode_name: Headline for the plates in the table
        :type barcode_name: str
        :return: Data from the database
        :rtype: dict
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
        :type data: str
        :return: all records that fits the data
        :rtype: dict
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
        :type data: str
        :return: commits updates to the database
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
        :
        """
        self.conn = sqlite3.connect(self.database)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        # return self.conn

    def list_of_all_tables(self):
        """
        Gets a list of all the tables in the database

        :return: A list of all the tables in the database
        :rtype: list
        """
        return [tables for tables in self.cursor.execute("SELECT name FROM sqlite_master  WHERE type='table';")]

    def number_of_rows(self, table):
        """
        Counts rows in database.
        Missing to check for active samples

        :param table: Table name
        :type table: str
        :return: number of rows in table.
        :rtype: int
        """
        number = f"SELECT COUNT(*) from {table}"
        self.create_connection()
        self.cursor.execute(number)
        return self.cursor.fetchone()[0]

    def join_table_controller_old(self, search_limiter, table_1="compound_main", table_2="compound_mp",
                              shared_data="compound_id"):
        """
        Joins two tables together to create a new temp table

        :param min_volume: Minimum volume needed for a compound
        :type min_volume: int
        :param table_1: Table 1 of 2 for joining together
        :type table_1: str
        :param table_2: Table 2 of 2 for joining together
        :type table_2: str
        :param shared_data: The data they share
        :type shared_data: str
        :return: Rows of data where the two tables matches.
        :rtype: dict
        """
        min_volume = search_limiter["volume"]["value"]
        sql_join = f"SELECT {table_1}.compound_id, mp_barcode, mp_well, smiles, {table_2}.volume  FROM {table_1} " \
                   f"JOIN " f"{table_2} ON {table_1}.{shared_data} = {table_2}.{shared_data} WHERE {min_volume}<" \
                   f"{table_2}.volume;"

        return self._row_creator(sql_join)

    def join_table_controller(self, search_limiter):
        """
        Joins two tables together to create a new temp table

        :param min_volume: Minimum volume needed for a compound
        :type min_volume: int
        :param table_1: Table 1 of 2 for joining together
        :type table_1: str
        :param table_2: Table 2 of 2 for joining together
        :type table_2: str
        :param shared_data: The data they share
        :type shared_data: str
        :return: Rows of data where the two tables matches.
        :rtype: dict
        """
        selector_1 = ""
        selector_2 = ""
        binder = ""
        for index, values in enumerate(search_limiter):
            if index == 0:
                table_1 = values
                selector_1 = self._where_clause_writer(search_limiter[values], values)
            if index == 1:
                table_2 = values
                selector_2 = self._where_clause_writer(search_limiter[values], values)
            shared_data = search_limiter["shared_data"]

        if selector_1 and selector_2:
            binder = "AND"


        sql_join = f"SELECT * FROM {table_1} JOIN {table_2} ON {table_1}.{shared_data} = {table_2}.{shared_data} " \
                   f"{selector_1} {binder} {selector_2}"

        print(sql_join)
        return self._row_creator(sql_join)

    @staticmethod
    def _where_clause_writer(search_limiter, join_table=None):

        if join_table:
            table = f"{join_table}."
        else:
            table = ""

        if search_limiter:
            final_text = "WHERE"
            for conditions in search_limiter:
                if search_limiter[conditions]["use"]:
                    if search_limiter[conditions]["value"]:
                        if search_limiter[conditions]['operator'] == "IN":
                            target_string = "("
                            for values in search_limiter[conditions]['value']:
                                target_string += f"'{values}'"
                                target_string += ","
                            target_string = target_string.removesuffix(",")
                            target_string += ")"

                            final_text += f" {table}{search_limiter[conditions]['target_column']} {search_limiter[conditions]['operator']} " \
                                          f"{target_string}"
                        else:
                            final_text += f" '{search_limiter[conditions]['value']}' {search_limiter[conditions]['operator']} " \
                                          f"{search_limiter[conditions]['target_column']}"
                        final_text += f" AND"

            final_text = final_text.removesuffix(" AND")
            final_text = final_text.removesuffix("WHERE")

        else:
            final_text = ""

        return final_text

    def return_table_data(self, table, search_limiter):
        """
        Gets all information from a table, there is over "min_volume" left

        :param table: Table the data needs  to be pulled from
        :type table: str
        :param search_limiter: Threshold for fecthing data
        :type search_limiter: int
        :return: Rows of data, based on min_volume
        :rtype: dict
        """

        selector = self._where_clause_writer(search_limiter)
        temp_table = f"SELECT * FROM {table} {selector}"
        return self._row_creator(temp_table)

    def records_to_rows(self, table, data, clm_header):
        """
        Gets record depending on a single data point

        :param table: Table the data needs  to be pulled from
        :type table: str
        :param data: The data the user is looking for
        :type data: str
        :param clm_header: The headline for the clm where the data is located
        :type clm_header: str
        :return: the row for the data
        :rtype: dict
        """
        temp_table = f"SELECT * FROM {table} WHERE {clm_header} = {data}"
        return self._row_creator(temp_table)

    def _row_creator(self, data):
        """
        Gets data from the database based on criteria

        :param data: Data that needs to be found.
        :type data: str
        :return: Rows of data from the database
        :rtype: dict
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
    ...

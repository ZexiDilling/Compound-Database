import configparser
from chem_operators import ChemOperators
from database_handler import DataBaseFunctions
from sdf_handler import SDFReader
from csv_handler import CSVReader
from random import sample
from operator import countOf
from file_handler import get_file_list, file_list_distributor, move_files
from xml_handler import XMLReader
from lc_data_handler import LCMSHandler


class FetchData:
    def __init__(self):
        """
        init
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config = config
        self.dbf = DataBaseFunctions()
        self.dbf.create_connection()
        self.co = ChemOperators()

        self.database = "SCore.db"
        self.compound_max = self.dbf.number_of_rows("compound_main")

    def __str__(self):
        """
        Gets data from the database
        :return: rows of Data
        """

    @staticmethod
    def _list_generator(sample_amount, compound_list_temp):
        """
        Generate a random list of compounds based on amount of samples, and total list of possible compounds
        :param sample_amount: Amount of compounds needed
        :param compound_list_temp: List of all compounds that fits criteria
        :return: A list of random compounds
        """
        compound_list_final = set()

        while len(compound_list_final) < sample_amount:
            if len(compound_list_temp) <= sample_amount:
                sample_amount = len(compound_list_temp)
            compound_list_final = sample(compound_list_temp, sample_amount)

        return compound_list_final

    @staticmethod
    def _rows_to_list(rows):
        """
        Makes a list of all compounds
        :param rows: All rows from the database
        :return: A list of all compounds
        """
        return [compound_id for compound_id in rows]

    @staticmethod
    def _liquid_warning(rows, min_volume):
        """
        Create a list of compounds that are running low or out
        :param rows: Rows of data from the Database
        :param min_volume: Minimum volume needed per transferee. Will also determent the warning threshold
        :return: A list of compounds that are under the warning threshold with amount of compound left
        """
        dead_volume = 1
        warning_level = min_volume * 3 + dead_volume
        liquid_warning = {}
        for compound_id in rows:
            if rows[compound_id]["volume"] < warning_level:
                liquid_warning[compound_id] = rows[compound_id]["volume"]

        return liquid_warning

    @staticmethod
    def _row_plate_data(rows, compound_id):
        """
        Generate dicts and list of different kind of data, based on data from the Database
        :param rows: Data from the Database
        :param compound_id: List of random compounds.
        :return: Dict of data, Dict of plates, List of plates and list of plates with amount of each plate.
        """
        row_data = {}
        mp_data = {}
        plate_set = set()
        plate_count = []
        for compounds in rows:
            if compounds in compound_id:
                row_data[compounds] = [rows[compounds]["mp_barcode"], rows[compounds]["mp_well"]]
                mp_data.setdefault(rows[compounds]["mp_barcode"], []).append([rows[compounds]["mp_well"], compounds])
                plate_set.add(rows[compounds]["mp_barcode"])
                plate_count.append(rows[compounds]["mp_barcode"])

        return row_data, mp_data, sorted(plate_set), sorted(plate_count)

    @staticmethod
    def _plate_counter(plates):
        """
        Makes a dict of plates and how many of the same plate there is
        :param plates: List of all the plates
        :return: Dicts with plates and amount of repeats
        """
        return dict((i, countOf(plates, i)) for i in set(plates))

    def _plate_mapping(self, table, plates, barcode_name):
        """
        Makes a dict of plates, with information, like where they are located
        :param table: The table the plates are in
        :param plates: list of all the plates without repeats
        :param barcode_name: Headlines for the plates in the table
        :return: A dict of plates where they are located
        """
        plate_list = []
        for plate in plates:
            plate_temp = self.dbf.find_plates(table, plate, barcode_name)
            plate_list.append(plate_temp)

        return plate_list

    def sub_structure_search(self, smiles, threshold, min_volume,
                             methode="sub_structure_general", table="compound_main"):
        """
        Structure search controller. Controls witch function to use and what table to look into
        :param smiles: The smiles codes that needs to be compared
        :param threshold: The threshold for how similar the compound needs to be to the main smiles code
        :param min_volume: Minimum volume that should be of the compound.
        :param methode: What search method to use
        :param table: What table to find the data
        :return: Rows of data from the Database with compound that fits the sub structure search criteria.
        """
        if table == "compound_main":
            rows = self.dbf.return_full_table(table, min_volume)
        elif table == "join_main_mp":
            rows = self.dbf.join_table_controller(min_volume)

        rows = self.co.structure_search(methode, threshold, rows, smiles)
        return rows

    def get_all_compounds_ids(self, min_volume, table="compound_main"):
        """
        Gets a list of all compounds in the database
        :param min_volume: Minimum volume of compound that should be left
        :param table: What table to look into.
        :return: rows of data from the Database
        """
        if table == "compound_main":
            rows = self.dbf.return_full_table(table, min_volume)
        elif table == "join_main_mp":
            rows = self.dbf.join_table_controller(min_volume)
        elif table == "compound_mp":
            rows = self.dbf.return_full_table(table, min_volume)

        return rows

    def list_to_rows(self, compound_list, table="compound_main"):
        rows = {}
        for compound_id in compound_list:
            temp_dict = self.dbf.records_to_rows(table, compound_id, "compound_id")
            for key, value in temp_dict.items():
                rows[key] = value

        return rows

    def list_limiter(self, sample_amount, table, transferee_volume, sub_search, sub_search_methode, smiles,
                     threshold, ignore_active, plated_compounds):
        """
        Limits the list of compounds based on different criteria.
        :param sample_amount: how many samples is needed
        :param table: What table to find the data in
        :param transferee_volume: volume of compound needed
        :param sub_search: True/False if it should be used or not
        :param sub_search_methode: What structure method should be used if sub_search is True
        :param smiles: The smiles code to be used for the structure search.
        :param threshold: How similar the compound needs to be to the smiles code
        :param ignore_active: If the list needs to take into account compounds already in MotherPlates
        :param plated_compounds: list of compounds in MotherPlates
        :return: List of compounds, list of warnings for low volume, data for the compounds, data for the plates,
        plate location, and volume of plates
        """

        if sub_search:
            rows = self.sub_structure_search(smiles, threshold, transferee_volume, sub_search_methode, table)
        else:
            rows = self.get_all_compounds_ids(transferee_volume, table)

        warnings = self._liquid_warning(rows, transferee_volume)
        full_compound_list = self._rows_to_list(rows)
        if not ignore_active and plated_compounds != []:
            full_compound_list = [compounds for compounds in full_compound_list not in plated_compounds]
        limited_compound_list = self._list_generator(sample_amount, full_compound_list)
        if table == "compound_main":
            return limited_compound_list, warnings
        elif table == "join_main_mp":
            row_data, mp_data, plate_set, plate_count = self._row_plate_data(rows, limited_compound_list)
            mp_mapping = self._plate_mapping("mp_plates", plate_set, "mp_barcode")
            plate_count = self._plate_counter(plate_count)

            return limited_compound_list, warnings, row_data, mp_data, mp_mapping, plate_count

    def get_tubes(self):
        ...

    def get_mother_plates(self):
        ...

    def info_df_generator(self, compounds):
        ...

    # def find_compound_id(self, table_name, item_id_1, item_id_2, item_name_1, item_name_2):
    #     """
    #     Find the compound ID based on plate for MotherPlates! ! !
    #     :param table: Table to look in
    #     :param plate_barcode: Barcode for the Plate
    #     :param well: Well id for the compound
    #     :return: Compound ID
    #     """
    #     rows = self.dbf.find_data(table_name, item_id_1, item_id_2, item_name_1, item_name_2)
    #     return rows[0][1]


class AddData:
    def __init__(self):
        """
        init
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config = config
        self.database = "SCore.db"
        self.dbf = DataBaseFunctions()
        self.sdf_r = SDFReader()
        self.csv_r = CSVReader()
        self.xml_r = XMLReader()
        self.co = ChemOperators()

    def __str__(self):
        """
        Main controller for adding data to the database
        :return: Data added to the database
        """

    @staticmethod
    def _key_name_chang(temp_data):
        temp_data = {key.replace("amount", "volume"): value for key, value in temp_data.items()}
        temp_data = {key.replace("barcode", "compound_id"): value for key, value in temp_data.items()}
        return temp_data

    @staticmethod
    def _popper(table, data_dict):
        """
        Remove data from a dict
        :param table: "Pops" different values depending on what table is being worked on.
        :param data_dict: Dict of data
        :return: A dict of data with less key-values
        """
        temp_dict = data_dict
        if table == "compound_mp":
            ban_list = ["SourceWell", "SourceBarcode"]
            if ban_list[0] in data_dict:
                for clm in ban_list:
                    data_dict.pop(clm)

        if table == "purity":
            ban_list = ["Peak_Info", "mass", "time_date", "wavelength"]
            if ban_list[0] in data_dict:
                for clm in ban_list:
                    data_dict.pop(clm)

        return temp_dict

    @staticmethod
    def _re_ordering_dict(dict_wrong_order, destination_table):
        """
        Re-arrange the order of the dict to work with the tables in the database
        :param dict_wrong_order: The dicts that needs to be re-arrange
        :param destination_table: What tables the data needs to fit
        :return: the Dict_wrong_order in the right order to fit the Database
        """
        if destination_table == "compound_main":
            key_order = ["compound_id", "smiles", "png", "volume"]

        if destination_table == "compound_mp":
            key_order = ["compound_id", "DestinationBarcode", "DestinationWell", "Volume"]

        elif destination_table == "compound_dp":
            key_order = ["compound_id", "SourceBarcode", "SourceWell", "DestinationBarcode", "DestinationWell", "Volume"]

        elif destination_table == "purity":
            key_order = ["compound_id", "experiment", "result_max", "result_max_ion", "result_total"]

        return {value: dict_wrong_order[value] for value in key_order}

    @staticmethod
    def _exp_dict_creator(compound_data, exp_count, exp_type, responsible):
        for data in compound_data:
            time_date = compound_data[data]["time_date"][0]
            break
        exp_count += 1
        experiment_dict = {"exp_id": exp_count, "type": exp_type, "responsible": responsible, "date": time_date}
        return experiment_dict, exp_count

    @staticmethod
    def _purity_unpacker(compound_data, exp_count):

        for compound in compound_data:
            temp_purity = []
            temp_ions = []
            for peaks in compound_data[compound]["Peak_Info"]:
                temp_purity_value = compound_data[compound]["Peak_Info"][peaks]["purity"]
                temp_purity.append(temp_purity_value)
                temp_ion = list(compound_data[compound]["Peak_Info"][peaks].keys())[0]
                temp_ions.append(temp_ion)

            purity_max = max(temp_purity)
            temp_total = sum(temp_purity)

            for index, data in enumerate(temp_purity):
                if data == purity_max:
                    ion_max = temp_ions[index]

            compound_data[compound]["result_max"] = purity_max
            compound_data[compound]["result_max_ion"] = ion_max
            compound_data[compound]["result_total"] = temp_total
            compound_data[compound]["experiment"] = exp_count

        return compound_data

    def compound_main(self, file_list, table="compound_main"):
        """
        Adds data to the main table.
        :param file_list: list of sdf_file that contains compound and compound information
        :param table: table to add the data. Should always be "compound_main"
        :return: None
        """
        for sdf_file in file_list:
            data = self.sdf_r.run(sdf_file)

            for compounds in data:
                temp_compounds_data = self._key_name_chang(data[compounds])
                temp_compounds_data["png"] = self.co.png_string(temp_compounds_data["smiles"])
                temp_compounds_data = self._re_ordering_dict(temp_compounds_data, table)
                self.dbf.add_records_controller(table, temp_compounds_data)

    def mother_plate(self, file_list, file_type, plate_table_name="mp_plates", destination_table="compound_mp",
                     source_table="compound_main", clm_id="compound_id"):
        """
        Reads a CSV file, Adds the data to "compound_mp" Table. Update the volume of "compound_main" table
        Adds the plates to "mp_plates" with locations.
        :param file_list: list of files that contains csv_files with the data that needs to be added.
        :param file_type: What kind of CSV file the data is in.
        :param plate_table_name: Name of tables  for the plates, should always be "mp_plates"
        :param destination_table: Where the compounds are going, should always be "compound_mp"
        :param source_table: Where the compounds are coming from, should always be "compound_main"
        :param clm_id: The name of the compound-ID coloumn, should always be "compound_id"
        :return: None
        """
        for csv_file in file_list:
            data_dict, plates_dict = self.csv_r.csv_r_controller(csv_file, file_type)

            for plate in plates_dict:
                self.dbf.add_records_controller(plate_table_name, plates_dict[plate])
            for transferee in data_dict:
                new_dict = self._popper(destination_table, data_dict[transferee])
                new_dict = self._re_ordering_dict(new_dict, destination_table)

                self.dbf.add_records_controller(destination_table, new_dict)
                self.dbf.update_vol(source_table, data_dict[transferee]["Volume"],
                                    data_dict[transferee]["compoundID"], clm_id)

    def daughter_plate(self, file_list, plate_table_name="dp_plates",
                       destination_table="compound_dp", source_table="compound_mp", clm_id="rowid"):
        """
        Locates all files in a folder with data from the Echo.
        Adds the data to "compound_dp" Table.
        Update the volume of "compound_mp" table
        Adds the plates to "dp_plates" with locations.
        :param file_list: with all the Echo files.
        :type file_list: list
        :param plate_table_name: Name of table for plates, should always be "dp_plates".
        :type plate_table_name: str
        :param destination_table: Where the compounds are going, should always be "compound_dp".
        :type destination_table: str
        :param source_table: Where the compounds are coming from, should always be "compound_mp".
        :type source_table: str
        :param clm_id: Header for clm where row_id is located for updating the right value.
        :type clm_id: str
        :return: None.
        """

        data_dict, plates_dict = self.xml_r.xml_controller(file_list)

        for plate in plates_dict:
            self.dbf.add_records_controller(plate_table_name, plates_dict[plate])

        # Find compound_ID based on source_plate_barcode and source_well from source_table. and add it to the data_dict
        for transferee in data_dict:
            row_data = self.dbf.find_data(source_table, data_dict[transferee]["SourceBarcode"],
                                          data_dict[transferee]["SourceWell"], "mp_barcode", "mp_well")
            data_dict[transferee]["compoundID"] = row_data[0][1]

            # re-arrange the order to make it fit to the database setup
            new_dict = self._re_ordering_dict(data_dict[transferee], destination_table)

            # Adding data to the database
            self.dbf.add_records_controller(destination_table, new_dict)

            # Finding row_id for making sure that it is the right data that gets updated...
            # This will fail with multiple copies of the same compounds in the same MotherPlate... ARG!!!!!
            row = self.dbf.find_data(source_table, data_dict[transferee]["SourceBarcode"],
                                     data_dict[transferee]["compoundID"], "mp_barcode", "compound_id")
            row_id = row[0][0]

            # Update the volume based on row_id.
            self.dbf.update_vol(source_table, data_dict[transferee]["Volume"],
                                row_id, clm_id)

    def purity_data(self, file_list, responsible="PHCH", exp_type="purity", experiment_tabel="experiment",
                    destination_table="purity"):
        """
        Add data to the experiment table, to show when the experiment is done ??
        Add data to the purity table, to have a table over purity, with a reference to the experiment table.
        Update source table to make used plate inactive ?
        :param file_list: contains a list of all the compound_data files
        :param responsible: The responsible person / the person who have produced the data
        :param exp_type: What experimental type the data is from. Should always be purity
        :param experiment_tabel: The table for experiments
        :param destination_table: The table where the data goes, should always be purity
        :return: None
        """
        for compound_data in file_list:
            # Get numbers of rows from the experiment database.
            exp_count = self.dbf.number_of_rows(experiment_tabel)
            # Get a dict for the experiment, to make it fit into the table layout for the experimental table.
            experiment_dict, exp_count = self._exp_dict_creator(compound_data, exp_count, exp_type, responsible)
            # add data to the experimental table.
            self.dbf.add_records_controller(experiment_tabel, experiment_dict)
            # unpack the purity data to single values, and add the last columns for the data to fit with the table
            compound_data = self._purity_unpacker(compound_data, exp_count)
            # loop over each compound, removed unnecessary keys, re-order the dict to fit with the table
            # add data to the table
            for compound in compound_data:
                new_dict = self._popper(destination_table, compound_data[compound])
                new_dict = self._re_ordering_dict(new_dict, destination_table)
                self.dbf.add_records_controller(destination_table, new_dict)
        move_files(file_list)

    def auto_controller(self, folder, file_type):
        compound_list, mp_list, dp_list, purity_list, bio_list, full_file_list = file_list_distributor(folder)
        lc_h = LCMSHandler()
        if compound_list:
            self.compound_main(compound_list)
        if mp_list:
            self.mother_plate(mp_list, file_type)
        if dp_list:
            self.daughter_plate(dp_list)
        if purity_list:
            compound_info = lc_h.lc_controller(purity_list, self.config["MS_default"]["uv_one"],
                                               self.config["MS_default"]["uv_wavelength"],
                                               self.config["MS_default"]["uv_wave"],
                                               self.config["MS_default"]["uv_threshold"],
                                               self.config["MS_default"]["rt_solvent"],
                                               self.config["MS_default"]["ms_delta"],
                                               self.config["MS_default"]["ms_mode"],
                                               self.config["MS_default"]["ms_threshold"])
            self.purity_data(compound_info)
        if bio_list:
            pass
        move_files(full_file_list)

    def add_controller(self, table, folder, file_type=None):
        """
        Main access point to adding data to the Database.
        :param table: What table the data needs to be added to
        :param folder: The folder with all the data files / For purity data this is compound information!!
        :param file_type: What kind of file it is
        :return: None
        """

        if table == "auto":
            self.auto_controller(folder, file_type)
        elif table == "purity_data":
            self.purity_data(folder)

        else:
            file_list = get_file_list(folder)

            if table == "compound_main":
                self.compound_main(file_list)
            elif table == "compound_mp":
                self.mother_plate(file_list, file_type)
            elif table == "compound_dp":
                self.daughter_plate(file_list)
            elif table == "location_table":
                pass
            move_files(file_list)






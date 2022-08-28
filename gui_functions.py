import PySimpleGUI as sg
import configparser
from datetime import date

from csv_handler import CSVWriter, CSVConverter, CSVReader
from lc_data_handler import LCMSHandler
from database_controller import FetchData, AddData
from file_handler import get_file_list
from bio_data_functions import original_data_dict, well_row_col_type
from bio_report_setup import bio_final_report_controller
from bio_date_handler import BIOAnalyser
from info import matrix_header
from json_handler import dict_writer, dict_reader
from pickle_handler import df_writer
from heatmap import Heatmap
from config_writer import ConfigWriter
from plate_formatting import plate_layout_to_well_ditc, daughter_plate_generator, plate_layout_re_formate
from excel_handler import export_plate_layout
from data_miner import dm_controller


def config_update(config):
    fd = FetchData(config)
    cw = ConfigWriter(config)
    # database_specific_commercial
    search_limiter = {
        "ac": {"value": "Commercial",
               "operator": "=",
               "target_column": "ac",
               "use": True}}
    rows = fd.data_search("origin", search_limiter)
    simple_settings = {"database_specific_commercial": {},
                       "database_specific_academic": {}}
    for row in rows:
        simple_settings["database_specific_commercial"][f"vendor_{rows[row]['ac_id']}"] = rows[row]["origin"]

    # database_specific_academia
    search_limiter = {
        "ac": {"value": "Academic",
               "operator": "=",
               "target_column": "ac",
               "use": True}}
    rows = fd.data_search("origin", search_limiter)
    for row in rows:
        simple_settings["database_specific_commercial"][f"academia_{rows[row]['ac_id']}"] = rows[row]["origin"]

    cw.run(simple_settings, "simple_settings", True)


def amount_samples(plate_amount, samples_per_plate=384):
    """
    calculate the amount of samples needed depending on amount of mother plates.

    :param plate_amount: Amount of plates needed
    :type plate_amount: int
    :param samples_per_plate: Amount of samples per plate
    :type samples_per_plate: int
    :return: Total amount of samples needed
    :rtype: int
    """
    if not isinstance(samples_per_plate, int):
        return None
    if not samples_per_plate > 0:
        return None

    if isinstance(plate_amount, int):
        if plate_amount < 1:
            return None
        return plate_amount * samples_per_plate
    else:
        return None


def _compound_list(config, mp_amount, samples_per_plate, ignore_active, sub_search, smiles,
                   sub_search_methode, threshold, source_table, fd, search_limiter):
    """
    Generate list of compounds, based on number of motherplates only, or by sub_structure search.
    Generate comPOUND file for fecthing tubes from the comPOUND freezer.

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param mp_amount: Amount of samples
    :type mp_amount: int
    :param ignore_active: If the list needs to take into account compounds already in MotherPlates with more than
        1 uL volume left. - This might needs to be lowered...
    :type ignore_active: bool
    :param smiles: smiles code to compare compounds with for sub search
    :type smiles: str
    :param sub_search: true or false, If it will use structure search to find compounds or not
    :type sub_search: bool
    :param sub_search_methode: What method to use for making a substructure search
    :type sub_search_methode: str
    :param threshold: This is for sub_searchs. how alike the compounds should minimum be
    :type threshold: float
    :param source_table: The table from the database, where the samples are coming from. and the table where the
        structure search is used. should always be compound_main
    :type source_table: str
    :param search_limiter: A dict over values to search for in the db
    :type search_limiter: dict
    :return:
        - compound_list: A list of compounds
        - liquid_warning_list: A warning for compounds that are close to zero
    :rtype:
        - list
        - list
    """
    if mp_amount:
        sample_amount = amount_samples(mp_amount, samples_per_plate)
    else:
        sample_amount = None
    plated_compounds = []
    if not ignore_active:
        plated_compounds = [compounds for compounds in fd.data_search(config["Tables"]["compound_mp_table"], None)]

    # Gets a list of compounds, based on search criteria
    items = fd.list_limiter(sample_amount, source_table, sub_search, sub_search_methode, smiles,
                            threshold, ignore_active, plated_compounds, search_limiter)

    return items


def table_update_tree(mp_amount, samples_per_plate, ignore_active, sub_search, smiles, sub_search_methode,
                      threshold, source_table, search_limiter, config):
    """
    Updates the compound table with compounds depending on search criteria

    :param mp_amount: amount of mother plates to find compounds from
    :type mp_amount: int
    :param ignore_active: If it should take into account witch compounds are allready in MotherPlates.
        True = All compounds, False = only compounds not found in MotherPlates
    :type ignore_active: bool
    :param sub_search: Is it uses structure search for finding the compounds:
    :type sub_search: bool
    :param smiles: smiles code for the structure search
    :type smiles: str
    :param sub_search_methode: what method to use for the structure search
    :type sub_search_methode: str
    :param threshold: threshold value for how alike the compounds should be to the smiles code
    :type threshold: float
    :param source_table: what table to look for compounds in. (not sure if this one makes sense...
    :type source_table: str
    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param search_limiter: A dict over values to search for in the db
    :type search_limiter: dict
    :return:
        - treedata: The data for the "tree" table
        - all_data: A dict over all the data
        - rows: A dict for each row in the database
        - counter: Number of compounds
    :rtype:
        - PySimpleGUI.PySimpleGUI.TreeData
        - dicts
        - dicts
        - int
    """

    fd = FetchData(config)
    all_data = {}
    all_data_headlines = ["compound_list", "liquid_warning_list", "row_data", "mp_data", "mp_mapping", "plate_count"]

    temp_all_data = _compound_list(config, mp_amount, samples_per_plate, ignore_active, sub_search, smiles,
                                   sub_search_methode, threshold, source_table, fd, search_limiter)

    if not temp_all_data:
        return None
    else:
        for índex, values in enumerate(temp_all_data):
            all_data[all_data_headlines[índex]] = values

        # if source_table == "join_main_mp":
        #     rows = fd.list_to_rows(all_data["compound_list"], source_table)
        # elif source_table == config["Tables"]["compound_main"]:
        #     rows = fd.list_to_rows(all_data["compound_list"], source_table)

        if source_table == "join_main_mp":
            search_limiter["join_tables"][config["Tables"]["compound_mp_table"]]["compound_id"]["value"] = \
                all_data["compound_list"]
            search_limiter["join_tables"][config["Tables"]["compound_mp_table"]]["compound_id"]["use"] = True
            search_limiter_tree = search_limiter["join_tables"]

        elif source_table == config["Tables"]["compound_main"]:
            search_limiter_tree = {source_table: {"value": all_data["compound_list"],
                                                  "operator": "IN",
                                                  "target_column": "compound_id",
                                                  "use": True}}
        rows = {}

        temp_dict = fd.data_search(source_table, search_limiter_tree)
        for key, value in temp_dict.items():
            rows[key] = value

        counter = 0
        treedata = sg.TreeData()

        for compound_id in rows:

            temp_list = []
            for key in rows[compound_id]:
                if key == "png":
                    temp_png = rows[compound_id][key]
                else:
                    temp_list.append(rows[compound_id][key])
            counter += 1
            if counter < 100:
                treedata.Insert("", compound_id, "", temp_list, icon=temp_png)
            else:
                treedata.Insert("", compound_id, "", temp_list, icon="")

        return treedata, all_data, rows, counter


def compound_export(folder, compound_list):
    """
    Export the list of compounds to a CSV file

    :param folder: The destination folder for the data
    :type folder: str
    :param compound_list: A list of all the compounds that needs to be extrated from the freezer
    :type compound_list: list
    :return: A CSV file that can be used for the comPOUND freezer
    """

    csvw = CSVWriter()
    csvw.compound_freezer_writer(folder, compound_list)


def compound_counter(config, table):
    """
    Gets the amount of compounds for a specific table

    :param table: The table for the compounds
    :type table: str
    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :return: The number of compounds in the table
    :rtype: int
    """
    fd = FetchData(config)
    return len(fd.data_search(table, None))


def update_database(data, table, file_type, config):
    """
    Update the database with data. Both for adding data to the different tables, but updating tables with new values

    :param data: Output file from the plate_butler system, tube files for the comPOUND freezer, or other data.
    :type data: str
    :param file_type: If the file is a CSV file, it needs a specific file_type to know how to handle the file. as the
        CSV files are different depending on where they are coming from.
    :type file_type: str
    :param table: What table needs to be updated/where the data is going
    :type table: str
    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :return: Updated database with values
    """

    ad_db = AddData(config)
    ad_db.add_controller(table, data, file_type)


def purity_handler(folder, uv_one, uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak, ms_delta, ms_mode,
                   ms_threshold):
    """
    Takes raw data from LC/MS (UV and MS data) and mass from the database, per compound. and see if they can find the
    mass in the raw data, and then find the purity of the peak (based on retention time) for each compound

    :param folder: Folder with the raw-data
    :type folder: str
    :param uv_one: If it uses a single wavelength per compound or uses the whole PDA-range
    :type uv_one: bool
    :param uv_same_wavelength: if it uses the same wavelength, what wavelength that is
    :type uv_same_wavelength: bool
    :param wavelength: set to all, if there is no wavelength for each individuel compound
    :type wavelength: float
    :param uv_threshold: minimum threshold for the UV signal. anything below will be ignored
    :type uv_threshold: float
    :param rt_solvent_peak: retention time for the solvent peak
    :type rt_solvent_peak: float
    :param ms_delta: When looking for the MS data, how precise the mass should fit with the data.
    :type ms_delta: float
    :param ms_mode: if you are looking at the positive or negative. Have not been set up to look at both yet.
    :type ms_mode: str
    :param ms_threshold: minimum threshold for the MS signal. anything below will be ignored
    :type ms_threshold: float
    :return: An updated database with MS data. I think ??
    """

    lc_h = LCMSHandler()
    file_list = get_file_list(folder)
    compound_info = lc_h.lc_controller(file_list, uv_one, uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak,
                                       ms_delta, ms_mode, ms_threshold)
    print("MISSING FILE TYPE!!! ")
    #update_database(compound_info, "purity_data", )


def draw_plate(config, graph, plate_type, well_data_dict, gui_tab, archive_plate=False, sample_layout=None, mapping=None
               , state_dict=None):
    """
    Draws different plate type in on a canvas/graph.

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param graph: The canvas/graph that is setup in sg.window
    :type graph: PySimpleGUI.PySimpleGUI.Graph
    :param plate_type: what platetype that it needs to draw. there are 3 options 96, 384 or 1536.
    :type plate_type: str
    :param well_dict: A dict over wells, this is used for drawing saved plate layouts. The dict hold information for
        what type each well is (sample, blank or paint) and the colour of the well to draw, or the value of the sample
        if the dict is from experimental data.
    :type well_dict: dict
    :param archive_plate: bool to see if it needs to draw a blank plate or a saved plate
    :type archive_plate: bool
    :param gui_tab: what tab the plate is drawn on. differet tabs differe sizes:
    :type gui_tab: str
    :param sample_layout: This is for single point, or multiple samples with same ID.
    :type sample_layout: str
    :param mapping: Information to colour wells in specific colours, depending on what state mapping is used.
        There are 3 states - state Mapping, heatmap and hit mapping
    :type mapping: dict
    :param state_dict: A dict over what state each sample is in
    :type state_dict: dict
    :return:
        - well_dict: a dict over the wells, name, state, colour and number.
        - min_x: coordinate boundaries for the plate on the canvas
        - min_y: coordinate boundaries for the plate on the canvas
        - max_x: coordinate boundaries for the plate on the canvas
        - max_y: coordinate boundaries for the plate on the canvas
    :rtype:
        - dict
        - int
        - int
        - int
        - int
    """
    if mapping and mapping["mapping"] == "Heatmap":

        heatmap = Heatmap()

        heatmap_dict = heatmap.dict_convert(well_data_dict, state_dict, mapping["states"])

        colour_dict, well_percentile, max_values, min_values = heatmap.heatmap_colours(heatmap_dict, mapping["percentile"], mapping["colours"])

    well_dict = {}
    graph.erase()
    if gui_tab == "bio":
        well_size = 20
        start_x = 5
        start_y = 165
    elif gui_tab == "bio_exp":
        well_size = 20
        start_x = 5
        start_y = 165
    else:
        well_size = 40
        start_x = 10
        start_y = 335

    fill_colour = config["plate_colouring"]["empty"]
    line_colour = "black"
    well_state = "empty"
    size = {"plate_96": well_size, "plate_384": well_size / 2, "plate_1536": well_size / 4}
    start_x = start_x + size[plate_type]
    rows = {"plate_96": 12, "plate_384": 24, "plate_1536": 48}
    columns = {"plate_96": 8, "plate_384": 16, "plate_1536": 32}
    well_id_col = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF"]
    sample_layout_dict = {
        "single point": 1,
        "duplicate": 2,
        "triplicate": 3
    }
    counter = 0
    sample_counter = 0
    group = 1

    for row in range(rows[plate_type]):
        for column in range(columns[plate_type]):
            bottom_left = (start_x + row * size[plate_type],
                           start_y - column * size[plate_type])
            top_right = (bottom_left[0] - size[plate_type],
                         bottom_left[1] - size[plate_type])
            well_id = f"{well_id_col[column]}{row+1}"
            if archive_plate:
                counter += 1
                # print(well_dict)
                well_state = well_data_dict[well_id]["state"]
                fill_colour = config["plate_colouring"][well_state]

            if sample_layout and sample_layout != "single point":
                if well_state == "sample":
                    sample_counter += 1
                    temp_colour = group % 200
                    if group % 2 == 0:
                        fill_colour = f"#FFFF{format(temp_colour, '02x')}"
                    else:
                        fill_colour = f"#FF{format(temp_colour, '02x')}FF"
                    if sample_counter % sample_layout_dict[sample_layout] == 0:
                        group += 1
            else:
                group = counter

            if mapping:
                if mapping["mapping"] == "Heatmap":
                    if state_dict[well_id]["state"] in mapping["states"]:
                        try:
                            fill_colour = heatmap.get_well_colour(colour_dict, well_percentile, well_data_dict, well_id)
                        except ZeroDivisionError:
                            fill_colour = "#FFFFFF"
                    else:
                        fill_colour = "#FFFFFF"
                elif mapping["mapping"] == "Hit Map":

                    if state_dict[well_id]["state"] in mapping["states"]:
                        if mapping["lower_bound_start"] < well_data_dict[well_id] < mapping["lower_bound_end"]:
                            fill_colour = mapping["low_colour"]
                        elif mapping["middle_bound_start"] < well_data_dict[well_id] < mapping["middle_bound_end"]:
                            fill_colour = mapping["mid_colour"]
                        elif mapping["higher_bound_start"] < well_data_dict[well_id] < mapping["higher_bound_end"]:
                            fill_colour = mapping["high_colour"]
                        else:
                            fill_colour = "#FFFFFF"
                    else:
                        fill_colour = "#FFFFFF"

            temp_well = graph.DrawRectangle(bottom_left, top_right, line_color=line_colour, fill_color=fill_colour)
            well_dict[temp_well] = {}
            well_dict[temp_well]["group"] = group
            well_dict[temp_well]["well_id"] = well_id
            well_dict[temp_well]["state"] = well_state
            well_dict[temp_well]["colour"] = fill_colour

    min_x = start_x - size[plate_type]
    min_y = start_y - (columns[plate_type] * size[plate_type])
    max_x = start_x + (rows[plate_type] * size[plate_type])-size[plate_type]
    max_y = start_y

    return well_dict, min_x, min_y, max_x, max_y


# def bio_data(config, folder, well_states_report, plate_analysis_dict, plate_layout, z_prime_calc, heatmap_colours):
#     bioa = BIOAnalyser(config, well_states_report, plate_analysis_dict, heatmap_colours)
#     file_list = get_file_list(folder)
#
#     all_plates_data = {}
#     for files in file_list:
#         all_data, well_row_col, well_type, barcode = original_data_dict(files, plate_layout)
#         if not all_data:
#             return False
#
#         all_plates_data[barcode] = bioa.bio_data_controller(files, plate_layout, all_data, well_row_col, well_type
#                                                             , z_prime_calc)
#
#     return True, all_plates_data


def bio_data(config, folder, plate_layout, bio_plate_report_setup, analysis, write_to_excel=True):
    """
    Handles the Bio data.

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param folder: The folder where the raw data is located
    :type folder: str
    :param plate_layout: The layout for the plate with values for each well, what state they are in
    :type plate_layout: dict
    :param bio_plate_report_setup: The setup for what is included in the report
    :type bio_plate_report_setup: dict
    :param analysis: The analysis method
    :type analysis: str
    :return: All the data for the plates raw data, and their calculations
    :rtype: dict
    """
    # needs to reformat plate-layout to use well ID instead of numbers...
    bioa = BIOAnalyser(config, bio_plate_report_setup)
    file_list = get_file_list(folder)

    all_plates_data = {}
    for files in file_list:
        all_data, well_row_col, well_type, barcode, date = original_data_dict(files, plate_layout)
        if not all_data:
            return False

        all_plates_data[barcode] = bioa.bio_data_controller(files, plate_layout, all_data, well_row_col, well_type,
                                                            analysis, write_to_excel)

    return True, all_plates_data, date


def bio_full_report(analyse_method, all_plate_data, final_report_setup, output_folder, final_report_name):
    """
    Writes the final report for the bio data

    :param analyse_method: The analysed method used for the data
    :type analyse_method: str
    :param all_plate_data: All the data for all the plates, raw and calculations
    :type all_plate_data: dict
    :param final_report_setup: The settings for the report
    :type final_report_name: dict
    :param output_folder: The output folder, where the final report ends up
    :type output_folder: str
    :param final_report_name: The name for the report
    :type final_report_name: str
    :return: A excel report file with all the data
    """

    output_file = f"{output_folder}/{final_report_name}.xlsx"
    bio_final_report_controller(analyse_method, all_plate_data, output_file, final_report_setup)


def mp_production_2d_to_pb_simulate(folder_output, barcodes_2d, mp_name, trans_vol):
    """
    A simulation modul, for simulating output data

    :param folder_output: Output folder
    :type folder_output: str
    :param barcodes_2d: The folder with the 2D barcodes
    :type barcodes_2d: str
    :param mp_name: The name used for the MotherPlates
    :type mp_name: str
    :param trans_vol: The amount of volume to transferee
    :type trans_vol: float
    :return: CSV file resembling the one produced by the PB
    """
    barcodes_2d_files = get_file_list(barcodes_2d)
    csvc = CSVConverter()
    csvc.mp_in_to_out(folder_output, barcodes_2d_files, mp_name, trans_vol)


def compound_freezer_to_2d_simulate(tube_file, output_folder):
    """
    A simulation modul, for simulating output data

    :param tube_file: The CSV file with all the tube ID's for the comPOUND freezer
    :type tube_file: str
    :param output_folder: The output folder for the CSV files
    :type output_folder: str
    :return: A lot of CSV files. 1 per 96 compounds
    """
    csv_w = CSVWriter()
    csv_r = CSVReader
    tube_dict = csv_r.tube_list_to_dict(tube_file)
    csv_w.compound_freezer_to_2d_csv_simulate(tube_dict, output_folder)


def bio_experiment_to_database(assay_name, plate_data, plate_layout, date, responsible, config, bio_files):
    fd = FetchData(config)

    table_name = "bio_experiment"

    raw_data = f"{assay_name}_{date}"
    exp_id = fd.get_number_of_rows(table_name) + 1

    data_dict = {
        "exp_id": exp_id,
        "assay_name": assay_name,
        "raw_data": raw_data,
        "plate_layout": plate_layout,
        "responsible": responsible,
        "date": date
    }
    temp_dict = {raw_data: plate_data}
    dict_writer(bio_files, temp_dict)
    update_database(data_dict, table_name, None, config)


def grab_table_data(config, table_name, search_limiter):
    fd = FetchData(config)

    rows = fd.data_search(table_name, search_limiter)

    all_data = []
    headlines = []

    for row in rows:
        temp_data = []
        for data in rows[row]:
            headlines.append(data)
            temp_data.append(rows[row][data])

        all_data.append(temp_data)

    return all_data, headlines


def update_bio_info_values(values, window, plate_bio_info):
    temp_plate_name = values["-BIO_INFO_PLATES-"]
    temp_analyse_method = values["-BIO_INFO_ANALYSE_METHOD-"]
    temp_state = values["-BIO_INFO_STATES-"]

    window["-INFO_BIO_AVG-"].update(
        value=plate_bio_info[temp_plate_name]["calculations"][temp_analyse_method][temp_state]["avg"])
    window["-INFO_BIO_STDEV-"].update(
        value=plate_bio_info[temp_plate_name]["calculations"][temp_analyse_method][temp_state]["stdev"])
    window["-INFO_BIO_Z_PRIME-"].update(value=plate_bio_info[temp_plate_name]["calculations"]["other"]["z_prime"])


def sub_settings_matrix(data_dict, calc, method, state):
    values = {}
    temp_plate_name = ["", ""]
    for plates in data_dict:
        temp_plate_name.append(plates)
        if state:
            values[plates] = data_dict[plates]["calculations"][method][state][calc]
        else:
            values[plates] = data_dict[plates]["calculations"]["other"][calc]

    # Writes name in headers
    table_data = [temp_plate_name]

    # Writes the first row of data
    temp_row_data = []
    for index, plates in enumerate(values):
        if index == 0:
            temp_row_data.append("")
            temp_row_data.append("")
        temp_row_data.append(values[plates])
    table_data.append(temp_row_data)

    # Writes the rest of the Matrix
    for index_row, plate_row in enumerate(values):
        temp_row_data = []
        for index_col, plate_col in enumerate(values):
            #  writes plate names in column 1
            if index_col == 0:
                temp_row_data.append(plate_row)
                temp_row_data.append(values[plate_row])
            try:
                temp_value = (values[plate_col] / values[plate_row]) * 100
                temp_value = round(temp_value, 2)
            except ZeroDivisionError:
                temp_value = ""
            temp_row_data.append(temp_value)

        table_data.append(temp_row_data)

    display_columns = []
    for x in range(len(table_data)):
        display_columns.append(matrix_header[x])

    return table_data, display_columns


def sub_settings_list(data_dict, method, state, calc):

    row_data = []
    for plates in data_dict:
        temp_row_data = []
        if calc != "z_prime":
            temp_row_data.append(plates)
            temp_row_data.append(data_dict[plates]["calculations"][method][state][calc])
        else:
            temp_row_data.append(plates)
            temp_row_data.append(data_dict[plates]["calculations"]["other"][calc])
        row_data.append(temp_row_data)

    return row_data


def sub_settings_plate_overview(data_dict, method, plate, state):
    row_data = []
    for methods in data_dict[plate]["calculations"]:
        include_method = True
        if methods in method:
            for states in data_dict[plate]["calculations"][methods]:
                include_state = True
                if states in state:
                    for calc in data_dict[plate]["calculations"][methods][states]:
                        if include_method:
                            temp_row_data = [methods]
                        else:
                            temp_row_data = [[]]

                        if include_state:
                            temp_row_data.append(states)
                        else:
                            temp_row_data.append([])
                        temp_row_data.append(calc)
                        temp_row_data.append(data_dict[plate]["calculations"][methods][states][calc])
                        row_data.append(temp_row_data)
                        include_method = False
                        include_state = False

    for calc in data_dict[plate]["calculations"]["other"]:
        temp_row_data = [[], calc, [], data_dict[plate]["calculations"]["other"][calc]]
        row_data.append(temp_row_data)

    return row_data


def sub_settings_overview(data_dict, method, state):
    row_data_avg = []
    row_data_stdev = []

    for plates in data_dict:
        for calc in data_dict[plates]["calculations"][method][state]:
            if calc == "avg":
                temp_row_avg = [plates, data_dict[plates]["calculations"][method][state][calc]]
                row_data_avg.append(temp_row_avg)
            elif calc == "stdev":
                temp_row_stdev = [plates, data_dict[plates]["calculations"][method][state][calc]]
                row_data_stdev.append(temp_row_stdev)

    row_data_z_prime, _, _ = listing_z_prime(data_dict)

    return row_data_avg, row_data_stdev, row_data_z_prime


def listing_z_prime(data_dict):
    row_data_z_prime = []
    z_prime_dict = {}
    z_prime_values = []
    for plates in data_dict:
        for calc in data_dict[plates]["calculations"]["other"]:
            temp_row_z_prime = [plates, data_dict[plates]["calculations"]["other"][calc]]
            z_prime_dict[data_dict[plates]["calculations"]["other"][calc]] = plates
            z_prime_values.append(data_dict[plates]["calculations"]["other"][calc])

        row_data_z_prime.append(temp_row_z_prime)

    return row_data_z_prime, z_prime_dict, z_prime_values


def sub_settings_z_prime(data_dict):
    row_data_z_prime, z_prime_dict, z_prime_values = listing_z_prime(data_dict)

    z_prime_max_value = max(z_prime_values)
    z_prime_min_value = min(z_prime_values)

    z_prime_max_barcode = z_prime_dict[z_prime_max_value]
    z_prime_min_barcode = z_prime_dict[z_prime_min_value]

    return row_data_z_prime, z_prime_max_barcode, z_prime_max_value, z_prime_min_barcode, z_prime_min_value


def sub_settings_hit_list(data_dict, plate, method, state, state_dict, pora_thresholds):

    row_data_low = []
    row_data_mid = []
    row_data_high = []

    for well in data_dict[plate]["plates"][method]["wells"]:
        if isinstance(well, str):
            if state == state_dict[well]["state"]:
                well_value = data_dict[plate]["plates"][method]["wells"][well]
                if pora_thresholds["low"]["min"] < well_value < pora_thresholds["low"]["max"]:
                    temp_row_data = [well, well_value]
                    row_data_low.append(temp_row_data)
                if pora_thresholds["mid"]["min"] < well_value < pora_thresholds["mid"]["max"]:
                    temp_row_data = [well, well_value]
                    row_data_mid.append(temp_row_data)
                if pora_thresholds["high"]["min"] < well_value < pora_thresholds["high"]["max"]:
                    temp_row_data = [well, well_value]
                    row_data_high.append(temp_row_data)

    return row_data_low, row_data_mid, row_data_high


def dp_creator(plate_layout, sample_amount, mp_data, transferee_volume, dp_name, output_folder):
    csv_w = CSVWriter()

    dp_layout = plate_layout_to_well_ditc(plate_layout)
    # generate a dict for Daughter_Plates
    dp_dict = daughter_plate_generator(mp_data, sample_amount, dp_name, dp_layout, transferee_volume)

    # generate CSV-file for PlateButler
    csv_w.dp_writer(dp_dict, output_folder)

    # Generate list over mp needed
    csv_w.plate_list_writer(mp_data, output_folder)


def update_plate_table(compound_id, config):
    plate_tables = {"compound_mp": "MP", "compound_dp": "DP"}

    search_limiter_plates = {"compound_id": {"value": compound_id,
                                             "operator": "=",
                                             "target_column": "compound_id",
                                             "use": True}}
    plate_data = []
    for tables in plate_tables:
        temp_data = []
        all_data_plate, _ = grab_table_data(config, tables, search_limiter_plates)
        if all_data_plate:
            all_data_plate = all_data_plate[0]
            if tables == "compound_mp":
                temp_data.append(all_data_plate[1])
                temp_data.append(plate_tables[tables])
                temp_data.append(all_data_plate[2])
                temp_data.append(all_data_plate[3])
                temp_data.append(all_data_plate[4])
            elif tables == "compound_dp":
                temp_data.append(all_data_plate[3])
                temp_data.append(plate_tables[tables])
                temp_data.append(all_data_plate[4])
                temp_data.append(all_data_plate[5])
                temp_data.append(all_data_plate[6])

        plate_data.append(temp_data)

    return plate_data


def set_colours(window, reports):
    """
    Update all the input colour fields with new colours, after changes in the settings.
    :param window: The sg window
    :type window: PySimpleGUI.PySimpleGUI.Window
    :param reports: All the settings from the menu
    :type reports: dict
    :return:
    """
    _, bio_plate_report_setup, ms, simple_settings = reports

    window["-PLATE_LAYOUT_COLOUR_BOX_SAMPLE-"].\
        update(background_color=simple_settings["plate_colouring"]["sample"])
    window["-PLATE_LAYOUT_COLOUR_BOX_BLANK-"].\
        update(background_color=simple_settings["plate_colouring"]["blank"])
    window["-PLATE_LAYOUT_COLOUR_BOX_NAX-"].\
        update(background_color=simple_settings["plate_colouring"]["max"])
    window["-PLATE_LAYOUT_COLOUR_BOX_MINIMUM-"].\
        update(background_color=simple_settings["plate_colouring"]["minimum"])
    window["-PLATE_LAYOUT_COLOUR_BOX_POSITIVE-"].\
        update(background_color=simple_settings["plate_colouring"]["positive"])
    window["-PLATE_LAYOUT_COLOUR_BOX_NEGATIVE-"].\
        update(background_color=simple_settings["plate_colouring"]["negative"])
    window["-PLATE_LAYOUT_COLOUR_BOX_EMPTY-"].\
        update(background_color=simple_settings["plate_colouring"]["empty"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_SAMPLE-"].\
        update(background_color=simple_settings["plate_colouring"]["sample"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_BLANK-"].\
        update(background_color=simple_settings["plate_colouring"]["blank"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_NAX-"].\
        update(background_color=simple_settings["plate_colouring"]["max"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_MINIMUM-"].\
        update(background_color=simple_settings["plate_colouring"]["minimum"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_POSITIVE-"].\
        update(background_color=simple_settings["plate_colouring"]["positive"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_NEGATIVE-"].\
        update(background_color=simple_settings["plate_colouring"]["negative"])
    window["-BIO_PLATE_LAYOUT_COLOUR_BOX_EMPTY-"].\
        update(background_color=simple_settings["plate_colouring"]["empty"])

    window["-BIO_INFO_HIT_MAP_LOW_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["heatmap_colours"]["low"])
    window["-BIO_INFO_HIT_MAP_MID_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["heatmap_colours"]["mid"])
    window["-BIO_INFO_HIT_MAP_HIGH_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["heatmap_colours"]["high"])
    window["-BIO_INFO_HEATMAP_LOW_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["pora_threshold"]["colour"]["low"])
    window["-BIO_INFO_HEATMAP_MID_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["pora_threshold"]["colour"]["mid"])
    window["-BIO_INFO_HEATMAP_HIGH_COLOUR_BOX-"].\
        update(background_color=bio_plate_report_setup["pora_threshold"]["colour"]["high"])


def plate_layout_to_excel(well_dict, name, folder):
    # for index, plate in enumerate(well_dict):
    #     if index == 0:
    well_col_row, well_type = well_row_col_type(well_dict)
    plate_layout = plate_layout_re_formate(well_dict)

    export_plate_layout(plate_layout, well_col_row, name, folder)


def import_ms_data(folder, add_to_database, config):

    file_list = get_file_list(folder)
    purity_data = dm_controller(file_list)

    samples = []
    table_data = []
    for sample in purity_data:
        samples.append(sample)
        temp_data = []
        for data in purity_data[sample]:
            temp_data.append(purity_data[sample][data])
        table_data.append(temp_data)

    if add_to_database:
        batch_dict = {}
        today = date.today()
        today = today.strftime("%m_%Y")
        path = f"{config['folders']['main_output_folder']}/purity_data_{today}"
        batch_list = []
        for samples in purity_data:

            batch_dict[purity_data[samples]["batch"]] = {"batch": purity_data[samples]["batch"],
                                                         "date": purity_data[samples]["date"]}

            for batch in batch_dict:
                # makes sure that only new batches are added to the database
                if batch not in batch_list:
                    update_database(batch_dict[batch], "lc_experiment", None, config)
                    batch_list.append(batch)


            temp_file_date = {}
            temp_file_date[f"{purity_data[samples]['sample']}_{purity_data[samples]['batch']}"] = {
                "uv": purity_data[samples]["uv"],
                "ms_neg": purity_data[samples]["ms_neg"],
                "ms_pos": purity_data[samples]["ms_pos"]}

            # Writes UV and MS data to a separated file. Name based on sample_batch.
            df_writer(path, temp_file_date)
            temp_data_ditc = {"row_id": purity_data[samples]["row_id"],
                              "sample": purity_data[samples]["sample"],
                              "batch": purity_data[samples]["batch"],
                              "method": purity_data[samples]["method"],
                              "file_name": path,
                              "date": purity_data[samples]["date"]}

            update_database(temp_data_ditc, "lc_raw", None, config)

            # Makes a dict of batches, for adding to the batch database



    return table_data, samples

def purity_plotting(method, samples):
    ...


if __name__ == "__main__":
    ...
    config = configparser.ConfigParser()
    config.read("config.ini")
    # well_states_report = {'sample': True, 'blank': False, 'max': False, 'minimum': False, 'positive': False, 'negative': False, 'empty': False}
    # plate_analysis_dict = {'original': {'used': True, 'methode': org, 'heatmap': False}, 'normalised': {'used': True, 'methode': norm, 'heatmap': False}, 'pora': {'used': True, 'methode': pora, 'heatmap': False}}
    # plate_layout = {'well_layout': {1: {'well_id': 'A1', 'state': 'empty', 'colour': 'blue'}, 2: {'well_id': 'B1', 'state': 'empty', 'colour': 'blue'}, 3: {'well_id': 'C1', 'state': 'empty', 'colour': 'blue'}, 4: {'well_id': 'D1', 'state': 'empty', 'colour': 'blue'}, 5: {'well_id': 'E1', 'state': 'empty', 'colour': 'blue'}, 6: {'well_id': 'F1', 'state': 'empty', 'colour': 'blue'}, 7: {'well_id': 'G1', 'state': 'empty', 'colour': 'blue'}, 8: {'well_id': 'H1', 'state': 'empty', 'colour': 'blue'}, 9: {'well_id': 'I1', 'state': 'empty', 'colour': 'blue'}, 10: {'well_id': 'J1', 'state': 'empty', 'colour': 'blue'}, 11: {'well_id': 'K1', 'state': 'empty', 'colour': 'blue'}, 12: {'well_id': 'L1', 'state': 'empty', 'colour': 'blue'}, 13: {'well_id': 'M1', 'state': 'empty', 'colour': 'blue'}, 14: {'well_id': 'N1', 'state': 'empty', 'colour': 'blue'}, 15: {'well_id': 'O1', 'state': 'empty', 'colour': 'blue'}, 16: {'well_id': 'P1', 'state': 'empty', 'colour': 'blue'}, 17: {'well_id': 'A2', 'state': 'empty', 'colour': 'blue'}, 18: {'well_id': 'B2', 'state': 'max', 'colour': 'purple'}, 19: {'well_id': 'C2', 'state': 'max', 'colour': 'purple'}, 20: {'well_id': 'D2', 'state': 'max', 'colour': 'purple'}, 21: {'well_id': 'E2', 'state': 'max', 'colour': 'purple'}, 22: {'well_id': 'F2', 'state': 'max', 'colour': 'purple'}, 23: {'well_id': 'G2', 'state': 'max', 'colour': 'purple'}, 24: {'well_id': 'H2', 'state': 'max', 'colour': 'purple'}, 25: {'well_id': 'I2', 'state': 'max', 'colour': 'purple'}, 26: {'well_id': 'J2', 'state': 'max', 'colour': 'purple'}, 27: {'well_id': 'K2', 'state': 'max', 'colour': 'purple'}, 28: {'well_id': 'L2', 'state': 'max', 'colour': 'purple'}, 29: {'well_id': 'M2', 'state': 'max', 'colour': 'purple'}, 30: {'well_id': 'N2', 'state': 'max', 'colour': 'purple'}, 31: {'well_id': 'O2', 'state': 'empty', 'colour': 'blue'}, 32: {'well_id': 'P2', 'state': 'empty', 'colour': 'blue'}, 33: {'well_id': 'A3', 'state': 'empty', 'colour': 'blue'}, 34: {'well_id': 'B3', 'state': 'sample', 'colour': 'orange'}, 35: {'well_id': 'C3', 'state': 'sample', 'colour': 'orange'}, 36: {'well_id': 'D3', 'state': 'sample', 'colour': 'orange'}, 37: {'well_id': 'E3', 'state': 'sample', 'colour': 'orange'}, 38: {'well_id': 'F3', 'state': 'sample', 'colour': 'orange'}, 39: {'well_id': 'G3', 'state': 'sample', 'colour': 'orange'}, 40: {'well_id': 'H3', 'state': 'sample', 'colour': 'orange'}, 41: {'well_id': 'I3', 'state': 'sample', 'colour': 'orange'}, 42: {'well_id': 'J3', 'state': 'sample', 'colour': 'orange'}, 43: {'well_id': 'K3', 'state': 'sample', 'colour': 'orange'}, 44: {'well_id': 'L3', 'state': 'sample', 'colour': 'orange'}, 45: {'well_id': 'M3', 'state': 'sample', 'colour': 'orange'}, 46: {'well_id': 'N3', 'state': 'sample', 'colour': 'orange'}, 47: {'well_id': 'O3', 'state': 'empty', 'colour': 'blue'}, 48: {'well_id': 'P3', 'state': 'empty', 'colour': 'blue'}, 49: {'well_id': 'A4', 'state': 'empty', 'colour': 'blue'}, 50: {'well_id': 'B4', 'state': 'sample', 'colour': 'orange'}, 51: {'well_id': 'C4', 'state': 'sample', 'colour': 'orange'}, 52: {'well_id': 'D4', 'state': 'sample', 'colour': 'orange'}, 53: {'well_id': 'E4', 'state': 'sample', 'colour': 'orange'}, 54: {'well_id': 'F4', 'state': 'sample', 'colour': 'orange'}, 55: {'well_id': 'G4', 'state': 'sample', 'colour': 'orange'}, 56: {'well_id': 'H4', 'state': 'sample', 'colour': 'orange'}, 57: {'well_id': 'I4', 'state': 'sample', 'colour': 'orange'}, 58: {'well_id': 'J4', 'state': 'sample', 'colour': 'orange'}, 59: {'well_id': 'K4', 'state': 'sample', 'colour': 'orange'}, 60: {'well_id': 'L4', 'state': 'sample', 'colour': 'orange'}, 61: {'well_id': 'M4', 'state': 'sample', 'colour': 'orange'}, 62: {'well_id': 'N4', 'state': 'sample', 'colour': 'orange'}, 63: {'well_id': 'O4', 'state': 'empty', 'colour': 'blue'}, 64: {'well_id': 'P4', 'state': 'empty', 'colour': 'blue'}, 65: {'well_id': 'A5', 'state': 'empty', 'colour': 'blue'}, 66: {'well_id': 'B5', 'state': 'sample', 'colour': 'orange'}, 67: {'well_id': 'C5', 'state': 'sample', 'colour': 'orange'}, 68: {'well_id': 'D5', 'state': 'sample', 'colour': 'orange'}, 69: {'well_id': 'E5', 'state': 'sample', 'colour': 'orange'}, 70: {'well_id': 'F5', 'state': 'sample', 'colour': 'orange'}, 71: {'well_id': 'G5', 'state': 'sample', 'colour': 'orange'}, 72: {'well_id': 'H5', 'state': 'sample', 'colour': 'orange'}, 73: {'well_id': 'I5', 'state': 'sample', 'colour': 'orange'}, 74: {'well_id': 'J5', 'state': 'sample', 'colour': 'orange'}, 75: {'well_id': 'K5', 'state': 'sample', 'colour': 'orange'}, 76: {'well_id': 'L5', 'state': 'sample', 'colour': 'orange'}, 77: {'well_id': 'M5', 'state': 'sample', 'colour': 'orange'}, 78: {'well_id': 'N5', 'state': 'sample', 'colour': 'orange'}, 79: {'well_id': 'O5', 'state': 'empty', 'colour': 'blue'}, 80: {'well_id': 'P5', 'state': 'empty', 'colour': 'blue'}, 81: {'well_id': 'A6', 'state': 'empty', 'colour': 'blue'}, 82: {'well_id': 'B6', 'state': 'sample', 'colour': 'orange'}, 83: {'well_id': 'C6', 'state': 'sample', 'colour': 'orange'}, 84: {'well_id': 'D6', 'state': 'sample', 'colour': 'orange'}, 85: {'well_id': 'E6', 'state': 'sample', 'colour': 'orange'}, 86: {'well_id': 'F6', 'state': 'sample', 'colour': 'orange'}, 87: {'well_id': 'G6', 'state': 'sample', 'colour': 'orange'}, 88: {'well_id': 'H6', 'state': 'sample', 'colour': 'orange'}, 89: {'well_id': 'I6', 'state': 'sample', 'colour': 'orange'}, 90: {'well_id': 'J6', 'state': 'sample', 'colour': 'orange'}, 91: {'well_id': 'K6', 'state': 'sample', 'colour': 'orange'}, 92: {'well_id': 'L6', 'state': 'sample', 'colour': 'orange'}, 93: {'well_id': 'M6', 'state': 'sample', 'colour': 'orange'}, 94: {'well_id': 'N6', 'state': 'sample', 'colour': 'orange'}, 95: {'well_id': 'O6', 'state': 'empty', 'colour': 'blue'}, 96: {'well_id': 'P6', 'state': 'empty', 'colour': 'blue'}, 97: {'well_id': 'A7', 'state': 'empty', 'colour': 'blue'}, 98: {'well_id': 'B7', 'state': 'sample', 'colour': 'orange'}, 99: {'well_id': 'C7', 'state': 'sample', 'colour': 'orange'}, 100: {'well_id': 'D7', 'state': 'sample', 'colour': 'orange'}, 101: {'well_id': 'E7', 'state': 'sample', 'colour': 'orange'}, 102: {'well_id': 'F7', 'state': 'sample', 'colour': 'orange'}, 103: {'well_id': 'G7', 'state': 'sample', 'colour': 'orange'}, 104: {'well_id': 'H7', 'state': 'sample', 'colour': 'orange'}, 105: {'well_id': 'I7', 'state': 'sample', 'colour': 'orange'}, 106: {'well_id': 'J7', 'state': 'sample', 'colour': 'orange'}, 107: {'well_id': 'K7', 'state': 'sample', 'colour': 'orange'}, 108: {'well_id': 'L7', 'state': 'sample', 'colour': 'orange'}, 109: {'well_id': 'M7', 'state': 'sample', 'colour': 'orange'}, 110: {'well_id': 'N7', 'state': 'sample', 'colour': 'orange'}, 111: {'well_id': 'O7', 'state': 'empty', 'colour': 'blue'}, 112: {'well_id': 'P7', 'state': 'empty', 'colour': 'blue'}, 113: {'well_id': 'A8', 'state': 'empty', 'colour': 'blue'}, 114: {'well_id': 'B8', 'state': 'sample', 'colour': 'orange'}, 115: {'well_id': 'C8', 'state': 'sample', 'colour': 'orange'}, 116: {'well_id': 'D8', 'state': 'sample', 'colour': 'orange'}, 117: {'well_id': 'E8', 'state': 'sample', 'colour': 'orange'}, 118: {'well_id': 'F8', 'state': 'sample', 'colour': 'orange'}, 119: {'well_id': 'G8', 'state': 'sample', 'colour': 'orange'}, 120: {'well_id': 'H8', 'state': 'sample', 'colour': 'orange'}, 121: {'well_id': 'I8', 'state': 'sample', 'colour': 'orange'}, 122: {'well_id': 'J8', 'state': 'sample', 'colour': 'orange'}, 123: {'well_id': 'K8', 'state': 'sample', 'colour': 'orange'}, 124: {'well_id': 'L8', 'state': 'sample', 'colour': 'orange'}, 125: {'well_id': 'M8', 'state': 'sample', 'colour': 'orange'}, 126: {'well_id': 'N8', 'state': 'sample', 'colour': 'orange'}, 127: {'well_id': 'O8', 'state': 'empty', 'colour': 'blue'}, 128: {'well_id': 'P8', 'state': 'empty', 'colour': 'blue'}, 129: {'well_id': 'A9', 'state': 'empty', 'colour': 'blue'}, 130: {'well_id': 'B9', 'state': 'sample', 'colour': 'orange'}, 131: {'well_id': 'C9', 'state': 'sample', 'colour': 'orange'}, 132: {'well_id': 'D9', 'state': 'sample', 'colour': 'orange'}, 133: {'well_id': 'E9', 'state': 'sample', 'colour': 'orange'}, 134: {'well_id': 'F9', 'state': 'sample', 'colour': 'orange'}, 135: {'well_id': 'G9', 'state': 'sample', 'colour': 'orange'}, 136: {'well_id': 'H9', 'state': 'sample', 'colour': 'orange'}, 137: {'well_id': 'I9', 'state': 'sample', 'colour': 'orange'}, 138: {'well_id': 'J9', 'state': 'sample', 'colour': 'orange'}, 139: {'well_id': 'K9', 'state': 'sample', 'colour': 'orange'}, 140: {'well_id': 'L9', 'state': 'sample', 'colour': 'orange'}, 141: {'well_id': 'M9', 'state': 'sample', 'colour': 'orange'}, 142: {'well_id': 'N9', 'state': 'sample', 'colour': 'orange'}, 143: {'well_id': 'O9', 'state': 'empty', 'colour': 'blue'}, 144: {'well_id': 'P9', 'state': 'empty', 'colour': 'blue'}, 145: {'well_id': 'A10', 'state': 'empty', 'colour': 'blue'}, 146: {'well_id': 'B10', 'state': 'sample', 'colour': 'orange'}, 147: {'well_id': 'C10', 'state': 'sample', 'colour': 'orange'}, 148: {'well_id': 'D10', 'state': 'sample', 'colour': 'orange'}, 149: {'well_id': 'E10', 'state': 'sample', 'colour': 'orange'}, 150: {'well_id': 'F10', 'state': 'sample', 'colour': 'orange'}, 151: {'well_id': 'G10', 'state': 'sample', 'colour': 'orange'}, 152: {'well_id': 'H10', 'state': 'sample', 'colour': 'orange'}, 153: {'well_id': 'I10', 'state': 'sample', 'colour': 'orange'}, 154: {'well_id': 'J10', 'state': 'sample', 'colour': 'orange'}, 155: {'well_id': 'K10', 'state': 'sample', 'colour': 'orange'}, 156: {'well_id': 'L10', 'state': 'sample', 'colour': 'orange'}, 157: {'well_id': 'M10', 'state': 'sample', 'colour': 'orange'}, 158: {'well_id': 'N10', 'state': 'sample', 'colour': 'orange'}, 159: {'well_id': 'O10', 'state': 'empty', 'colour': 'blue'}, 160: {'well_id': 'P10', 'state': 'empty', 'colour': 'blue'}, 161: {'well_id': 'A11', 'state': 'empty', 'colour': 'blue'}, 162: {'well_id': 'B11', 'state': 'sample', 'colour': 'orange'}, 163: {'well_id': 'C11', 'state': 'sample', 'colour': 'orange'}, 164: {'well_id': 'D11', 'state': 'sample', 'colour': 'orange'}, 165: {'well_id': 'E11', 'state': 'sample', 'colour': 'orange'}, 166: {'well_id': 'F11', 'state': 'sample', 'colour': 'orange'}, 167: {'well_id': 'G11', 'state': 'sample', 'colour': 'orange'}, 168: {'well_id': 'H11', 'state': 'sample', 'colour': 'orange'}, 169: {'well_id': 'I11', 'state': 'sample', 'colour': 'orange'}, 170: {'well_id': 'J11', 'state': 'sample', 'colour': 'orange'}, 171: {'well_id': 'K11', 'state': 'sample', 'colour': 'orange'}, 172: {'well_id': 'L11', 'state': 'sample', 'colour': 'orange'}, 173: {'well_id': 'M11', 'state': 'sample', 'colour': 'orange'}, 174: {'well_id': 'N11', 'state': 'sample', 'colour': 'orange'}, 175: {'well_id': 'O11', 'state': 'empty', 'colour': 'blue'}, 176: {'well_id': 'P11', 'state': 'empty', 'colour': 'blue'}, 177: {'well_id': 'A12', 'state': 'empty', 'colour': 'blue'}, 178: {'well_id': 'B12', 'state': 'sample', 'colour': 'orange'}, 179: {'well_id': 'C12', 'state': 'sample', 'colour': 'orange'}, 180: {'well_id': 'D12', 'state': 'sample', 'colour': 'orange'}, 181: {'well_id': 'E12', 'state': 'sample', 'colour': 'orange'}, 182: {'well_id': 'F12', 'state': 'sample', 'colour': 'orange'}, 183: {'well_id': 'G12', 'state': 'sample', 'colour': 'orange'}, 184: {'well_id': 'H12', 'state': 'sample', 'colour': 'orange'}, 185: {'well_id': 'I12', 'state': 'sample', 'colour': 'orange'}, 186: {'well_id': 'J12', 'state': 'sample', 'colour': 'orange'}, 187: {'well_id': 'K12', 'state': 'sample', 'colour': 'orange'}, 188: {'well_id': 'L12', 'state': 'sample', 'colour': 'orange'}, 189: {'well_id': 'M12', 'state': 'sample', 'colour': 'orange'}, 190: {'well_id': 'N12', 'state': 'sample', 'colour': 'orange'}, 191: {'well_id': 'O12', 'state': 'empty', 'colour': 'blue'}, 192: {'well_id': 'P12', 'state': 'empty', 'colour': 'blue'}, 193: {'well_id': 'A13', 'state': 'empty', 'colour': 'blue'}, 194: {'well_id': 'B13', 'state': 'sample', 'colour': 'orange'}, 195: {'well_id': 'C13', 'state': 'sample', 'colour': 'orange'}, 196: {'well_id': 'D13', 'state': 'sample', 'colour': 'orange'}, 197: {'well_id': 'E13', 'state': 'sample', 'colour': 'orange'}, 198: {'well_id': 'F13', 'state': 'sample', 'colour': 'orange'}, 199: {'well_id': 'G13', 'state': 'sample', 'colour': 'orange'}, 200: {'well_id': 'H13', 'state': 'sample', 'colour': 'orange'}, 201: {'well_id': 'I13', 'state': 'sample', 'colour': 'orange'}, 202: {'well_id': 'J13', 'state': 'sample', 'colour': 'orange'}, 203: {'well_id': 'K13', 'state': 'sample', 'colour': 'orange'}, 204: {'well_id': 'L13', 'state': 'sample', 'colour': 'orange'}, 205: {'well_id': 'M13', 'state': 'sample', 'colour': 'orange'}, 206: {'well_id': 'N13', 'state': 'sample', 'colour': 'orange'}, 207: {'well_id': 'O13', 'state': 'empty', 'colour': 'blue'}, 208: {'well_id': 'P13', 'state': 'empty', 'colour': 'blue'}, 209: {'well_id': 'A14', 'state': 'empty', 'colour': 'blue'}, 210: {'well_id': 'B14', 'state': 'sample', 'colour': 'orange'}, 211: {'well_id': 'C14', 'state': 'sample', 'colour': 'orange'}, 212: {'well_id': 'D14', 'state': 'sample', 'colour': 'orange'}, 213: {'well_id': 'E14', 'state': 'sample', 'colour': 'orange'}, 214: {'well_id': 'F14', 'state': 'sample', 'colour': 'orange'}, 215: {'well_id': 'G14', 'state': 'sample', 'colour': 'orange'}, 216: {'well_id': 'H14', 'state': 'sample', 'colour': 'orange'}, 217: {'well_id': 'I14', 'state': 'sample', 'colour': 'orange'}, 218: {'well_id': 'J14', 'state': 'sample', 'colour': 'orange'}, 219: {'well_id': 'K14', 'state': 'sample', 'colour': 'orange'}, 220: {'well_id': 'L14', 'state': 'sample', 'colour': 'orange'}, 221: {'well_id': 'M14', 'state': 'sample', 'colour': 'orange'}, 222: {'well_id': 'N14', 'state': 'sample', 'colour': 'orange'}, 223: {'well_id': 'O14', 'state': 'empty', 'colour': 'blue'}, 224: {'well_id': 'P14', 'state': 'empty', 'colour': 'blue'}, 225: {'well_id': 'A15', 'state': 'empty', 'colour': 'blue'}, 226: {'well_id': 'B15', 'state': 'sample', 'colour': 'orange'}, 227: {'well_id': 'C15', 'state': 'sample', 'colour': 'orange'}, 228: {'well_id': 'D15', 'state': 'sample', 'colour': 'orange'}, 229: {'well_id': 'E15', 'state': 'sample', 'colour': 'orange'}, 230: {'well_id': 'F15', 'state': 'sample', 'colour': 'orange'}, 231: {'well_id': 'G15', 'state': 'sample', 'colour': 'orange'}, 232: {'well_id': 'H15', 'state': 'sample', 'colour': 'orange'}, 233: {'well_id': 'I15', 'state': 'sample', 'colour': 'orange'}, 234: {'well_id': 'J15', 'state': 'sample', 'colour': 'orange'}, 235: {'well_id': 'K15', 'state': 'sample', 'colour': 'orange'}, 236: {'well_id': 'L15', 'state': 'sample', 'colour': 'orange'}, 237: {'well_id': 'M15', 'state': 'sample', 'colour': 'orange'}, 238: {'well_id': 'N15', 'state': 'sample', 'colour': 'orange'}, 239: {'well_id': 'O15', 'state': 'empty', 'colour': 'blue'}, 240: {'well_id': 'P15', 'state': 'empty', 'colour': 'blue'}, 241: {'well_id': 'A16', 'state': 'empty', 'colour': 'blue'}, 242: {'well_id': 'B16', 'state': 'sample', 'colour': 'orange'}, 243: {'well_id': 'C16', 'state': 'sample', 'colour': 'orange'}, 244: {'well_id': 'D16', 'state': 'sample', 'colour': 'orange'}, 245: {'well_id': 'E16', 'state': 'sample', 'colour': 'orange'}, 246: {'well_id': 'F16', 'state': 'sample', 'colour': 'orange'}, 247: {'well_id': 'G16', 'state': 'sample', 'colour': 'orange'}, 248: {'well_id': 'H16', 'state': 'sample', 'colour': 'orange'}, 249: {'well_id': 'I16', 'state': 'sample', 'colour': 'orange'}, 250: {'well_id': 'J16', 'state': 'sample', 'colour': 'orange'}, 251: {'well_id': 'K16', 'state': 'sample', 'colour': 'orange'}, 252: {'well_id': 'L16', 'state': 'sample', 'colour': 'orange'}, 253: {'well_id': 'M16', 'state': 'sample', 'colour': 'orange'}, 254: {'well_id': 'N16', 'state': 'sample', 'colour': 'orange'}, 255: {'well_id': 'O16', 'state': 'empty', 'colour': 'blue'}, 256: {'well_id': 'P16', 'state': 'empty', 'colour': 'blue'}, 257: {'well_id': 'A17', 'state': 'empty', 'colour': 'blue'}, 258: {'well_id': 'B17', 'state': 'sample', 'colour': 'orange'}, 259: {'well_id': 'C17', 'state': 'sample', 'colour': 'orange'}, 260: {'well_id': 'D17', 'state': 'sample', 'colour': 'orange'}, 261: {'well_id': 'E17', 'state': 'sample', 'colour': 'orange'}, 262: {'well_id': 'F17', 'state': 'sample', 'colour': 'orange'}, 263: {'well_id': 'G17', 'state': 'sample', 'colour': 'orange'}, 264: {'well_id': 'H17', 'state': 'sample', 'colour': 'orange'}, 265: {'well_id': 'I17', 'state': 'sample', 'colour': 'orange'}, 266: {'well_id': 'J17', 'state': 'sample', 'colour': 'orange'}, 267: {'well_id': 'K17', 'state': 'sample', 'colour': 'orange'}, 268: {'well_id': 'L17', 'state': 'sample', 'colour': 'orange'}, 269: {'well_id': 'M17', 'state': 'sample', 'colour': 'orange'}, 270: {'well_id': 'N17', 'state': 'sample', 'colour': 'orange'}, 271: {'well_id': 'O17', 'state': 'empty', 'colour': 'blue'}, 272: {'well_id': 'P17', 'state': 'empty', 'colour': 'blue'}, 273: {'well_id': 'A18', 'state': 'empty', 'colour': 'blue'}, 274: {'well_id': 'B18', 'state': 'sample', 'colour': 'orange'}, 275: {'well_id': 'C18', 'state': 'sample', 'colour': 'orange'}, 276: {'well_id': 'D18', 'state': 'sample', 'colour': 'orange'}, 277: {'well_id': 'E18', 'state': 'sample', 'colour': 'orange'}, 278: {'well_id': 'F18', 'state': 'sample', 'colour': 'orange'}, 279: {'well_id': 'G18', 'state': 'sample', 'colour': 'orange'}, 280: {'well_id': 'H18', 'state': 'sample', 'colour': 'orange'}, 281: {'well_id': 'I18', 'state': 'sample', 'colour': 'orange'}, 282: {'well_id': 'J18', 'state': 'sample', 'colour': 'orange'}, 283: {'well_id': 'K18', 'state': 'sample', 'colour': 'orange'}, 284: {'well_id': 'L18', 'state': 'sample', 'colour': 'orange'}, 285: {'well_id': 'M18', 'state': 'sample', 'colour': 'orange'}, 286: {'well_id': 'N18', 'state': 'sample', 'colour': 'orange'}, 287: {'well_id': 'O18', 'state': 'empty', 'colour': 'blue'}, 288: {'well_id': 'P18', 'state': 'empty', 'colour': 'blue'}, 289: {'well_id': 'A19', 'state': 'empty', 'colour': 'blue'}, 290: {'well_id': 'B19', 'state': 'sample', 'colour': 'orange'}, 291: {'well_id': 'C19', 'state': 'sample', 'colour': 'orange'}, 292: {'well_id': 'D19', 'state': 'sample', 'colour': 'orange'}, 293: {'well_id': 'E19', 'state': 'sample', 'colour': 'orange'}, 294: {'well_id': 'F19', 'state': 'sample', 'colour': 'orange'}, 295: {'well_id': 'G19', 'state': 'sample', 'colour': 'orange'}, 296: {'well_id': 'H19', 'state': 'sample', 'colour': 'orange'}, 297: {'well_id': 'I19', 'state': 'sample', 'colour': 'orange'}, 298: {'well_id': 'J19', 'state': 'sample', 'colour': 'orange'}, 299: {'well_id': 'K19', 'state': 'sample', 'colour': 'orange'}, 300: {'well_id': 'L19', 'state': 'sample', 'colour': 'orange'}, 301: {'well_id': 'M19', 'state': 'sample', 'colour': 'orange'}, 302: {'well_id': 'N19', 'state': 'sample', 'colour': 'orange'}, 303: {'well_id': 'O19', 'state': 'empty', 'colour': 'blue'}, 304: {'well_id': 'P19', 'state': 'empty', 'colour': 'blue'}, 305: {'well_id': 'A20', 'state': 'empty', 'colour': 'blue'}, 306: {'well_id': 'B20', 'state': 'sample', 'colour': 'orange'}, 307: {'well_id': 'C20', 'state': 'sample', 'colour': 'orange'}, 308: {'well_id': 'D20', 'state': 'sample', 'colour': 'orange'}, 309: {'well_id': 'E20', 'state': 'sample', 'colour': 'orange'}, 310: {'well_id': 'F20', 'state': 'sample', 'colour': 'orange'}, 311: {'well_id': 'G20', 'state': 'sample', 'colour': 'orange'}, 312: {'well_id': 'H20', 'state': 'sample', 'colour': 'orange'}, 313: {'well_id': 'I20', 'state': 'sample', 'colour': 'orange'}, 314: {'well_id': 'J20', 'state': 'sample', 'colour': 'orange'}, 315: {'well_id': 'K20', 'state': 'sample', 'colour': 'orange'}, 316: {'well_id': 'L20', 'state': 'sample', 'colour': 'orange'}, 317: {'well_id': 'M20', 'state': 'sample', 'colour': 'orange'}, 318: {'well_id': 'N20', 'state': 'sample', 'colour': 'orange'}, 319: {'well_id': 'O20', 'state': 'empty', 'colour': 'blue'}, 320: {'well_id': 'P20', 'state': 'empty', 'colour': 'blue'}, 321: {'well_id': 'A21', 'state': 'empty', 'colour': 'blue'}, 322: {'well_id': 'B21', 'state': 'sample', 'colour': 'orange'}, 323: {'well_id': 'C21', 'state': 'sample', 'colour': 'orange'}, 324: {'well_id': 'D21', 'state': 'sample', 'colour': 'orange'}, 325: {'well_id': 'E21', 'state': 'sample', 'colour': 'orange'}, 326: {'well_id': 'F21', 'state': 'sample', 'colour': 'orange'}, 327: {'well_id': 'G21', 'state': 'sample', 'colour': 'orange'}, 328: {'well_id': 'H21', 'state': 'sample', 'colour': 'orange'}, 329: {'well_id': 'I21', 'state': 'sample', 'colour': 'orange'}, 330: {'well_id': 'J21', 'state': 'sample', 'colour': 'orange'}, 331: {'well_id': 'K21', 'state': 'sample', 'colour': 'orange'}, 332: {'well_id': 'L21', 'state': 'sample', 'colour': 'orange'}, 333: {'well_id': 'M21', 'state': 'sample', 'colour': 'orange'}, 334: {'well_id': 'N21', 'state': 'sample', 'colour': 'orange'}, 335: {'well_id': 'O21', 'state': 'empty', 'colour': 'blue'}, 336: {'well_id': 'P21', 'state': 'empty', 'colour': 'blue'}, 337: {'well_id': 'A22', 'state': 'empty', 'colour': 'blue'}, 338: {'well_id': 'B22', 'state': 'sample', 'colour': 'orange'}, 339: {'well_id': 'C22', 'state': 'sample', 'colour': 'orange'}, 340: {'well_id': 'D22', 'state': 'sample', 'colour': 'orange'}, 341: {'well_id': 'E22', 'state': 'sample', 'colour': 'orange'}, 342: {'well_id': 'F22', 'state': 'sample', 'colour': 'orange'}, 343: {'well_id': 'G22', 'state': 'sample', 'colour': 'orange'}, 344: {'well_id': 'H22', 'state': 'sample', 'colour': 'orange'}, 345: {'well_id': 'I22', 'state': 'sample', 'colour': 'orange'}, 346: {'well_id': 'J22', 'state': 'sample', 'colour': 'orange'}, 347: {'well_id': 'K22', 'state': 'sample', 'colour': 'orange'}, 348: {'well_id': 'L22', 'state': 'sample', 'colour': 'orange'}, 349: {'well_id': 'M22', 'state': 'sample', 'colour': 'orange'}, 350: {'well_id': 'N22', 'state': 'sample', 'colour': 'orange'}, 351: {'well_id': 'O22', 'state': 'empty', 'colour': 'blue'}, 352: {'well_id': 'P22', 'state': 'empty', 'colour': 'blue'}, 353: {'well_id': 'A23', 'state': 'empty', 'colour': 'blue'}, 354: {'well_id': 'B23', 'state': 'minimum', 'colour': 'yellow'}, 355: {'well_id': 'C23', 'state': 'minimum', 'colour': 'yellow'}, 356: {'well_id': 'D23', 'state': 'minimum', 'colour': 'yellow'}, 357: {'well_id': 'E23', 'state': 'minimum', 'colour': 'yellow'}, 358: {'well_id': 'F23', 'state': 'minimum', 'colour': 'yellow'}, 359: {'well_id': 'G23', 'state': 'minimum', 'colour': 'yellow'}, 360: {'well_id': 'H23', 'state': 'minimum', 'colour': 'yellow'}, 361: {'well_id': 'I23', 'state': 'minimum', 'colour': 'yellow'}, 362: {'well_id': 'J23', 'state': 'minimum', 'colour': 'yellow'}, 363: {'well_id': 'K23', 'state': 'minimum', 'colour': 'yellow'}, 364: {'well_id': 'L23', 'state': 'minimum', 'colour': 'yellow'}, 365: {'well_id': 'M23', 'state': 'minimum', 'colour': 'yellow'}, 366: {'well_id': 'N23', 'state': 'minimum', 'colour': 'yellow'}, 367: {'well_id': 'O23', 'state': 'empty', 'colour': 'blue'}, 368: {'well_id': 'P23', 'state': 'empty', 'colour': 'blue'}, 369: {'well_id': 'A24', 'state': 'empty', 'colour': 'blue'}, 370: {'well_id': 'B24', 'state': 'empty', 'colour': 'blue'}, 371: {'well_id': 'C24', 'state': 'empty', 'colour': 'blue'}, 372: {'well_id': 'D24', 'state': 'empty', 'colour': 'blue'}, 373: {'well_id': 'E24', 'state': 'empty', 'colour': 'blue'}, 374: {'well_id': 'F24', 'state': 'empty', 'colour': 'blue'}, 375: {'well_id': 'G24', 'state': 'empty', 'colour': 'blue'}, 376: {'well_id': 'H24', 'state': 'empty', 'colour': 'blue'}, 377: {'well_id': 'I24', 'state': 'empty', 'colour': 'blue'}, 378: {'well_id': 'J24', 'state': 'empty', 'colour': 'blue'}, 379: {'well_id': 'K24', 'state': 'empty', 'colour': 'blue'}, 380: {'well_id': 'L24', 'state': 'empty', 'colour': 'blue'}, 381: {'well_id': 'M24', 'state': 'empty', 'colour': 'blue'}, 382: {'well_id': 'N24', 'state': 'empty', 'colour': 'blue'}, 383: {'well_id': 'O24', 'state': 'empty', 'colour': 'blue'}, 384: {'well_id': 'P24', 'state': 'empty', 'colour': 'blue'}}, 'plate_type': 'plate_384'}
    plate_layout = {"Standard_384": {"well_layout": {"1": {"group": 1, "well_id": "A1", "state": "empty", "colour": "#1e0bc8"}, "2": {"group": 2, "well_id": "B1", "state": "empty", "colour": "#1e0bc8"}, "3": {"group": 3, "well_id": "C1", "state": "empty", "colour": "#1e0bc8"}, "4": {"group": 4, "well_id": "D1", "state": "empty", "colour": "#1e0bc8"}, "5": {"group": 5, "well_id": "E1", "state": "empty", "colour": "#1e0bc8"}, "6": {"group": 6, "well_id": "F1", "state": "empty", "colour": "#1e0bc8"}, "7": {"group": 7, "well_id": "G1", "state": "empty", "colour": "#1e0bc8"}, "8": {"group": 8, "well_id": "H1", "state": "empty", "colour": "#1e0bc8"}, "9": {"group": 9, "well_id": "I1", "state": "empty", "colour": "#1e0bc8"}, "10": {"group": 10, "well_id": "J1", "state": "empty", "colour": "#1e0bc8"}, "11": {"group": 11, "well_id": "K1", "state": "empty", "colour": "#1e0bc8"}, "12": {"group": 12, "well_id": "L1", "state": "empty", "colour": "#1e0bc8"}, "13": {"group": 13, "well_id": "M1", "state": "empty", "colour": "#1e0bc8"}, "14": {"group": 14, "well_id": "N1", "state": "empty", "colour": "#1e0bc8"}, "15": {"group": 15, "well_id": "O1", "state": "empty", "colour": "#1e0bc8"}, "16": {"group": 16, "well_id": "P1", "state": "empty", "colour": "#1e0bc8"}, "17": {"group": 17, "well_id": "A2", "state": "empty", "colour": "#1e0bc8"}, "18": {"group": 18, "well_id": "B2", "state": "max", "colour": "#790dc1"}, "19": {"group": 19, "well_id": "C2", "state": "max", "colour": "#790dc1"}, "20": {"group": 20, "well_id": "D2", "state": "max", "colour": "#790dc1"}, "21": {"group": 21, "well_id": "E2", "state": "max", "colour": "#790dc1"}, "22": {"group": 22, "well_id": "F2", "state": "max", "colour": "#790dc1"}, "23": {"group": 23, "well_id": "G2", "state": "max", "colour": "#790dc1"}, "24": {"group": 24, "well_id": "H2", "state": "max", "colour": "#790dc1"}, "25": {"group": 25, "well_id": "I2", "state": "max", "colour": "#790dc1"}, "26": {"group": 26, "well_id": "J2", "state": "max", "colour": "#790dc1"}, "27": {"group": 27, "well_id": "K2", "state": "max", "colour": "#790dc1"}, "28": {"group": 28, "well_id": "L2", "state": "max", "colour": "#790dc1"}, "29": {"group": 29, "well_id": "M2", "state": "max", "colour": "#790dc1"}, "30": {"group": 30, "well_id": "N2", "state": "max", "colour": "#790dc1"}, "31": {"group": 31, "well_id": "O2", "state": "empty", "colour": "#1e0bc8"}, "32": {"group": 32, "well_id": "P2", "state": "empty", "colour": "#1e0bc8"}, "33": {"group": 33, "well_id": "A3", "state": "empty", "colour": "#1e0bc8"}, "34": {"group": 34, "well_id": "B3", "state": "sample", "colour": "#ff00ff"}, "35": {"group": 35, "well_id": "C3", "state": "sample", "colour": "#ff00ff"}, "36": {"group": 36, "well_id": "D3", "state": "sample", "colour": "#ff00ff"}, "37": {"group": 37, "well_id": "E3", "state": "sample", "colour": "#ff00ff"}, "38": {"group": 38, "well_id": "F3", "state": "sample", "colour": "#ff00ff"}, "39": {"group": 39, "well_id": "G3", "state": "sample", "colour": "#ff00ff"}, "40": {"group": 40, "well_id": "H3", "state": "sample", "colour": "#ff00ff"}, "41": {"group": 41, "well_id": "I3", "state": "sample", "colour": "#ff00ff"}, "42": {"group": 42, "well_id": "J3", "state": "sample", "colour": "#ff00ff"}, "43": {"group": 43, "well_id": "K3", "state": "sample", "colour": "#ff00ff"}, "44": {"group": 44, "well_id": "L3", "state": "sample", "colour": "#ff00ff"}, "45": {"group": 45, "well_id": "M3", "state": "sample", "colour": "#ff00ff"}, "46": {"group": 46, "well_id": "N3", "state": "sample", "colour": "#ff00ff"}, "47": {"group": 47, "well_id": "O3", "state": "empty", "colour": "#1e0bc8"}, "48": {"group": 48, "well_id": "P3", "state": "empty", "colour": "#1e0bc8"}, "49": {"group": 49, "well_id": "A4", "state": "empty", "colour": "#1e0bc8"}, "50": {"group": 50, "well_id": "B4", "state": "sample", "colour": "#ff00ff"}, "51": {"group": 51, "well_id": "C4", "state": "sample", "colour": "#ff00ff"}, "52": {"group": 52, "well_id": "D4", "state": "sample", "colour": "#ff00ff"}, "53": {"group": 53, "well_id": "E4", "state": "sample", "colour": "#ff00ff"}, "54": {"group": 54, "well_id": "F4", "state": "sample", "colour": "#ff00ff"}, "55": {"group": 55, "well_id": "G4", "state": "sample", "colour": "#ff00ff"}, "56": {"group": 56, "well_id": "H4", "state": "sample", "colour": "#ff00ff"}, "57": {"group": 57, "well_id": "I4", "state": "sample", "colour": "#ff00ff"}, "58": {"group": 58, "well_id": "J4", "state": "sample", "colour": "#ff00ff"}, "59": {"group": 59, "well_id": "K4", "state": "sample", "colour": "#ff00ff"}, "60": {"group": 60, "well_id": "L4", "state": "sample", "colour": "#ff00ff"}, "61": {"group": 61, "well_id": "M4", "state": "sample", "colour": "#ff00ff"}, "62": {"group": 62, "well_id": "N4", "state": "sample", "colour": "#ff00ff"}, "63": {"group": 63, "well_id": "O4", "state": "empty", "colour": "#1e0bc8"}, "64": {"group": 64, "well_id": "P4", "state": "empty", "colour": "#1e0bc8"}, "65": {"group": 65, "well_id": "A5", "state": "empty", "colour": "#1e0bc8"}, "66": {"group": 66, "well_id": "B5", "state": "sample", "colour": "#ff00ff"}, "67": {"group": 67, "well_id": "C5", "state": "sample", "colour": "#ff00ff"}, "68": {"group": 68, "well_id": "D5", "state": "sample", "colour": "#ff00ff"}, "69": {"group": 69, "well_id": "E5", "state": "sample", "colour": "#ff00ff"}, "70": {"group": 70, "well_id": "F5", "state": "sample", "colour": "#ff00ff"}, "71": {"group": 71, "well_id": "G5", "state": "sample", "colour": "#ff00ff"}, "72": {"group": 72, "well_id": "H5", "state": "sample", "colour": "#ff00ff"}, "73": {"group": 73, "well_id": "I5", "state": "sample", "colour": "#ff00ff"}, "74": {"group": 74, "well_id": "J5", "state": "sample", "colour": "#ff00ff"}, "75": {"group": 75, "well_id": "K5", "state": "sample", "colour": "#ff00ff"}, "76": {"group": 76, "well_id": "L5", "state": "sample", "colour": "#ff00ff"}, "77": {"group": 77, "well_id": "M5", "state": "sample", "colour": "#ff00ff"}, "78": {"group": 78, "well_id": "N5", "state": "sample", "colour": "#ff00ff"}, "79": {"group": 79, "well_id": "O5", "state": "empty", "colour": "#1e0bc8"}, "80": {"group": 80, "well_id": "P5", "state": "empty", "colour": "#1e0bc8"}, "81": {"group": 81, "well_id": "A6", "state": "empty", "colour": "#1e0bc8"}, "82": {"group": 82, "well_id": "B6", "state": "sample", "colour": "#ff00ff"}, "83": {"group": 83, "well_id": "C6", "state": "sample", "colour": "#ff00ff"}, "84": {"group": 84, "well_id": "D6", "state": "sample", "colour": "#ff00ff"}, "85": {"group": 85, "well_id": "E6", "state": "sample", "colour": "#ff00ff"}, "86": {"group": 86, "well_id": "F6", "state": "sample", "colour": "#ff00ff"}, "87": {"group": 87, "well_id": "G6", "state": "sample", "colour": "#ff00ff"}, "88": {"group": 88, "well_id": "H6", "state": "sample", "colour": "#ff00ff"}, "89": {"group": 89, "well_id": "I6", "state": "sample", "colour": "#ff00ff"}, "90": {"group": 90, "well_id": "J6", "state": "sample", "colour": "#ff00ff"}, "91": {"group": 91, "well_id": "K6", "state": "sample", "colour": "#ff00ff"}, "92": {"group": 92, "well_id": "L6", "state": "sample", "colour": "#ff00ff"}, "93": {"group": 93, "well_id": "M6", "state": "sample", "colour": "#ff00ff"}, "94": {"group": 94, "well_id": "N6", "state": "sample", "colour": "#ff00ff"}, "95": {"group": 95, "well_id": "O6", "state": "empty", "colour": "#1e0bc8"}, "96": {"group": 96, "well_id": "P6", "state": "empty", "colour": "#1e0bc8"}, "97": {"group": 97, "well_id": "A7", "state": "empty", "colour": "#1e0bc8"}, "98": {"group": 98, "well_id": "B7", "state": "sample", "colour": "#ff00ff"}, "99": {"group": 99, "well_id": "C7", "state": "sample", "colour": "#ff00ff"}, "100": {"group": 100, "well_id": "D7", "state": "sample", "colour": "#ff00ff"}, "101": {"group": 101, "well_id": "E7", "state": "sample", "colour": "#ff00ff"}, "102": {"group": 102, "well_id": "F7", "state": "sample", "colour": "#ff00ff"}, "103": {"group": 103, "well_id": "G7", "state": "sample", "colour": "#ff00ff"}, "104": {"group": 104, "well_id": "H7", "state": "sample", "colour": "#ff00ff"}, "105": {"group": 105, "well_id": "I7", "state": "sample", "colour": "#ff00ff"}, "106": {"group": 106, "well_id": "J7", "state": "sample", "colour": "#ff00ff"}, "107": {"group": 107, "well_id": "K7", "state": "sample", "colour": "#ff00ff"}, "108": {"group": 108, "well_id": "L7", "state": "sample", "colour": "#ff00ff"}, "109": {"group": 109, "well_id": "M7", "state": "sample", "colour": "#ff00ff"}, "110": {"group": 110, "well_id": "N7", "state": "sample", "colour": "#ff00ff"}, "111": {"group": 111, "well_id": "O7", "state": "empty", "colour": "#1e0bc8"}, "112": {"group": 112, "well_id": "P7", "state": "empty", "colour": "#1e0bc8"}, "113": {"group": 113, "well_id": "A8", "state": "empty", "colour": "#1e0bc8"}, "114": {"group": 114, "well_id": "B8", "state": "sample", "colour": "#ff00ff"}, "115": {"group": 115, "well_id": "C8", "state": "sample", "colour": "#ff00ff"}, "116": {"group": 116, "well_id": "D8", "state": "sample", "colour": "#ff00ff"}, "117": {"group": 117, "well_id": "E8", "state": "sample", "colour": "#ff00ff"}, "118": {"group": 118, "well_id": "F8", "state": "sample", "colour": "#ff00ff"}, "119": {"group": 119, "well_id": "G8", "state": "sample", "colour": "#ff00ff"}, "120": {"group": 120, "well_id": "H8", "state": "sample", "colour": "#ff00ff"}, "121": {"group": 121, "well_id": "I8", "state": "sample", "colour": "#ff00ff"}, "122": {"group": 122, "well_id": "J8", "state": "sample", "colour": "#ff00ff"}, "123": {"group": 123, "well_id": "K8", "state": "sample", "colour": "#ff00ff"}, "124": {"group": 124, "well_id": "L8", "state": "sample", "colour": "#ff00ff"}, "125": {"group": 125, "well_id": "M8", "state": "sample", "colour": "#ff00ff"}, "126": {"group": 126, "well_id": "N8", "state": "sample", "colour": "#ff00ff"}, "127": {"group": 127, "well_id": "O8", "state": "empty", "colour": "#1e0bc8"}, "128": {"group": 128, "well_id": "P8", "state": "empty", "colour": "#1e0bc8"}, "129": {"group": 129, "well_id": "A9", "state": "empty", "colour": "#1e0bc8"}, "130": {"group": 130, "well_id": "B9", "state": "sample", "colour": "#ff00ff"}, "131": {"group": 131, "well_id": "C9", "state": "sample", "colour": "#ff00ff"}, "132": {"group": 132, "well_id": "D9", "state": "sample", "colour": "#ff00ff"}, "133": {"group": 133, "well_id": "E9", "state": "sample", "colour": "#ff00ff"}, "134": {"group": 134, "well_id": "F9", "state": "sample", "colour": "#ff00ff"}, "135": {"group": 135, "well_id": "G9", "state": "sample", "colour": "#ff00ff"}, "136": {"group": 136, "well_id": "H9", "state": "sample", "colour": "#ff00ff"}, "137": {"group": 137, "well_id": "I9", "state": "sample", "colour": "#ff00ff"}, "138": {"group": 138, "well_id": "J9", "state": "sample", "colour": "#ff00ff"}, "139": {"group": 139, "well_id": "K9", "state": "sample", "colour": "#ff00ff"}, "140": {"group": 140, "well_id": "L9", "state": "sample", "colour": "#ff00ff"}, "141": {"group": 141, "well_id": "M9", "state": "sample", "colour": "#ff00ff"}, "142": {"group": 142, "well_id": "N9", "state": "sample", "colour": "#ff00ff"}, "143": {"group": 143, "well_id": "O9", "state": "empty", "colour": "#1e0bc8"}, "144": {"group": 144, "well_id": "P9", "state": "empty", "colour": "#1e0bc8"}, "145": {"group": 145, "well_id": "A10", "state": "empty", "colour": "#1e0bc8"}, "146": {"group": 146, "well_id": "B10", "state": "sample", "colour": "#ff00ff"}, "147": {"group": 147, "well_id": "C10", "state": "sample", "colour": "#ff00ff"}, "148": {"group": 148, "well_id": "D10", "state": "sample", "colour": "#ff00ff"}, "149": {"group": 149, "well_id": "E10", "state": "sample", "colour": "#ff00ff"}, "150": {"group": 150, "well_id": "F10", "state": "sample", "colour": "#ff00ff"}, "151": {"group": 151, "well_id": "G10", "state": "sample", "colour": "#ff00ff"}, "152": {"group": 152, "well_id": "H10", "state": "sample", "colour": "#ff00ff"}, "153": {"group": 153, "well_id": "I10", "state": "sample", "colour": "#ff00ff"}, "154": {"group": 154, "well_id": "J10", "state": "sample", "colour": "#ff00ff"}, "155": {"group": 155, "well_id": "K10", "state": "sample", "colour": "#ff00ff"}, "156": {"group": 156, "well_id": "L10", "state": "sample", "colour": "#ff00ff"}, "157": {"group": 157, "well_id": "M10", "state": "sample", "colour": "#ff00ff"}, "158": {"group": 158, "well_id": "N10", "state": "sample", "colour": "#ff00ff"}, "159": {"group": 159, "well_id": "O10", "state": "empty", "colour": "#1e0bc8"}, "160": {"group": 160, "well_id": "P10", "state": "empty", "colour": "#1e0bc8"}, "161": {"group": 161, "well_id": "A11", "state": "empty", "colour": "#1e0bc8"}, "162": {"group": 162, "well_id": "B11", "state": "sample", "colour": "#ff00ff"}, "163": {"group": 163, "well_id": "C11", "state": "sample", "colour": "#ff00ff"}, "164": {"group": 164, "well_id": "D11", "state": "sample", "colour": "#ff00ff"}, "165": {"group": 165, "well_id": "E11", "state": "sample", "colour": "#ff00ff"}, "166": {"group": 166, "well_id": "F11", "state": "sample", "colour": "#ff00ff"}, "167": {"group": 167, "well_id": "G11", "state": "sample", "colour": "#ff00ff"}, "168": {"group": 168, "well_id": "H11", "state": "sample", "colour": "#ff00ff"}, "169": {"group": 169, "well_id": "I11", "state": "sample", "colour": "#ff00ff"}, "170": {"group": 170, "well_id": "J11", "state": "sample", "colour": "#ff00ff"}, "171": {"group": 171, "well_id": "K11", "state": "sample", "colour": "#ff00ff"}, "172": {"group": 172, "well_id": "L11", "state": "sample", "colour": "#ff00ff"}, "173": {"group": 173, "well_id": "M11", "state": "sample", "colour": "#ff00ff"}, "174": {"group": 174, "well_id": "N11", "state": "sample", "colour": "#ff00ff"}, "175": {"group": 175, "well_id": "O11", "state": "empty", "colour": "#1e0bc8"}, "176": {"group": 176, "well_id": "P11", "state": "empty", "colour": "#1e0bc8"}, "177": {"group": 177, "well_id": "A12", "state": "empty", "colour": "#1e0bc8"}, "178": {"group": 178, "well_id": "B12", "state": "sample", "colour": "#ff00ff"}, "179": {"group": 179, "well_id": "C12", "state": "sample", "colour": "#ff00ff"}, "180": {"group": 180, "well_id": "D12", "state": "sample", "colour": "#ff00ff"}, "181": {"group": 181, "well_id": "E12", "state": "sample", "colour": "#ff00ff"}, "182": {"group": 182, "well_id": "F12", "state": "sample", "colour": "#ff00ff"}, "183": {"group": 183, "well_id": "G12", "state": "sample", "colour": "#ff00ff"}, "184": {"group": 184, "well_id": "H12", "state": "sample", "colour": "#ff00ff"}, "185": {"group": 185, "well_id": "I12", "state": "sample", "colour": "#ff00ff"}, "186": {"group": 186, "well_id": "J12", "state": "sample", "colour": "#ff00ff"}, "187": {"group": 187, "well_id": "K12", "state": "sample", "colour": "#ff00ff"}, "188": {"group": 188, "well_id": "L12", "state": "sample", "colour": "#ff00ff"}, "189": {"group": 189, "well_id": "M12", "state": "sample", "colour": "#ff00ff"}, "190": {"group": 190, "well_id": "N12", "state": "sample", "colour": "#ff00ff"}, "191": {"group": 191, "well_id": "O12", "state": "empty", "colour": "#1e0bc8"}, "192": {"group": 192, "well_id": "P12", "state": "empty", "colour": "#1e0bc8"}, "193": {"group": 193, "well_id": "A13", "state": "empty", "colour": "#1e0bc8"}, "194": {"group": 194, "well_id": "B13", "state": "sample", "colour": "#ff00ff"}, "195": {"group": 195, "well_id": "C13", "state": "sample", "colour": "#ff00ff"}, "196": {"group": 196, "well_id": "D13", "state": "sample", "colour": "#ff00ff"}, "197": {"group": 197, "well_id": "E13", "state": "sample", "colour": "#ff00ff"}, "198": {"group": 198, "well_id": "F13", "state": "sample", "colour": "#ff00ff"}, "199": {"group": 199, "well_id": "G13", "state": "sample", "colour": "#ff00ff"}, "200": {"group": 200, "well_id": "H13", "state": "sample", "colour": "#ff00ff"}, "201": {"group": 201, "well_id": "I13", "state": "sample", "colour": "#ff00ff"}, "202": {"group": 202, "well_id": "J13", "state": "sample", "colour": "#ff00ff"}, "203": {"group": 203, "well_id": "K13", "state": "sample", "colour": "#ff00ff"}, "204": {"group": 204, "well_id": "L13", "state": "sample", "colour": "#ff00ff"}, "205": {"group": 205, "well_id": "M13", "state": "sample", "colour": "#ff00ff"}, "206": {"group": 206, "well_id": "N13", "state": "sample", "colour": "#ff00ff"}, "207": {"group": 207, "well_id": "O13", "state": "empty", "colour": "#1e0bc8"}, "208": {"group": 208, "well_id": "P13", "state": "empty", "colour": "#1e0bc8"}, "209": {"group": 209, "well_id": "A14", "state": "empty", "colour": "#1e0bc8"}, "210": {"group": 210, "well_id": "B14", "state": "sample", "colour": "#ff00ff"}, "211": {"group": 211, "well_id": "C14", "state": "sample", "colour": "#ff00ff"}, "212": {"group": 212, "well_id": "D14", "state": "sample", "colour": "#ff00ff"}, "213": {"group": 213, "well_id": "E14", "state": "sample", "colour": "#ff00ff"}, "214": {"group": 214, "well_id": "F14", "state": "sample", "colour": "#ff00ff"}, "215": {"group": 215, "well_id": "G14", "state": "sample", "colour": "#ff00ff"}, "216": {"group": 216, "well_id": "H14", "state": "sample", "colour": "#ff00ff"}, "217": {"group": 217, "well_id": "I14", "state": "sample", "colour": "#ff00ff"}, "218": {"group": 218, "well_id": "J14", "state": "sample", "colour": "#ff00ff"}, "219": {"group": 219, "well_id": "K14", "state": "sample", "colour": "#ff00ff"}, "220": {"group": 220, "well_id": "L14", "state": "sample", "colour": "#ff00ff"}, "221": {"group": 221, "well_id": "M14", "state": "sample", "colour": "#ff00ff"}, "222": {"group": 222, "well_id": "N14", "state": "sample", "colour": "#ff00ff"}, "223": {"group": 223, "well_id": "O14", "state": "empty", "colour": "#1e0bc8"}, "224": {"group": 224, "well_id": "P14", "state": "empty", "colour": "#1e0bc8"}, "225": {"group": 225, "well_id": "A15", "state": "empty", "colour": "#1e0bc8"}, "226": {"group": 226, "well_id": "B15", "state": "sample", "colour": "#ff00ff"}, "227": {"group": 227, "well_id": "C15", "state": "sample", "colour": "#ff00ff"}, "228": {"group": 228, "well_id": "D15", "state": "sample", "colour": "#ff00ff"}, "229": {"group": 229, "well_id": "E15", "state": "sample", "colour": "#ff00ff"}, "230": {"group": 230, "well_id": "F15", "state": "sample", "colour": "#ff00ff"}, "231": {"group": 231, "well_id": "G15", "state": "sample", "colour": "#ff00ff"}, "232": {"group": 232, "well_id": "H15", "state": "sample", "colour": "#ff00ff"}, "233": {"group": 233, "well_id": "I15", "state": "sample", "colour": "#ff00ff"}, "234": {"group": 234, "well_id": "J15", "state": "sample", "colour": "#ff00ff"}, "235": {"group": 235, "well_id": "K15", "state": "sample", "colour": "#ff00ff"}, "236": {"group": 236, "well_id": "L15", "state": "sample", "colour": "#ff00ff"}, "237": {"group": 237, "well_id": "M15", "state": "sample", "colour": "#ff00ff"}, "238": {"group": 238, "well_id": "N15", "state": "sample", "colour": "#ff00ff"}, "239": {"group": 239, "well_id": "O15", "state": "empty", "colour": "#1e0bc8"}, "240": {"group": 240, "well_id": "P15", "state": "empty", "colour": "#1e0bc8"}, "241": {"group": 241, "well_id": "A16", "state": "empty", "colour": "#1e0bc8"}, "242": {"group": 242, "well_id": "B16", "state": "sample", "colour": "#ff00ff"}, "243": {"group": 243, "well_id": "C16", "state": "sample", "colour": "#ff00ff"}, "244": {"group": 244, "well_id": "D16", "state": "sample", "colour": "#ff00ff"}, "245": {"group": 245, "well_id": "E16", "state": "sample", "colour": "#ff00ff"}, "246": {"group": 246, "well_id": "F16", "state": "sample", "colour": "#ff00ff"}, "247": {"group": 247, "well_id": "G16", "state": "sample", "colour": "#ff00ff"}, "248": {"group": 248, "well_id": "H16", "state": "sample", "colour": "#ff00ff"}, "249": {"group": 249, "well_id": "I16", "state": "sample", "colour": "#ff00ff"}, "250": {"group": 250, "well_id": "J16", "state": "sample", "colour": "#ff00ff"}, "251": {"group": 251, "well_id": "K16", "state": "sample", "colour": "#ff00ff"}, "252": {"group": 252, "well_id": "L16", "state": "sample", "colour": "#ff00ff"}, "253": {"group": 253, "well_id": "M16", "state": "sample", "colour": "#ff00ff"}, "254": {"group": 254, "well_id": "N16", "state": "sample", "colour": "#ff00ff"}, "255": {"group": 255, "well_id": "O16", "state": "empty", "colour": "#1e0bc8"}, "256": {"group": 256, "well_id": "P16", "state": "empty", "colour": "#1e0bc8"}, "257": {"group": 257, "well_id": "A17", "state": "empty", "colour": "#1e0bc8"}, "258": {"group": 258, "well_id": "B17", "state": "sample", "colour": "#ff00ff"}, "259": {"group": 259, "well_id": "C17", "state": "sample", "colour": "#ff00ff"}, "260": {"group": 260, "well_id": "D17", "state": "sample", "colour": "#ff00ff"}, "261": {"group": 261, "well_id": "E17", "state": "sample", "colour": "#ff00ff"}, "262": {"group": 262, "well_id": "F17", "state": "sample", "colour": "#ff00ff"}, "263": {"group": 263, "well_id": "G17", "state": "sample", "colour": "#ff00ff"}, "264": {"group": 264, "well_id": "H17", "state": "sample", "colour": "#ff00ff"}, "265": {"group": 265, "well_id": "I17", "state": "sample", "colour": "#ff00ff"}, "266": {"group": 266, "well_id": "J17", "state": "sample", "colour": "#ff00ff"}, "267": {"group": 267, "well_id": "K17", "state": "sample", "colour": "#ff00ff"}, "268": {"group": 268, "well_id": "L17", "state": "sample", "colour": "#ff00ff"}, "269": {"group": 269, "well_id": "M17", "state": "sample", "colour": "#ff00ff"}, "270": {"group": 270, "well_id": "N17", "state": "sample", "colour": "#ff00ff"}, "271": {"group": 271, "well_id": "O17", "state": "empty", "colour": "#1e0bc8"}, "272": {"group": 272, "well_id": "P17", "state": "empty", "colour": "#1e0bc8"}, "273": {"group": 273, "well_id": "A18", "state": "empty", "colour": "#1e0bc8"}, "274": {"group": 274, "well_id": "B18", "state": "sample", "colour": "#ff00ff"}, "275": {"group": 275, "well_id": "C18", "state": "sample", "colour": "#ff00ff"}, "276": {"group": 276, "well_id": "D18", "state": "sample", "colour": "#ff00ff"}, "277": {"group": 277, "well_id": "E18", "state": "sample", "colour": "#ff00ff"}, "278": {"group": 278, "well_id": "F18", "state": "sample", "colour": "#ff00ff"}, "279": {"group": 279, "well_id": "G18", "state": "sample", "colour": "#ff00ff"}, "280": {"group": 280, "well_id": "H18", "state": "sample", "colour": "#ff00ff"}, "281": {"group": 281, "well_id": "I18", "state": "sample", "colour": "#ff00ff"}, "282": {"group": 282, "well_id": "J18", "state": "sample", "colour": "#ff00ff"}, "283": {"group": 283, "well_id": "K18", "state": "sample", "colour": "#ff00ff"}, "284": {"group": 284, "well_id": "L18", "state": "sample", "colour": "#ff00ff"}, "285": {"group": 285, "well_id": "M18", "state": "sample", "colour": "#ff00ff"}, "286": {"group": 286, "well_id": "N18", "state": "sample", "colour": "#ff00ff"}, "287": {"group": 287, "well_id": "O18", "state": "empty", "colour": "#1e0bc8"}, "288": {"group": 288, "well_id": "P18", "state": "empty", "colour": "#1e0bc8"}, "289": {"group": 289, "well_id": "A19", "state": "empty", "colour": "#1e0bc8"}, "290": {"group": 290, "well_id": "B19", "state": "sample", "colour": "#ff00ff"}, "291": {"group": 291, "well_id": "C19", "state": "sample", "colour": "#ff00ff"}, "292": {"group": 292, "well_id": "D19", "state": "sample", "colour": "#ff00ff"}, "293": {"group": 293, "well_id": "E19", "state": "sample", "colour": "#ff00ff"}, "294": {"group": 294, "well_id": "F19", "state": "sample", "colour": "#ff00ff"}, "295": {"group": 295, "well_id": "G19", "state": "sample", "colour": "#ff00ff"}, "296": {"group": 296, "well_id": "H19", "state": "sample", "colour": "#ff00ff"}, "297": {"group": 297, "well_id": "I19", "state": "sample", "colour": "#ff00ff"}, "298": {"group": 298, "well_id": "J19", "state": "sample", "colour": "#ff00ff"}, "299": {"group": 299, "well_id": "K19", "state": "sample", "colour": "#ff00ff"}, "300": {"group": 300, "well_id": "L19", "state": "sample", "colour": "#ff00ff"}, "301": {"group": 301, "well_id": "M19", "state": "sample", "colour": "#ff00ff"}, "302": {"group": 302, "well_id": "N19", "state": "sample", "colour": "#ff00ff"}, "303": {"group": 303, "well_id": "O19", "state": "empty", "colour": "#1e0bc8"}, "304": {"group": 304, "well_id": "P19", "state": "empty", "colour": "#1e0bc8"}, "305": {"group": 305, "well_id": "A20", "state": "empty", "colour": "#1e0bc8"}, "306": {"group": 306, "well_id": "B20", "state": "sample", "colour": "#ff00ff"}, "307": {"group": 307, "well_id": "C20", "state": "sample", "colour": "#ff00ff"}, "308": {"group": 308, "well_id": "D20", "state": "sample", "colour": "#ff00ff"}, "309": {"group": 309, "well_id": "E20", "state": "sample", "colour": "#ff00ff"}, "310": {"group": 310, "well_id": "F20", "state": "sample", "colour": "#ff00ff"}, "311": {"group": 311, "well_id": "G20", "state": "sample", "colour": "#ff00ff"}, "312": {"group": 312, "well_id": "H20", "state": "sample", "colour": "#ff00ff"}, "313": {"group": 313, "well_id": "I20", "state": "sample", "colour": "#ff00ff"}, "314": {"group": 314, "well_id": "J20", "state": "sample", "colour": "#ff00ff"}, "315": {"group": 315, "well_id": "K20", "state": "sample", "colour": "#ff00ff"}, "316": {"group": 316, "well_id": "L20", "state": "sample", "colour": "#ff00ff"}, "317": {"group": 317, "well_id": "M20", "state": "sample", "colour": "#ff00ff"}, "318": {"group": 318, "well_id": "N20", "state": "sample", "colour": "#ff00ff"}, "319": {"group": 319, "well_id": "O20", "state": "empty", "colour": "#1e0bc8"}, "320": {"group": 320, "well_id": "P20", "state": "empty", "colour": "#1e0bc8"}, "321": {"group": 321, "well_id": "A21", "state": "empty", "colour": "#1e0bc8"}, "322": {"group": 322, "well_id": "B21", "state": "sample", "colour": "#ff00ff"}, "323": {"group": 323, "well_id": "C21", "state": "sample", "colour": "#ff00ff"}, "324": {"group": 324, "well_id": "D21", "state": "sample", "colour": "#ff00ff"}, "325": {"group": 325, "well_id": "E21", "state": "sample", "colour": "#ff00ff"}, "326": {"group": 326, "well_id": "F21", "state": "sample", "colour": "#ff00ff"}, "327": {"group": 327, "well_id": "G21", "state": "sample", "colour": "#ff00ff"}, "328": {"group": 328, "well_id": "H21", "state": "sample", "colour": "#ff00ff"}, "329": {"group": 329, "well_id": "I21", "state": "sample", "colour": "#ff00ff"}, "330": {"group": 330, "well_id": "J21", "state": "sample", "colour": "#ff00ff"}, "331": {"group": 331, "well_id": "K21", "state": "sample", "colour": "#ff00ff"}, "332": {"group": 332, "well_id": "L21", "state": "sample", "colour": "#ff00ff"}, "333": {"group": 333, "well_id": "M21", "state": "sample", "colour": "#ff00ff"}, "334": {"group": 334, "well_id": "N21", "state": "sample", "colour": "#ff00ff"}, "335": {"group": 335, "well_id": "O21", "state": "empty", "colour": "#1e0bc8"}, "336": {"group": 336, "well_id": "P21", "state": "empty", "colour": "#1e0bc8"}, "337": {"group": 337, "well_id": "A22", "state": "empty", "colour": "#1e0bc8"}, "338": {"group": 338, "well_id": "B22", "state": "sample", "colour": "#ff00ff"}, "339": {"group": 339, "well_id": "C22", "state": "sample", "colour": "#ff00ff"}, "340": {"group": 340, "well_id": "D22", "state": "sample", "colour": "#ff00ff"}, "341": {"group": 341, "well_id": "E22", "state": "sample", "colour": "#ff00ff"}, "342": {"group": 342, "well_id": "F22", "state": "sample", "colour": "#ff00ff"}, "343": {"group": 343, "well_id": "G22", "state": "sample", "colour": "#ff00ff"}, "344": {"group": 344, "well_id": "H22", "state": "sample", "colour": "#ff00ff"}, "345": {"group": 345, "well_id": "I22", "state": "sample", "colour": "#ff00ff"}, "346": {"group": 346, "well_id": "J22", "state": "sample", "colour": "#ff00ff"}, "347": {"group": 347, "well_id": "K22", "state": "sample", "colour": "#ff00ff"}, "348": {"group": 348, "well_id": "L22", "state": "sample", "colour": "#ff00ff"}, "349": {"group": 349, "well_id": "M22", "state": "sample", "colour": "#ff00ff"}, "350": {"group": 350, "well_id": "N22", "state": "sample", "colour": "#ff00ff"}, "351": {"group": 351, "well_id": "O22", "state": "empty", "colour": "#1e0bc8"}, "352": {"group": 352, "well_id": "P22", "state": "empty", "colour": "#1e0bc8"}, "353": {"group": 353, "well_id": "A23", "state": "empty", "colour": "#1e0bc8"}, "354": {"group": 354, "well_id": "B23", "state": "minimum", "colour": "#ff8000"}, "355": {"group": 355, "well_id": "C23", "state": "minimum", "colour": "#ff8000"}, "356": {"group": 356, "well_id": "D23", "state": "minimum", "colour": "#ff8000"}, "357": {"group": 357, "well_id": "E23", "state": "minimum", "colour": "#ff8000"}, "358": {"group": 358, "well_id": "F23", "state": "minimum", "colour": "#ff8000"}, "359": {"group": 359, "well_id": "G23", "state": "minimum", "colour": "#ff8000"}, "360": {"group": 360, "well_id": "H23", "state": "minimum", "colour": "#ff8000"}, "361": {"group": 361, "well_id": "I23", "state": "minimum", "colour": "#ff8000"}, "362": {"group": 362, "well_id": "J23", "state": "minimum", "colour": "#ff8000"}, "363": {"group": 363, "well_id": "K23", "state": "minimum", "colour": "#ff8000"}, "364": {"group": 364, "well_id": "L23", "state": "minimum", "colour": "#ff8000"}, "365": {"group": 365, "well_id": "M23", "state": "minimum", "colour": "#ff8000"}, "366": {"group": 366, "well_id": "N23", "state": "minimum", "colour": "#ff8000"}, "367": {"group": 367, "well_id": "O23", "state": "empty", "colour": "#1e0bc8"}, "368": {"group": 368, "well_id": "P23", "state": "empty", "colour": "#1e0bc8"}, "369": {"group": 369, "well_id": "A24", "state": "empty", "colour": "#1e0bc8"}, "370": {"group": 370, "well_id": "B24", "state": "empty", "colour": "#1e0bc8"}, "371": {"group": 371, "well_id": "C24", "state": "empty", "colour": "#1e0bc8"}, "372": {"group": 372, "well_id": "D24", "state": "empty", "colour": "#1e0bc8"}, "373": {"group": 373, "well_id": "E24", "state": "empty", "colour": "#1e0bc8"}, "374": {"group": 374, "well_id": "F24", "state": "empty", "colour": "#1e0bc8"}, "375": {"group": 375, "well_id": "G24", "state": "empty", "colour": "#1e0bc8"}, "376": {"group": 376, "well_id": "H24", "state": "empty", "colour": "#1e0bc8"}, "377": {"group": 377, "well_id": "I24", "state": "empty", "colour": "#1e0bc8"}, "378": {"group": 378, "well_id": "J24", "state": "empty", "colour": "#1e0bc8"}, "379": {"group": 379, "well_id": "K24", "state": "empty", "colour": "#1e0bc8"}, "380": {"group": 380, "well_id": "L24", "state": "empty", "colour": "#1e0bc8"}, "381": {"group": 381, "well_id": "M24", "state": "empty", "colour": "#1e0bc8"}, "382": {"group": 382, "well_id": "N24", "state": "empty", "colour": "#1e0bc8"}, "383": {"group": 383, "well_id": "O24", "state": "empty", "colour": "#1e0bc8"}, "384": {"group": 384, "well_id": "P24", "state": "empty", "colour": "#1e0bc8"}}, "plate_type": "plate_384"}}
    # z_prime_calc = True
    # heatmap_colours = {'start': 'light red', 'mid': 'white', 'end': 'light green'}
    # folder = "C:/Users/phch/PycharmProjects/structure_search/Bio Data/raw data"
    # bio_data(config, folder, well_states_report, plate_analysis_dict, plate_layout, z_prime_calc, heatmap_colours)
    plate_layout_to_excel(plate_layout)
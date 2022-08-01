import PySimpleGUI as sg

from plate_formatting import daughter_plate_generator
from database_startup import DatabaseSetUp
from database_controller import FetchData, AddData
from csv_handler import CSVWriter, CSVConverter
from excel_handler import ExcelReader
from lc_data_handler import LCMSHandler
from database_controller import FetchData
from file_handler import get_file_list
from bio_data_functions import original_data_dict
from bio_date_handler import BIOAnalyser

import bio_data_functions
import configparser
from json_handler import dict_reader


def amount_samples(plate_amount, samples_per_plate=10):
    """
    calculate the amount of samples needed depending on amount of mother plates.
    :param plate_amount: Amount of plates needed
    :param samples_per_plate: Amount of samples per plate
    :return: Total amount of samples needed
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


def _compound_list(mp_amount, transferee_volume, ignore_active, sub_search, smiles,
                  sub_search_methode, threshold, source_table):
    """
    Generate list of compounds, based on number of motherplates only, or by sub_structure search.
    Generate comPOUND file for fecthing tubes from the comPOUND freezer.
    :param mp_amount: amount of samples
    :param transferee_volume: amount of liquid to transferee
    :param ignore_active: If the list needs to take into account compounds already in MotherPlates with more than
    1 uL volume left. - This might needs to be lowered...
    :param smiles: smiles code to compare compounds with for sub search
    :param sub_search: tuble (true/false) if it will use structure search to find compounds or not
    :param sub_search_methode: What method to use for making a substructure search
    :param threshold: This is for sub_searchs. how alike the compounds should minimum be
    :param source_table: The table from the database, where the samples are coming from. and the table where the
    structure search is used. should always be compound_main
    :param database: The database, should always be SCore.db
    :return: compound_list, liquid_warning_list
    """

    sample_amount = amount_samples(mp_amount)
    fd = FetchData()

    plated_compounds = []
    if not ignore_active:
        plated_compounds = [compounds for compounds in fd.get_all_compounds_ids(1, "compound_mp")]

    # Gets a list of compounds, based on search criteria
    compound_list, liquid_warning_list = fd.list_limiter(sample_amount, source_table, transferee_volume,
                                                                     sub_search, sub_search_methode, smiles, threshold,
                                                                     ignore_active, plated_compounds)

    return compound_list, liquid_warning_list


def table_update(mp_amount, transferee_volume, ignore_active, sub_search, smiles, sub_search_methode,
                 threshold, source_table):
    """
    Updates the compound table with compounds depending on search criteria
    :param mp_amount: amount of mother plates to find compounds from
    :type mp_amount: int
    :param transferee_volume: how much volume to transfere
    :type transferee_volume: float
    :param ignore_active: If it should take into account witch compounds are allready in MotherPlates. True = All
    compounds, False = only compounds not found in MotherPlates
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
    :return: treedata, all_data, rows, counter
    """

    fd = FetchData()
    all_data = {}
    all_data_headlines = ["compound_list", "liquid_warning_list", "row_data", "mp_data", "mp_mapping", "plate_count"]

    temp_all_data = _compound_list(mp_amount, transferee_volume, ignore_active, sub_search, smiles, sub_search_methode,
                              threshold, source_table)

    for índex, values in enumerate(temp_all_data):
        all_data[all_data_headlines[índex]] = values

    rows = fd.list_to_rows(all_data["compound_list"])

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
        if counter < 4000:
            treedata.Insert("", compound_id, "", temp_list, icon=temp_png)
        else:
            treedata.Insert("", compound_id, "", temp_list, icon="")

    return treedata, all_data, rows, counter


def compound_export(folder, compound_list):
    csvw = CSVWriter()
    csvw.compound_freezer_writer(folder, compound_list)


def compound_counter():
    fd = FetchData()
    return len(fd.get_all_compounds_ids(0, "compound_main"))


def update_database(data, table, file_type=None):
    """
    Update the database with data. Both for adding data to the different tables, but updating tables with new values
    :param data: Output file from the plate_butler system, tube files for the comPOUND freezer, or other data.
    :param file_type: If the file is a CSV file, it needs a specific file_type to know how to handle the file.
    as the CSV files are different depending on where they are coming from.
    :param table: What table needs to be updated/where the data is going
    :param database: Main database
    :return: None
    """

    ad_db = AddData()
    ad_db.add_controller(table, data, file_type)


def purity_handler(folder, uv_one, uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak, ms_delta, ms_mode,
                   ms_threshold):
    """
    Takes raw data from LC/MS (UV and MS data) and mass from the database, per compound. and see if they can find the
    mass in the raw data, and then find the purity of the peak (based on retention time) for each compound
    :param folder: Folder with the raw-data
    :param uv_one: If it uses a single wavelength per compound or uses the whole PDA-range
    :param uv_same_wavelength: if it uses the same wavelength, what wavelength that is
    :param wavelength: set to all, if there is no wavelength for each individuel compound
    :param uv_threshold: minimum threshold for the UV signal. anything below will be ignored
    :param rt_solvent_peak: retention time for the solvent peak
    :param ms_delta: When looking for the MS data, how precise the mass should fit with the data.
    :param ms_mode: if you are looking at the positive or negative. Have not been set up to look at both yet.
    :param ms_threshold: minimum threshold for the MS signal. anything below will be ignored
    :return: None
    """

    lc_h = LCMSHandler()
    file_list = get_file_list(folder)
    compound_info = lc_h.lc_controller(file_list, uv_one, uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak,
                                       ms_delta, ms_mode, ms_threshold)
    update_database(compound_info, "purity_data")


def draw_plate(config, graph, plate_type, well_dict, archive_plate, gui_tab, sample_layout):
    """
    Draws different plate type in on a canvas/graph.
    :param graph: The canvas/graph that is setup in sg.window
    :type graph: PySimpleGUI.PySimpleGUI.Graph
    :param plate_type: what platetype that it needs to draw. there are 3 options 96, 384 or 1536.
    :type plate_type: str
    :param well_dict: A dict over wells, this is used for drawing saved plate layouts. The dict hold information for
    :type well_dict: dict
    what type each well is (sample, blank or paint) and the colour of the well to draw
    :param archive_plate: bool to see if it needs to draw a blank plate or a saved plate
    :type archive_plate: bool
    :param gui_tab: what tab the plate is drawn on. differet tabs differe sizes:
    :type gui_tab: str
    :return: well_dict: a dict over the wells, name, state, colour and number.
    min_x, min_y, max_x, max_y: coordinate boundaries for the plate on the canvas
    """

    graph.erase()
    if gui_tab == "bio":
        well_size = 20
        start_x = 5
        start_y = 165
    else:
        well_size = 40
        start_x = 10
        start_y = 335

    fill_colour = "blue"
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
                well_state = well_dict[counter]["state"]
                fill_colour = config["plate_colouring"][well_state]

            if sample_layout != "single point":
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


def bio_data(config, folder, well_states_report, plate_analysis_dict, plate_layout, z_prime_calc, heatmap_colours):
    bioa = BIOAnalyser(config, well_states_report, plate_analysis_dict, heatmap_colours)
    file_list = get_file_list(folder)

    all_plates_data = {}
    for files in file_list:
        all_data, well_row_col, well_type = original_data_dict(files, plate_layout)
        if not all_data:
            return False

        file_name = files.split("-")
        all_plates_data[file_name[-1]] = bioa.bio_data_controller(files, plate_layout, all_data, well_row_col, well_type
                                                                  , z_prime_calc)

    return True


def mp_production_2d_to_pb_simulate(folder_output, barcodes_2d, mp_name, trans_vol):
    barcodes_2d_files = get_file_list(barcodes_2d)
    csvc = CSVConverter()
    csvc.mp_in_to_out(folder_output, barcodes_2d_files, mp_name, trans_vol)


def plate_layout_re_formate(plate_layout):
    plate_layout_re = {}

    for counter in plate_layout:
        plate_layout_re[plate_layout[counter]["well_id"]] = {}

        plate_layout_re[plate_layout[counter]["well_id"]]["group"] = plate_layout[counter]["group"]
        plate_layout_re[plate_layout[counter]["well_id"]]["well_state"] = plate_layout[counter]["state"]
        plate_layout_re[plate_layout[counter]["well_id"]]["colour"] = plate_layout[counter]["colour"]

    return plate_layout_re

if __name__ == "__main__":
    ...

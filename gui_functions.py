import PySimpleGUI as sg

from plate_formatting import daughter_plate_generator
from database_startup import DatabaseSetUp
from database_controller import FetchData, AddData
from csv_handler import CSVWriter, CSVConverter, CSVReader
from excel_handler import ExcelReader
from lc_data_handler import LCMSHandler
from database_controller import FetchData
from file_handler import get_file_list
from bio_data_functions import original_data_dict, org, norm, pora, bio_full_report_writer
from bio_date_handler import BIOAnalyser
from info import compound_well_layout
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
    items = fd.list_limiter(sample_amount, source_table, transferee_volume,
                                                                     sub_search, sub_search_methode, smiles, threshold,
                                                                     ignore_active, plated_compounds)

    return items


def table_update_tree(mp_amount, transferee_volume, ignore_active, sub_search, smiles, sub_search_methode,
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

    if not temp_all_data:
        return None
    else:
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


def update_database(data, table, file_type):
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


def bio_data(config, folder, plate_layout, bio_plate_report_setup):
    # needs to reformat plate-layout to use well ID instead of numbers...
    bioa = BIOAnalyser(config, bio_plate_report_setup)
    file_list = get_file_list(folder)

    all_plates_data = {}
    for files in file_list:
        all_data, well_row_col, well_type, barcode = original_data_dict(files, plate_layout)
        if not all_data:
            return False

        all_plates_data[barcode] = bioa.bio_data_controller(files, plate_layout, all_data, well_row_col, well_type)

    return True, all_plates_data


def bio_full_report(analyse_method, all_plate_data, final_report_setup, output_folder, final_report_name):

    output_file = f"{output_folder}/{final_report_name}.xlsx"
    bio_full_report_writer(analyse_method, all_plate_data, output_file, final_report_setup)


def mp_production_2d_to_pb_simulate(folder_output, barcodes_2d, mp_name, trans_vol):
    barcodes_2d_files = get_file_list(barcodes_2d)
    csvc = CSVConverter()
    csvc.mp_in_to_out(folder_output, barcodes_2d_files, mp_name, trans_vol)


def compound_freezer_to_2d_simulate(tube_file, output_folder):
    csv_w = CSVWriter()
    csv_r = CSVReader
    tube_dict = csv_r.tube_list_to_dict(tube_file)
    csv_w.compound_freezer_to_2d_CSV_simulate(tube_dict, output_folder)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    well_states_report = {'sample': True, 'blank': False, 'max': False, 'minimum': False, 'positive': False, 'negative': False, 'empty': False}
    plate_analysis_dict = {'original': {'used': True, 'methode': org, 'heatmap': False}, 'normalised': {'used': True, 'methode': norm, 'heatmap': False}, 'pora': {'used': True, 'methode': pora, 'heatmap': False}}
    plate_layout = {'well_layout': {1: {'well_id': 'A1', 'state': 'empty', 'colour': 'blue'}, 2: {'well_id': 'B1', 'state': 'empty', 'colour': 'blue'}, 3: {'well_id': 'C1', 'state': 'empty', 'colour': 'blue'}, 4: {'well_id': 'D1', 'state': 'empty', 'colour': 'blue'}, 5: {'well_id': 'E1', 'state': 'empty', 'colour': 'blue'}, 6: {'well_id': 'F1', 'state': 'empty', 'colour': 'blue'}, 7: {'well_id': 'G1', 'state': 'empty', 'colour': 'blue'}, 8: {'well_id': 'H1', 'state': 'empty', 'colour': 'blue'}, 9: {'well_id': 'I1', 'state': 'empty', 'colour': 'blue'}, 10: {'well_id': 'J1', 'state': 'empty', 'colour': 'blue'}, 11: {'well_id': 'K1', 'state': 'empty', 'colour': 'blue'}, 12: {'well_id': 'L1', 'state': 'empty', 'colour': 'blue'}, 13: {'well_id': 'M1', 'state': 'empty', 'colour': 'blue'}, 14: {'well_id': 'N1', 'state': 'empty', 'colour': 'blue'}, 15: {'well_id': 'O1', 'state': 'empty', 'colour': 'blue'}, 16: {'well_id': 'P1', 'state': 'empty', 'colour': 'blue'}, 17: {'well_id': 'A2', 'state': 'empty', 'colour': 'blue'}, 18: {'well_id': 'B2', 'state': 'max', 'colour': 'purple'}, 19: {'well_id': 'C2', 'state': 'max', 'colour': 'purple'}, 20: {'well_id': 'D2', 'state': 'max', 'colour': 'purple'}, 21: {'well_id': 'E2', 'state': 'max', 'colour': 'purple'}, 22: {'well_id': 'F2', 'state': 'max', 'colour': 'purple'}, 23: {'well_id': 'G2', 'state': 'max', 'colour': 'purple'}, 24: {'well_id': 'H2', 'state': 'max', 'colour': 'purple'}, 25: {'well_id': 'I2', 'state': 'max', 'colour': 'purple'}, 26: {'well_id': 'J2', 'state': 'max', 'colour': 'purple'}, 27: {'well_id': 'K2', 'state': 'max', 'colour': 'purple'}, 28: {'well_id': 'L2', 'state': 'max', 'colour': 'purple'}, 29: {'well_id': 'M2', 'state': 'max', 'colour': 'purple'}, 30: {'well_id': 'N2', 'state': 'max', 'colour': 'purple'}, 31: {'well_id': 'O2', 'state': 'empty', 'colour': 'blue'}, 32: {'well_id': 'P2', 'state': 'empty', 'colour': 'blue'}, 33: {'well_id': 'A3', 'state': 'empty', 'colour': 'blue'}, 34: {'well_id': 'B3', 'state': 'sample', 'colour': 'orange'}, 35: {'well_id': 'C3', 'state': 'sample', 'colour': 'orange'}, 36: {'well_id': 'D3', 'state': 'sample', 'colour': 'orange'}, 37: {'well_id': 'E3', 'state': 'sample', 'colour': 'orange'}, 38: {'well_id': 'F3', 'state': 'sample', 'colour': 'orange'}, 39: {'well_id': 'G3', 'state': 'sample', 'colour': 'orange'}, 40: {'well_id': 'H3', 'state': 'sample', 'colour': 'orange'}, 41: {'well_id': 'I3', 'state': 'sample', 'colour': 'orange'}, 42: {'well_id': 'J3', 'state': 'sample', 'colour': 'orange'}, 43: {'well_id': 'K3', 'state': 'sample', 'colour': 'orange'}, 44: {'well_id': 'L3', 'state': 'sample', 'colour': 'orange'}, 45: {'well_id': 'M3', 'state': 'sample', 'colour': 'orange'}, 46: {'well_id': 'N3', 'state': 'sample', 'colour': 'orange'}, 47: {'well_id': 'O3', 'state': 'empty', 'colour': 'blue'}, 48: {'well_id': 'P3', 'state': 'empty', 'colour': 'blue'}, 49: {'well_id': 'A4', 'state': 'empty', 'colour': 'blue'}, 50: {'well_id': 'B4', 'state': 'sample', 'colour': 'orange'}, 51: {'well_id': 'C4', 'state': 'sample', 'colour': 'orange'}, 52: {'well_id': 'D4', 'state': 'sample', 'colour': 'orange'}, 53: {'well_id': 'E4', 'state': 'sample', 'colour': 'orange'}, 54: {'well_id': 'F4', 'state': 'sample', 'colour': 'orange'}, 55: {'well_id': 'G4', 'state': 'sample', 'colour': 'orange'}, 56: {'well_id': 'H4', 'state': 'sample', 'colour': 'orange'}, 57: {'well_id': 'I4', 'state': 'sample', 'colour': 'orange'}, 58: {'well_id': 'J4', 'state': 'sample', 'colour': 'orange'}, 59: {'well_id': 'K4', 'state': 'sample', 'colour': 'orange'}, 60: {'well_id': 'L4', 'state': 'sample', 'colour': 'orange'}, 61: {'well_id': 'M4', 'state': 'sample', 'colour': 'orange'}, 62: {'well_id': 'N4', 'state': 'sample', 'colour': 'orange'}, 63: {'well_id': 'O4', 'state': 'empty', 'colour': 'blue'}, 64: {'well_id': 'P4', 'state': 'empty', 'colour': 'blue'}, 65: {'well_id': 'A5', 'state': 'empty', 'colour': 'blue'}, 66: {'well_id': 'B5', 'state': 'sample', 'colour': 'orange'}, 67: {'well_id': 'C5', 'state': 'sample', 'colour': 'orange'}, 68: {'well_id': 'D5', 'state': 'sample', 'colour': 'orange'}, 69: {'well_id': 'E5', 'state': 'sample', 'colour': 'orange'}, 70: {'well_id': 'F5', 'state': 'sample', 'colour': 'orange'}, 71: {'well_id': 'G5', 'state': 'sample', 'colour': 'orange'}, 72: {'well_id': 'H5', 'state': 'sample', 'colour': 'orange'}, 73: {'well_id': 'I5', 'state': 'sample', 'colour': 'orange'}, 74: {'well_id': 'J5', 'state': 'sample', 'colour': 'orange'}, 75: {'well_id': 'K5', 'state': 'sample', 'colour': 'orange'}, 76: {'well_id': 'L5', 'state': 'sample', 'colour': 'orange'}, 77: {'well_id': 'M5', 'state': 'sample', 'colour': 'orange'}, 78: {'well_id': 'N5', 'state': 'sample', 'colour': 'orange'}, 79: {'well_id': 'O5', 'state': 'empty', 'colour': 'blue'}, 80: {'well_id': 'P5', 'state': 'empty', 'colour': 'blue'}, 81: {'well_id': 'A6', 'state': 'empty', 'colour': 'blue'}, 82: {'well_id': 'B6', 'state': 'sample', 'colour': 'orange'}, 83: {'well_id': 'C6', 'state': 'sample', 'colour': 'orange'}, 84: {'well_id': 'D6', 'state': 'sample', 'colour': 'orange'}, 85: {'well_id': 'E6', 'state': 'sample', 'colour': 'orange'}, 86: {'well_id': 'F6', 'state': 'sample', 'colour': 'orange'}, 87: {'well_id': 'G6', 'state': 'sample', 'colour': 'orange'}, 88: {'well_id': 'H6', 'state': 'sample', 'colour': 'orange'}, 89: {'well_id': 'I6', 'state': 'sample', 'colour': 'orange'}, 90: {'well_id': 'J6', 'state': 'sample', 'colour': 'orange'}, 91: {'well_id': 'K6', 'state': 'sample', 'colour': 'orange'}, 92: {'well_id': 'L6', 'state': 'sample', 'colour': 'orange'}, 93: {'well_id': 'M6', 'state': 'sample', 'colour': 'orange'}, 94: {'well_id': 'N6', 'state': 'sample', 'colour': 'orange'}, 95: {'well_id': 'O6', 'state': 'empty', 'colour': 'blue'}, 96: {'well_id': 'P6', 'state': 'empty', 'colour': 'blue'}, 97: {'well_id': 'A7', 'state': 'empty', 'colour': 'blue'}, 98: {'well_id': 'B7', 'state': 'sample', 'colour': 'orange'}, 99: {'well_id': 'C7', 'state': 'sample', 'colour': 'orange'}, 100: {'well_id': 'D7', 'state': 'sample', 'colour': 'orange'}, 101: {'well_id': 'E7', 'state': 'sample', 'colour': 'orange'}, 102: {'well_id': 'F7', 'state': 'sample', 'colour': 'orange'}, 103: {'well_id': 'G7', 'state': 'sample', 'colour': 'orange'}, 104: {'well_id': 'H7', 'state': 'sample', 'colour': 'orange'}, 105: {'well_id': 'I7', 'state': 'sample', 'colour': 'orange'}, 106: {'well_id': 'J7', 'state': 'sample', 'colour': 'orange'}, 107: {'well_id': 'K7', 'state': 'sample', 'colour': 'orange'}, 108: {'well_id': 'L7', 'state': 'sample', 'colour': 'orange'}, 109: {'well_id': 'M7', 'state': 'sample', 'colour': 'orange'}, 110: {'well_id': 'N7', 'state': 'sample', 'colour': 'orange'}, 111: {'well_id': 'O7', 'state': 'empty', 'colour': 'blue'}, 112: {'well_id': 'P7', 'state': 'empty', 'colour': 'blue'}, 113: {'well_id': 'A8', 'state': 'empty', 'colour': 'blue'}, 114: {'well_id': 'B8', 'state': 'sample', 'colour': 'orange'}, 115: {'well_id': 'C8', 'state': 'sample', 'colour': 'orange'}, 116: {'well_id': 'D8', 'state': 'sample', 'colour': 'orange'}, 117: {'well_id': 'E8', 'state': 'sample', 'colour': 'orange'}, 118: {'well_id': 'F8', 'state': 'sample', 'colour': 'orange'}, 119: {'well_id': 'G8', 'state': 'sample', 'colour': 'orange'}, 120: {'well_id': 'H8', 'state': 'sample', 'colour': 'orange'}, 121: {'well_id': 'I8', 'state': 'sample', 'colour': 'orange'}, 122: {'well_id': 'J8', 'state': 'sample', 'colour': 'orange'}, 123: {'well_id': 'K8', 'state': 'sample', 'colour': 'orange'}, 124: {'well_id': 'L8', 'state': 'sample', 'colour': 'orange'}, 125: {'well_id': 'M8', 'state': 'sample', 'colour': 'orange'}, 126: {'well_id': 'N8', 'state': 'sample', 'colour': 'orange'}, 127: {'well_id': 'O8', 'state': 'empty', 'colour': 'blue'}, 128: {'well_id': 'P8', 'state': 'empty', 'colour': 'blue'}, 129: {'well_id': 'A9', 'state': 'empty', 'colour': 'blue'}, 130: {'well_id': 'B9', 'state': 'sample', 'colour': 'orange'}, 131: {'well_id': 'C9', 'state': 'sample', 'colour': 'orange'}, 132: {'well_id': 'D9', 'state': 'sample', 'colour': 'orange'}, 133: {'well_id': 'E9', 'state': 'sample', 'colour': 'orange'}, 134: {'well_id': 'F9', 'state': 'sample', 'colour': 'orange'}, 135: {'well_id': 'G9', 'state': 'sample', 'colour': 'orange'}, 136: {'well_id': 'H9', 'state': 'sample', 'colour': 'orange'}, 137: {'well_id': 'I9', 'state': 'sample', 'colour': 'orange'}, 138: {'well_id': 'J9', 'state': 'sample', 'colour': 'orange'}, 139: {'well_id': 'K9', 'state': 'sample', 'colour': 'orange'}, 140: {'well_id': 'L9', 'state': 'sample', 'colour': 'orange'}, 141: {'well_id': 'M9', 'state': 'sample', 'colour': 'orange'}, 142: {'well_id': 'N9', 'state': 'sample', 'colour': 'orange'}, 143: {'well_id': 'O9', 'state': 'empty', 'colour': 'blue'}, 144: {'well_id': 'P9', 'state': 'empty', 'colour': 'blue'}, 145: {'well_id': 'A10', 'state': 'empty', 'colour': 'blue'}, 146: {'well_id': 'B10', 'state': 'sample', 'colour': 'orange'}, 147: {'well_id': 'C10', 'state': 'sample', 'colour': 'orange'}, 148: {'well_id': 'D10', 'state': 'sample', 'colour': 'orange'}, 149: {'well_id': 'E10', 'state': 'sample', 'colour': 'orange'}, 150: {'well_id': 'F10', 'state': 'sample', 'colour': 'orange'}, 151: {'well_id': 'G10', 'state': 'sample', 'colour': 'orange'}, 152: {'well_id': 'H10', 'state': 'sample', 'colour': 'orange'}, 153: {'well_id': 'I10', 'state': 'sample', 'colour': 'orange'}, 154: {'well_id': 'J10', 'state': 'sample', 'colour': 'orange'}, 155: {'well_id': 'K10', 'state': 'sample', 'colour': 'orange'}, 156: {'well_id': 'L10', 'state': 'sample', 'colour': 'orange'}, 157: {'well_id': 'M10', 'state': 'sample', 'colour': 'orange'}, 158: {'well_id': 'N10', 'state': 'sample', 'colour': 'orange'}, 159: {'well_id': 'O10', 'state': 'empty', 'colour': 'blue'}, 160: {'well_id': 'P10', 'state': 'empty', 'colour': 'blue'}, 161: {'well_id': 'A11', 'state': 'empty', 'colour': 'blue'}, 162: {'well_id': 'B11', 'state': 'sample', 'colour': 'orange'}, 163: {'well_id': 'C11', 'state': 'sample', 'colour': 'orange'}, 164: {'well_id': 'D11', 'state': 'sample', 'colour': 'orange'}, 165: {'well_id': 'E11', 'state': 'sample', 'colour': 'orange'}, 166: {'well_id': 'F11', 'state': 'sample', 'colour': 'orange'}, 167: {'well_id': 'G11', 'state': 'sample', 'colour': 'orange'}, 168: {'well_id': 'H11', 'state': 'sample', 'colour': 'orange'}, 169: {'well_id': 'I11', 'state': 'sample', 'colour': 'orange'}, 170: {'well_id': 'J11', 'state': 'sample', 'colour': 'orange'}, 171: {'well_id': 'K11', 'state': 'sample', 'colour': 'orange'}, 172: {'well_id': 'L11', 'state': 'sample', 'colour': 'orange'}, 173: {'well_id': 'M11', 'state': 'sample', 'colour': 'orange'}, 174: {'well_id': 'N11', 'state': 'sample', 'colour': 'orange'}, 175: {'well_id': 'O11', 'state': 'empty', 'colour': 'blue'}, 176: {'well_id': 'P11', 'state': 'empty', 'colour': 'blue'}, 177: {'well_id': 'A12', 'state': 'empty', 'colour': 'blue'}, 178: {'well_id': 'B12', 'state': 'sample', 'colour': 'orange'}, 179: {'well_id': 'C12', 'state': 'sample', 'colour': 'orange'}, 180: {'well_id': 'D12', 'state': 'sample', 'colour': 'orange'}, 181: {'well_id': 'E12', 'state': 'sample', 'colour': 'orange'}, 182: {'well_id': 'F12', 'state': 'sample', 'colour': 'orange'}, 183: {'well_id': 'G12', 'state': 'sample', 'colour': 'orange'}, 184: {'well_id': 'H12', 'state': 'sample', 'colour': 'orange'}, 185: {'well_id': 'I12', 'state': 'sample', 'colour': 'orange'}, 186: {'well_id': 'J12', 'state': 'sample', 'colour': 'orange'}, 187: {'well_id': 'K12', 'state': 'sample', 'colour': 'orange'}, 188: {'well_id': 'L12', 'state': 'sample', 'colour': 'orange'}, 189: {'well_id': 'M12', 'state': 'sample', 'colour': 'orange'}, 190: {'well_id': 'N12', 'state': 'sample', 'colour': 'orange'}, 191: {'well_id': 'O12', 'state': 'empty', 'colour': 'blue'}, 192: {'well_id': 'P12', 'state': 'empty', 'colour': 'blue'}, 193: {'well_id': 'A13', 'state': 'empty', 'colour': 'blue'}, 194: {'well_id': 'B13', 'state': 'sample', 'colour': 'orange'}, 195: {'well_id': 'C13', 'state': 'sample', 'colour': 'orange'}, 196: {'well_id': 'D13', 'state': 'sample', 'colour': 'orange'}, 197: {'well_id': 'E13', 'state': 'sample', 'colour': 'orange'}, 198: {'well_id': 'F13', 'state': 'sample', 'colour': 'orange'}, 199: {'well_id': 'G13', 'state': 'sample', 'colour': 'orange'}, 200: {'well_id': 'H13', 'state': 'sample', 'colour': 'orange'}, 201: {'well_id': 'I13', 'state': 'sample', 'colour': 'orange'}, 202: {'well_id': 'J13', 'state': 'sample', 'colour': 'orange'}, 203: {'well_id': 'K13', 'state': 'sample', 'colour': 'orange'}, 204: {'well_id': 'L13', 'state': 'sample', 'colour': 'orange'}, 205: {'well_id': 'M13', 'state': 'sample', 'colour': 'orange'}, 206: {'well_id': 'N13', 'state': 'sample', 'colour': 'orange'}, 207: {'well_id': 'O13', 'state': 'empty', 'colour': 'blue'}, 208: {'well_id': 'P13', 'state': 'empty', 'colour': 'blue'}, 209: {'well_id': 'A14', 'state': 'empty', 'colour': 'blue'}, 210: {'well_id': 'B14', 'state': 'sample', 'colour': 'orange'}, 211: {'well_id': 'C14', 'state': 'sample', 'colour': 'orange'}, 212: {'well_id': 'D14', 'state': 'sample', 'colour': 'orange'}, 213: {'well_id': 'E14', 'state': 'sample', 'colour': 'orange'}, 214: {'well_id': 'F14', 'state': 'sample', 'colour': 'orange'}, 215: {'well_id': 'G14', 'state': 'sample', 'colour': 'orange'}, 216: {'well_id': 'H14', 'state': 'sample', 'colour': 'orange'}, 217: {'well_id': 'I14', 'state': 'sample', 'colour': 'orange'}, 218: {'well_id': 'J14', 'state': 'sample', 'colour': 'orange'}, 219: {'well_id': 'K14', 'state': 'sample', 'colour': 'orange'}, 220: {'well_id': 'L14', 'state': 'sample', 'colour': 'orange'}, 221: {'well_id': 'M14', 'state': 'sample', 'colour': 'orange'}, 222: {'well_id': 'N14', 'state': 'sample', 'colour': 'orange'}, 223: {'well_id': 'O14', 'state': 'empty', 'colour': 'blue'}, 224: {'well_id': 'P14', 'state': 'empty', 'colour': 'blue'}, 225: {'well_id': 'A15', 'state': 'empty', 'colour': 'blue'}, 226: {'well_id': 'B15', 'state': 'sample', 'colour': 'orange'}, 227: {'well_id': 'C15', 'state': 'sample', 'colour': 'orange'}, 228: {'well_id': 'D15', 'state': 'sample', 'colour': 'orange'}, 229: {'well_id': 'E15', 'state': 'sample', 'colour': 'orange'}, 230: {'well_id': 'F15', 'state': 'sample', 'colour': 'orange'}, 231: {'well_id': 'G15', 'state': 'sample', 'colour': 'orange'}, 232: {'well_id': 'H15', 'state': 'sample', 'colour': 'orange'}, 233: {'well_id': 'I15', 'state': 'sample', 'colour': 'orange'}, 234: {'well_id': 'J15', 'state': 'sample', 'colour': 'orange'}, 235: {'well_id': 'K15', 'state': 'sample', 'colour': 'orange'}, 236: {'well_id': 'L15', 'state': 'sample', 'colour': 'orange'}, 237: {'well_id': 'M15', 'state': 'sample', 'colour': 'orange'}, 238: {'well_id': 'N15', 'state': 'sample', 'colour': 'orange'}, 239: {'well_id': 'O15', 'state': 'empty', 'colour': 'blue'}, 240: {'well_id': 'P15', 'state': 'empty', 'colour': 'blue'}, 241: {'well_id': 'A16', 'state': 'empty', 'colour': 'blue'}, 242: {'well_id': 'B16', 'state': 'sample', 'colour': 'orange'}, 243: {'well_id': 'C16', 'state': 'sample', 'colour': 'orange'}, 244: {'well_id': 'D16', 'state': 'sample', 'colour': 'orange'}, 245: {'well_id': 'E16', 'state': 'sample', 'colour': 'orange'}, 246: {'well_id': 'F16', 'state': 'sample', 'colour': 'orange'}, 247: {'well_id': 'G16', 'state': 'sample', 'colour': 'orange'}, 248: {'well_id': 'H16', 'state': 'sample', 'colour': 'orange'}, 249: {'well_id': 'I16', 'state': 'sample', 'colour': 'orange'}, 250: {'well_id': 'J16', 'state': 'sample', 'colour': 'orange'}, 251: {'well_id': 'K16', 'state': 'sample', 'colour': 'orange'}, 252: {'well_id': 'L16', 'state': 'sample', 'colour': 'orange'}, 253: {'well_id': 'M16', 'state': 'sample', 'colour': 'orange'}, 254: {'well_id': 'N16', 'state': 'sample', 'colour': 'orange'}, 255: {'well_id': 'O16', 'state': 'empty', 'colour': 'blue'}, 256: {'well_id': 'P16', 'state': 'empty', 'colour': 'blue'}, 257: {'well_id': 'A17', 'state': 'empty', 'colour': 'blue'}, 258: {'well_id': 'B17', 'state': 'sample', 'colour': 'orange'}, 259: {'well_id': 'C17', 'state': 'sample', 'colour': 'orange'}, 260: {'well_id': 'D17', 'state': 'sample', 'colour': 'orange'}, 261: {'well_id': 'E17', 'state': 'sample', 'colour': 'orange'}, 262: {'well_id': 'F17', 'state': 'sample', 'colour': 'orange'}, 263: {'well_id': 'G17', 'state': 'sample', 'colour': 'orange'}, 264: {'well_id': 'H17', 'state': 'sample', 'colour': 'orange'}, 265: {'well_id': 'I17', 'state': 'sample', 'colour': 'orange'}, 266: {'well_id': 'J17', 'state': 'sample', 'colour': 'orange'}, 267: {'well_id': 'K17', 'state': 'sample', 'colour': 'orange'}, 268: {'well_id': 'L17', 'state': 'sample', 'colour': 'orange'}, 269: {'well_id': 'M17', 'state': 'sample', 'colour': 'orange'}, 270: {'well_id': 'N17', 'state': 'sample', 'colour': 'orange'}, 271: {'well_id': 'O17', 'state': 'empty', 'colour': 'blue'}, 272: {'well_id': 'P17', 'state': 'empty', 'colour': 'blue'}, 273: {'well_id': 'A18', 'state': 'empty', 'colour': 'blue'}, 274: {'well_id': 'B18', 'state': 'sample', 'colour': 'orange'}, 275: {'well_id': 'C18', 'state': 'sample', 'colour': 'orange'}, 276: {'well_id': 'D18', 'state': 'sample', 'colour': 'orange'}, 277: {'well_id': 'E18', 'state': 'sample', 'colour': 'orange'}, 278: {'well_id': 'F18', 'state': 'sample', 'colour': 'orange'}, 279: {'well_id': 'G18', 'state': 'sample', 'colour': 'orange'}, 280: {'well_id': 'H18', 'state': 'sample', 'colour': 'orange'}, 281: {'well_id': 'I18', 'state': 'sample', 'colour': 'orange'}, 282: {'well_id': 'J18', 'state': 'sample', 'colour': 'orange'}, 283: {'well_id': 'K18', 'state': 'sample', 'colour': 'orange'}, 284: {'well_id': 'L18', 'state': 'sample', 'colour': 'orange'}, 285: {'well_id': 'M18', 'state': 'sample', 'colour': 'orange'}, 286: {'well_id': 'N18', 'state': 'sample', 'colour': 'orange'}, 287: {'well_id': 'O18', 'state': 'empty', 'colour': 'blue'}, 288: {'well_id': 'P18', 'state': 'empty', 'colour': 'blue'}, 289: {'well_id': 'A19', 'state': 'empty', 'colour': 'blue'}, 290: {'well_id': 'B19', 'state': 'sample', 'colour': 'orange'}, 291: {'well_id': 'C19', 'state': 'sample', 'colour': 'orange'}, 292: {'well_id': 'D19', 'state': 'sample', 'colour': 'orange'}, 293: {'well_id': 'E19', 'state': 'sample', 'colour': 'orange'}, 294: {'well_id': 'F19', 'state': 'sample', 'colour': 'orange'}, 295: {'well_id': 'G19', 'state': 'sample', 'colour': 'orange'}, 296: {'well_id': 'H19', 'state': 'sample', 'colour': 'orange'}, 297: {'well_id': 'I19', 'state': 'sample', 'colour': 'orange'}, 298: {'well_id': 'J19', 'state': 'sample', 'colour': 'orange'}, 299: {'well_id': 'K19', 'state': 'sample', 'colour': 'orange'}, 300: {'well_id': 'L19', 'state': 'sample', 'colour': 'orange'}, 301: {'well_id': 'M19', 'state': 'sample', 'colour': 'orange'}, 302: {'well_id': 'N19', 'state': 'sample', 'colour': 'orange'}, 303: {'well_id': 'O19', 'state': 'empty', 'colour': 'blue'}, 304: {'well_id': 'P19', 'state': 'empty', 'colour': 'blue'}, 305: {'well_id': 'A20', 'state': 'empty', 'colour': 'blue'}, 306: {'well_id': 'B20', 'state': 'sample', 'colour': 'orange'}, 307: {'well_id': 'C20', 'state': 'sample', 'colour': 'orange'}, 308: {'well_id': 'D20', 'state': 'sample', 'colour': 'orange'}, 309: {'well_id': 'E20', 'state': 'sample', 'colour': 'orange'}, 310: {'well_id': 'F20', 'state': 'sample', 'colour': 'orange'}, 311: {'well_id': 'G20', 'state': 'sample', 'colour': 'orange'}, 312: {'well_id': 'H20', 'state': 'sample', 'colour': 'orange'}, 313: {'well_id': 'I20', 'state': 'sample', 'colour': 'orange'}, 314: {'well_id': 'J20', 'state': 'sample', 'colour': 'orange'}, 315: {'well_id': 'K20', 'state': 'sample', 'colour': 'orange'}, 316: {'well_id': 'L20', 'state': 'sample', 'colour': 'orange'}, 317: {'well_id': 'M20', 'state': 'sample', 'colour': 'orange'}, 318: {'well_id': 'N20', 'state': 'sample', 'colour': 'orange'}, 319: {'well_id': 'O20', 'state': 'empty', 'colour': 'blue'}, 320: {'well_id': 'P20', 'state': 'empty', 'colour': 'blue'}, 321: {'well_id': 'A21', 'state': 'empty', 'colour': 'blue'}, 322: {'well_id': 'B21', 'state': 'sample', 'colour': 'orange'}, 323: {'well_id': 'C21', 'state': 'sample', 'colour': 'orange'}, 324: {'well_id': 'D21', 'state': 'sample', 'colour': 'orange'}, 325: {'well_id': 'E21', 'state': 'sample', 'colour': 'orange'}, 326: {'well_id': 'F21', 'state': 'sample', 'colour': 'orange'}, 327: {'well_id': 'G21', 'state': 'sample', 'colour': 'orange'}, 328: {'well_id': 'H21', 'state': 'sample', 'colour': 'orange'}, 329: {'well_id': 'I21', 'state': 'sample', 'colour': 'orange'}, 330: {'well_id': 'J21', 'state': 'sample', 'colour': 'orange'}, 331: {'well_id': 'K21', 'state': 'sample', 'colour': 'orange'}, 332: {'well_id': 'L21', 'state': 'sample', 'colour': 'orange'}, 333: {'well_id': 'M21', 'state': 'sample', 'colour': 'orange'}, 334: {'well_id': 'N21', 'state': 'sample', 'colour': 'orange'}, 335: {'well_id': 'O21', 'state': 'empty', 'colour': 'blue'}, 336: {'well_id': 'P21', 'state': 'empty', 'colour': 'blue'}, 337: {'well_id': 'A22', 'state': 'empty', 'colour': 'blue'}, 338: {'well_id': 'B22', 'state': 'sample', 'colour': 'orange'}, 339: {'well_id': 'C22', 'state': 'sample', 'colour': 'orange'}, 340: {'well_id': 'D22', 'state': 'sample', 'colour': 'orange'}, 341: {'well_id': 'E22', 'state': 'sample', 'colour': 'orange'}, 342: {'well_id': 'F22', 'state': 'sample', 'colour': 'orange'}, 343: {'well_id': 'G22', 'state': 'sample', 'colour': 'orange'}, 344: {'well_id': 'H22', 'state': 'sample', 'colour': 'orange'}, 345: {'well_id': 'I22', 'state': 'sample', 'colour': 'orange'}, 346: {'well_id': 'J22', 'state': 'sample', 'colour': 'orange'}, 347: {'well_id': 'K22', 'state': 'sample', 'colour': 'orange'}, 348: {'well_id': 'L22', 'state': 'sample', 'colour': 'orange'}, 349: {'well_id': 'M22', 'state': 'sample', 'colour': 'orange'}, 350: {'well_id': 'N22', 'state': 'sample', 'colour': 'orange'}, 351: {'well_id': 'O22', 'state': 'empty', 'colour': 'blue'}, 352: {'well_id': 'P22', 'state': 'empty', 'colour': 'blue'}, 353: {'well_id': 'A23', 'state': 'empty', 'colour': 'blue'}, 354: {'well_id': 'B23', 'state': 'minimum', 'colour': 'yellow'}, 355: {'well_id': 'C23', 'state': 'minimum', 'colour': 'yellow'}, 356: {'well_id': 'D23', 'state': 'minimum', 'colour': 'yellow'}, 357: {'well_id': 'E23', 'state': 'minimum', 'colour': 'yellow'}, 358: {'well_id': 'F23', 'state': 'minimum', 'colour': 'yellow'}, 359: {'well_id': 'G23', 'state': 'minimum', 'colour': 'yellow'}, 360: {'well_id': 'H23', 'state': 'minimum', 'colour': 'yellow'}, 361: {'well_id': 'I23', 'state': 'minimum', 'colour': 'yellow'}, 362: {'well_id': 'J23', 'state': 'minimum', 'colour': 'yellow'}, 363: {'well_id': 'K23', 'state': 'minimum', 'colour': 'yellow'}, 364: {'well_id': 'L23', 'state': 'minimum', 'colour': 'yellow'}, 365: {'well_id': 'M23', 'state': 'minimum', 'colour': 'yellow'}, 366: {'well_id': 'N23', 'state': 'minimum', 'colour': 'yellow'}, 367: {'well_id': 'O23', 'state': 'empty', 'colour': 'blue'}, 368: {'well_id': 'P23', 'state': 'empty', 'colour': 'blue'}, 369: {'well_id': 'A24', 'state': 'empty', 'colour': 'blue'}, 370: {'well_id': 'B24', 'state': 'empty', 'colour': 'blue'}, 371: {'well_id': 'C24', 'state': 'empty', 'colour': 'blue'}, 372: {'well_id': 'D24', 'state': 'empty', 'colour': 'blue'}, 373: {'well_id': 'E24', 'state': 'empty', 'colour': 'blue'}, 374: {'well_id': 'F24', 'state': 'empty', 'colour': 'blue'}, 375: {'well_id': 'G24', 'state': 'empty', 'colour': 'blue'}, 376: {'well_id': 'H24', 'state': 'empty', 'colour': 'blue'}, 377: {'well_id': 'I24', 'state': 'empty', 'colour': 'blue'}, 378: {'well_id': 'J24', 'state': 'empty', 'colour': 'blue'}, 379: {'well_id': 'K24', 'state': 'empty', 'colour': 'blue'}, 380: {'well_id': 'L24', 'state': 'empty', 'colour': 'blue'}, 381: {'well_id': 'M24', 'state': 'empty', 'colour': 'blue'}, 382: {'well_id': 'N24', 'state': 'empty', 'colour': 'blue'}, 383: {'well_id': 'O24', 'state': 'empty', 'colour': 'blue'}, 384: {'well_id': 'P24', 'state': 'empty', 'colour': 'blue'}}, 'plate_type': 'plate_384'}
    z_prime_calc = True
    heatmap_colours = {'start': 'light red', 'mid': 'white', 'end': 'light green'}
    folder = "C:/Users/phch/PycharmProjects/structure_search/Bio Data/raw data"
    bio_data(config, folder, well_states_report, plate_analysis_dict, plate_layout, z_prime_calc, heatmap_colours)

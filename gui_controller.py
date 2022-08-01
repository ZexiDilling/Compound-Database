import copy
from gui_layout import GUILayout
from gui_functions import *
from json_handler import dict_reader, dict_writer
import configparser

def main(config):

    plate_file = config["files"]["plate_layouts"]
    try:
        plate_list, archive_plates_dict = dict_reader(plate_file)
    except TypeError:
        plate_list = []
        archive_plates_dict = {}

    gl = GUILayout(config, plate_list)

    window = gl.full_layout()
    window.maximize()

    #   WINDOW 1 - BIO  #
    graph_bio = window["-BIO_CANVAS-"]

    #   WINDOW 1 - PLATE LAYOUT #
    graph_plate = window["-CANVAS-"]
    dragging = False
    temp_selector = False
    plate_active = False

    color_select = {}
    for keys in list(config["plate_colouring"].keys()):
        color_select[keys] = config["plate_colouring"][keys]

    start_point = end_point = prior_rect = temp_tool = None
    well_dict = {}
    # COMPOUND TABLE CONSTANTS #
    all_data = None
    treedata = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        ###   WINDOW 1 - SEARCH     ###
        if event == "-SEARCH_ORIGIN-":
            values["-SEARCH_ORIGIN-"]
            temp_values = list(config[values["-SEARCH_ORIGIN-"]].keys())
            temp_value = temp_values[0]
            window["-SEARCH_WHO-"].update(values=temp_values, value=temp_value)

        if event == "-SS_METHOD-":
            if values["-SS_METHOD-"] == "morgan":
                window["-MORGAN_OPTIONS-"].update(visible=True)
                window["-MORGAN_CHIRALITY-"].update(visible=True)
                window["-MORGAN_FEATURES-"].update(visible=True)
                window["-BITS_TEXT-"].update(visible=True)
                window["-MORGAN_BITS-"].update(visible=True)
                window["-BOUND_TEXT-"].update(visible=True)
                window["-MORGAN_RANGE-"].update(visible=True)
            else:
                window["-MORGAN_OPTIONS-"].update(visible=False)
                window["-MORGAN_CHIRALITY-"].update(visible=False)
                window["-MORGAN_FEATURES-"].update(visible=False)
                window["-BITS_TEXT-"].update(visible=False)
                window["-MORGAN_BITS-"].update(visible=False)
                window["-BOUND_TEXT-"].update(visible=False)
                window["-MORGAN_RANGE-"].update(visible=False)

        if event == "-DRAW_MOL-":
            sg.popup("This does not work yet, sorry. Use Chemdraw and copy smiles code instead")

        ###     WINDOW 1 - BIO DATA         ###
        if event == "-BIO_PLATE_LAYOUT-":
            well_dict.clear()
            well_dict = copy.deepcopy(archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["well_layout"])
            plate_size = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["plate_type"]
            archive = True
            gui_tab = "bio"
            sample_type = values["-BIO_SAMPLE_TYPE-"]
            draw_plate(config, graph_bio, plate_size, well_dict, archive, gui_tab, sample_type)

        if event == "-BIO_SAMPLE_TYPE-":
            if values["-BIO_PLATE_LAYOUT-"]:
                well_dict.clear()
                well_dict = copy.deepcopy(archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["well_layout"])
                plate_size = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["plate_type"]
                archive = True
                gui_tab = "bio"
                sample_type = values["-BIO_SAMPLE_TYPE-"]
                draw_plate(config, graph_bio, plate_size, well_dict, archive, gui_tab, sample_type)

        if event == "-EXPORT_BIO-":
            if not values["-BIO_IMPORT_FOLDER-"]:
                sg.popup_error("Please choose a folder")
            elif not values["-BIO_PLATE_LAYOUT-"]:
                sg.popup_error("Please choose a plate layout")
            # elif not values["-BIO_ANALYSE_TYPE-"]:
            #     sg.popup_error("Please choose an analyse type")
            else:
                folder = values["-BIO_IMPORT_FOLDER-"]
                well_states_report = {
                    "sample": values["-BIO_SAMPLE-"],
                    "blank": values["-BIO_MIN-"],
                    "max": values["-BIO_MAX-"],
                    "minimum": values["-BIO_EMPTY-"],
                    "positive": values["-BIO_NEG_C-"],
                    "negative": values["-BIO_POS_C-"],
                    "empty": values["-BIO_BLANK-"]
                }
                plate_analysis_dict = {
                    "original": {"used": True, "methode": bio_data_functions.org, "heatmap": False},
                    "normalised": {"used": True, "methode": bio_data_functions.norm, "heatmap": values["-BIO_HEATMAP-"]},
                    "pora": {"used": True, "methode": bio_data_functions.pora, "heatmap": values["-BIO_HEATMAP-"]}}

                plate_layout = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]
                z_prime_calc = values["-BIO_Z-PRIME-"]

                # missing implimentations: "
                heatmap_colours = {"start": values["-HEAT_START-"],
                                   "mid": values["-HEAT_MID-"],
                                   "end": values["-HEAT_END-"]}
                state_colours = values["-BIO_STATE-"]
                export_folder = values["-BIO_EXPORT_FOLDER-"]

                worked = bio_data(config, folder, well_states_report, plate_analysis_dict, plate_layout,
                                          z_prime_calc, heatmap_colours)
                if worked:
                    sg.popup("Done")

        if event == "-BIO_ANALYSE_TYPE-":
            sg.popup("This functions does nothing ATM ")

        ###     WINDOW 1 - PLATE LAYOUT     ###
        if event == "-DRAW-":
            well_dict.clear()
            # sets the size of the well for when it draws the plate
            graph = graph_plate
            plate_type = values["-PLATE-"]
            archive_plates = values["-ARCHIVE-"]
            gui_tab = "plate_layout"
            sample_type = values["-RECT_SAMPLE_TYPE-"]

            if values["-ARCHIVE-"]:
                try:
                    well_dict = copy.deepcopy(archive_plates_dict[values["-ARCHIVE_PLATES-"]]["well_layout"])
                    window["-PLATE-"].update(archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"])
                    plate_type = archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"]

                except KeyError:
                    window["-ARCHIVE-"].update(False)
                    values["-ARCHIVE-"] = False

            well_dict, min_x, min_y, max_x, max_y = draw_plate(config, graph, plate_type, well_dict, archive_plates, gui_tab,
                                                               sample_type)
            plate_active = True

        if event == "-EXPORT_LAYOUT-":
            sg.PopupError("This is not working yet :D")

        if event == "-SAVE_LAYOUT-":
            if not well_dict:
                sg.PopupError("Please create a layout to save")
            else:
                temp_well_dict = {}
                temp_dict_name = sg.PopupGetText("Name plate layout")

                if temp_dict_name:
                    archive_plates_dict[temp_dict_name] = {}
                    for index, well_counter in enumerate(well_dict):
                        temp_well_dict[index + 1] = copy.deepcopy(well_dict[well_counter])

                    archive_plates_dict[temp_dict_name]["well_layout"] = temp_well_dict
                    archive_plates_dict[temp_dict_name]["plate_type"] = values["-PLATE-"]
                    dict_writer(plate_file, archive_plates_dict)
                    plate_list, archive_plates_dict = dict_reader(plate_file)
                    window["-ARCHIVE_PLATES-"].update(values=sorted(plate_list), value=plate_list[0])
                    window["-BIO_PLATE_LAYOUT-"].update(values=sorted(plate_list), value="")

        if event == "-DELETE_LAYOUT-":
            if not values["-ARCHIVE_PLATES-"]:
                sg.PopupError("Please select a layout to delete")
            else:
                archive_plates_dict.pop(values["-ARCHIVE_PLATES-"])
                plate_list.remove(values["-ARCHIVE_PLATES-"])
                try:
                    window["-ARCHIVE_PLATES-"].update(values=sorted(plate_list), value=plate_list[0])
                    window["-BIO_PLATE_LAYOUT-"].update(values=sorted(plate_list), value="")
                except IndexError:
                    window["-ARCHIVE_PLATES-"].update(values=[], value="")
                    window["-BIO_PLATE_LAYOUT-"].update(values=[], value="")
                dict_writer(plate_file, archive_plates_dict)

        if event == "-RENAME_LAYOUT-":
            if not values["-ARCHIVE_PLATES-"]:
                sg.PopupError("Please select a layout to rename")
            else:
                temp_dict_name = sg.PopupGetText("Name plate layout")
                if temp_dict_name:
                    archive_plates_dict[temp_dict_name] = archive_plates_dict[values["-ARCHIVE_PLATES-"]]
                    archive_plates_dict.pop(values["-ARCHIVE_PLATES-"])
                    plate_list.remove(values["-ARCHIVE_PLATES-"])
                    plate_list.append(temp_dict_name)
                    window["-ARCHIVE_PLATES-"].update(values=sorted(plate_list), value=plate_list[0])
                    window["-BIO_PLATE_LAYOUT-"].update(values=sorted(plate_list), value="")
                    dict_writer(plate_file, archive_plates_dict)

        # prints coordinate and well under the plate layout
        if event.endswith("+MOVE"):
            try:
                temp_well = graph_plate.get_figures_at_location(values['-CANVAS-'])[0]
                temp_well_id = well_dict[temp_well]["well_id"]
            except IndexError:
                temp_well_id = ""
            window["-INFO-"].update(value=f"{values['-CANVAS-']} {temp_well_id}")

        if event == "-CANVAS-":
            x, y = values["-CANVAS-"]
            if not dragging:
                start_point = (x, y)
                dragging = True
            else:
                end_point = (x, y)
            if prior_rect:
                graph_plate.delete_figure(prior_rect)

            # Choosing which tool to pain the plate with.
            if None not in (start_point, end_point):
                if values["-RECT_SAMPLES-"]:
                    temp_tool = "sample"
                elif values["-RECT_BLANK-"]:
                    temp_tool = "blank"
                elif values["-RECT_MAX-"]:
                    temp_tool = "max"
                if values["-RECT_MIN-"]:
                    temp_tool = "minimum"
                elif values["-RECT_NEG-"]:
                    temp_tool = "negative"
                elif values["-RECT_POS-"]:
                    temp_tool = "positive"
                elif values["-RECT_EMPTY-"]:
                    temp_tool = "empty"
                elif values["-COLOUR-"]:
                    temp_tool = "paint"
                temp_selector = True
                prior_rect = graph_plate.draw_rectangle(start_point, end_point, fill_color="",
                                                  line_color=config["plate_colouring"][temp_tool])

        # it does not always detect this event:
        elif event.endswith("+UP"):

            if temp_selector and plate_active:

                # if you drag and let go too fast, the values are set to None. this is to handle that bug
                if not start_point:
                    start_point = (0, 0)
                if not end_point:
                    end_point = (0, 0)

                # get a list of coordination within the selected area
                temp_x = []
                temp_y = []

                if start_point[0] < end_point[0]:
                    for x_cord in range(start_point[0], end_point[0]):
                        temp_x.append(x_cord)
                if start_point[0] > end_point[0]:
                    for x_cord in range(end_point[0], start_point[0]):
                        temp_x.append(x_cord)

                if start_point[1] < end_point[1]:
                    for y_cord in range(start_point[1], end_point[1]):
                        temp_y.append(y_cord)
                if start_point[1] > end_point[1]:
                    for y_cord in range(end_point[1], start_point[1]):
                        temp_y.append(y_cord)

                # This is to enable clicking on wells to mark them
                if not temp_x:
                    temp_x = [x]
                if not temp_y:
                    temp_y = [y]

                # makes a set, for adding wells, to avoid duplicates
                graphs_list = set()

                # goes over the coordinates and if they are within the bounds of the plate
                # if that is the case, then the figure for that location is added the set
                for index_x, cords_x in enumerate(temp_x):
                    for index_y, cords_y in enumerate(temp_y):
                        if min_x <= temp_x[index_x] <= max_x and min_y <= temp_y[index_y] <= max_y:
                            graphs_list.add(graph_plate.get_figures_at_location((temp_x[index_x], temp_y[index_y]))[0])

                # colours the wells in different colour, depending on if they are samples or blanks
                for wells in graphs_list:
                    color = color_select[temp_tool]
                    well_state = temp_tool
                    if color == "paint":
                        color = values["-COLOUR_CHOICE-"]
                    graph_plate.Widget.itemconfig(wells, fill=color)
                    well_dict[wells]["colour"] = color
                    well_dict[wells]["state"] = well_state

            # deletes the rectangle used for selection
            if prior_rect:
                graph_plate.delete_figure(prior_rect)

            # reset everything
            start_point, end_point = None, None
            dragging = False
            prior_rect = None
            temp_selector = False
            temp_tool = None

        ###     WINDOW 1 - UPDATE Database      ###
        if event == "-UPDATE_COMPOUND-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing compound data")
            update_database(values["-UPDATE_FOLDER-"], "compound_main")

        if event == "-UPDATE_MP-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing MotherPlate data")
            update_database(values["-UPDATE_FOLDER-"], "compound_mp")

        if event == "-UPDATE_DP-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing AssayPlate data")
            update_database(values["-UPDATE_FOLDER-"], "compound_dp")

        if event == "-UPDATE_PURITY-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing LCMS data")
            if values["-UPDATE_MS_MODE-"] == "Positive":
                ms_mode = "pos"
            else:
                ms_mode = "neg"
            purity_handler(values["-UPDATE_FOLDER-"], values["-UPDATE_UV-"], int(values["-UPDATE_UV_WAVE-"]), "all",
                           int(values["-UPDATE_UV_THRESHOLD-"]), float(values["-UPDATE_RT_SOLVENT-"]),
                           float(values["-UPDATE_MS_DELTA-"]), ms_mode, int(values["-UPDATE_MS_THRESHOLD-"]))

        if event == "-UPDATE_BIO-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing bio data")
            sg.PopupError("this is not working atm")

        if event == "-UPDATE_AUTO-":
            sg.PopupOKCancel("this is not working atm")

                        ### TABLE TABS ###

        ###     WINDOW 1 - SIMULATE         ###
        if event == "-SIM_INPUT_EQ-":

            if values["-SIM_INPUT_EQ-"] == "comPOUND":
                window["-SIM_COMPOUND_FRAME-"].update(visible=True)
                window["-SIM_MP_FRAME-"].update(visible=False)
                window["-SIM_DP_FRAME-"].update(visible=False)

            elif values["-SIM_INPUT_EQ-"] == "MP Production":
                window["-SIM_COMPOUND_FRAME-"].update(visible=False)
                window["-SIM_MP_FRAME-"].update(visible=True)
                window["-SIM_DP_FRAME-"].update(visible=False)

            elif values["-SIM_INPUT_EQ-"] == "DP production":
                window["-SIM_COMPOUND_FRAME-"].update(visible=False)
                window["-SIM_MP_FRAME-"].update(visible=False)
                window["-SIM_DP_FRAME-"].update(visible=True)

        if event == "-SIM_BUTTON-":
            if values["-SIM_INPUT_EQ-"] == "comPOUND":
                if not values["-SIM_INPUT_COMPOUND_FILE-"]:
                    sg.popup_error("Missing Compound file")
                else:
                    sg.Popup("not working atm")

            elif values["-SIM_INPUT_EQ-"] == "MP Production":
                if not values["-SIM_INPUT_MP_FILE-"]:
                    sg.popup_error("Missing 2D barcode file")
                else:
                    folder_output = values["-SIM_OUTPUT-"]
                    barcodes_2d = values["-SIM_INPUT_MP_FILE-"]
                    mp_name = values["-SIM_MP_NAME-"]
                    trans_vol = values["-SIM_MP_VOL-"]

                    mp_production_2d_to_pb_simulate(folder_output, barcodes_2d, mp_name, trans_vol)

                    sg.Popup("Done")

            elif values["-SIM_INPUT_EQ-"] == "DP production":
                if not values["-SIM_INPUT_DP_FILE-"]:
                    sg.popup_error("Missing PlateButler file")
                else:
                    sg.Popup("not working atm")


        ###     TAB GROUP EVENTS    ###
        if event == "-TABLE_TAB_GRP-":
            print(values["-TABLE_TAB_GRP-"])

        ###     WINDOW TABLES - COMPOUND TABLE      ###
        if event == "-TREE_DB-":
            try:
                temp_id = window.Element("-TREE_DB-").SelectedRows[0]
            except IndexError:
                pass
            # temp_info = window.Element("-TREE_DB-").TreeData.tree_dict[temp_id].values
            window["-INFO_NAME-"].update(value=compound_data[temp_id]["compound_id"])
            window["-INFO_SMILES-"].update(value=compound_data[temp_id]["smiles"])
            window["-INFO_MP_VOLUME-"].update(value=compound_data[temp_id]["volume"])
            window["-INFO_PIC-"].update(data=compound_data[temp_id]["png"])

        if event == "-C_TABLE_REFRESH-":
            if values["-ALL_COMPOUNDS-"]:
                values["-MP_AMOUNT-"] = compound_counter()
                values["-TRANS_VOL-"] = 0
                values["-IGNORE_ACTIVE-"] = True
                values["-SUB_SEARCH-"] = False

            if values["-PP-"] == "Assay Plates":
                table = "join_main_mp"
            else:
                table = "compound_main"

            if treedata:
                treedata = sg.TreeData()
                window['-TREE_DB-'].update(treedata)
                window["-C_TABLE_REFRESH-"].update(text="Refresh")
                window["-C_TABLE_COUNT-"].update(Text=f"Compounds: 0")

            else:
                try:
                    mp_amount = int(values["-MP_AMOUNT-"])
                    transferee_volume = float(values["-TRANS_VOL-"])
                    ignore_active = values["-IGNORE_ACTIVE-"]
                    sub_search = values["-SUB_SEARCH-"]
                    smiles = values["-SMILES-"]
                    sub_search_methode = values["-SS_METHOD-"]
                    threshold = float(values["-THRESHOLD-"])
                    source_table = table

                    treedata, all_data, compound_data, counter = table_update(mp_amount, transferee_volume,
                                                                              ignore_active, sub_search, smiles,
                                                                              sub_search_methode, threshold,
                                                                              source_table)
                    window['-TREE_DB-'].image_dict.clear()
                    window["-TREE_DB-"].update(treedata)
                    window["-C_TABLE_COUNT-"].update(Text=f"Compounds: {counter}")
                    window["-C_TABLE_REFRESH-"].update(text="Clear Table")

                except ValueError:
                    sg.Popup("Fill in missing data")

        if event == "-C_TABLE_EXPORT-":
            if not all_data:
                sg.popup_error("Missing table data")
            elif not values["-OUTPUT_FILE-"]:
                sg.popup_error("missing folder")
            else:
                if values["-C_TABLE_FILE_TYPE-"] == "Compound":
                    compound_export(values["-OUTPUT_FILE-"], all_data["compound_list"])


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)

    # sg.main_get_debug_data()
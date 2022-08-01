import copy

import gui_layout as gl
from gui_functions import *
from json_handler import dict_reader, dict_writer


def main(config):
    """Main gui controller"""

    window = gl.setup_main()
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-", "-ESCAPE-"):
            break
        if event == "-PLATES-":
            table_view()
        if event == "-UPDATE-":
            update_view()
        if event == "-PLATE_LAYOUT-":
            plate_layout(config)


def export_view(all_data):
    window = gl.setup_export()
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-", "-ESCAPE-"):
            break
        if event == "-COMPOUND-":
            if not value["-FOLDER-"]:
                sg.Popup("missing folder")
            else:
                compound_export(value["-FOLDER-"], all_data["compound_list"])


def update_view():
    window = gl.setup_update_db()
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-", "-ESCAPE-"):
            break
        if event == "-COMPOUND-":
            update_database(value["-FOLDER-"], "compound_main")
        if event == "-MP-":
            update_database(value["-FOLDER-"], "compound_mp")
        if event == "-DP-":
            update_database(value["-FOLDER-"], "compound_dp")
        if event == "-PURITY-":
            purity_updater_view(value["-FOLDER-"])
        if event == "-BIO-":
            ...


def purity_updater_view(folder):
    window = gl.setup_purity_updater()
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event in (sg.WIN_CLOSED, "-CANCEL-", "-ESCAPE-"):
            break
        if event == "-RUN-":

            if value["-MS_MODE-"] == "positive":
                ms_mode = "pos"
            else:
                ms_mode = "neg"
            purity_handler(folder, value["-UV-"], int(value["-UV_WAVE-"]), "all", value["-UV_THRESHOLD-"],
                           value["-RT_SOLVENT-"], value["-MS_DELTA-"], ms_mode, value["-MS_THRESHOLD-"])
            sg.popup("data transferred")
            break


def table_view():
    window = gl.setup_table()
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-", "-ESCAPE-"):
            break
        if event == "-REFRESH-":
            if value["-ALL_COMPOUNDS-"]:
                value["-MP_AMOUNT-"] = compound_counter()
                value["-TRANS_VOL-"] = 0
                value["-IGNORE_ACTIVE-"] = True
                value["-SUB_SEARCH-"] = False

            if value["-PP-"] == "Assay Plates":
                table = "join_main_mp"
            else:
                table = "compound_main"

            try:
                treedata, compound_list, all_data = table_update(int(value["-MP_AMOUNT-"]), float(value["-TRANS_VOL-"]),
                                                                 value["-IGNORE_ACTIVE-"], value["-SUB_SEARCH-"],
                                                                 value["-SMILES-"], value["-SEARCH_METHOD-"],
                                                                 int(value["-THRESHOLD-"]), table)

                window["-TREE_DB-"].update(treedata)

            except ValueError:
                sg.Popup("Fill in missing data")

        if event == "-EXPORT-":
            try:
                export_view(all_data)
            except UnboundLocalError:
                sg.popup("please select data")


def plate_layout(config):
    """
    GUI for drawing plate layouts
    :return: a dict over well ID and their state (blank/sample/paint)
    """

    plate_file = config["files"]["plate_layouts"]
    # plate_file = "plate_archive.txt"
    #
    try:
        plate_list, archive_plates_dict = dict_reader(plate_file)
    except TypeError:
        plate_list = []
        archive_plates_dict = {}
    window = gl.setup_plate_layout(config, plate_list)
    graph = window["-CANVAS-"]
    dragging = False
    temp_selector = False
    plate_active = False
    start_point = end_point = prior_rect = temp_tool = None
    well_dict = {}
    color_select = {
        "sample": "yellow",
        "blank": "blue",
        "paint": "paint"
    }

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-DRAW-":
            well_dict.clear()
            if values["-ARCHIVE-"]:
                try:
                    well_dict = copy.deepcopy(archive_plates_dict[values["-ARCHIVE_PLATES-"]]["well_layout"])
                    window["-PLATE-"].update(archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"])
                    values["-PLATE-"] = archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"]

                except KeyError:
                    window["-ARCHIVE-"].update(False)
                    values["-ARCHIVE-"] = False
            well_dict, min_x, min_y, max_x, max_y = draw_plate(graph, values["-PLATE-"], well_dict, values["-ARCHIVE-"])
            plate_active = True
        if event == "-EXPORT-":
            print(well_dict)

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

        if event == "-DELETE_LAYOUT-":
            if not values["-ARCHIVE_PLATES-"]:
                sg.PopupError("Please select a layout to delete")
            else:
                archive_plates_dict.pop(values["-ARCHIVE_PLATES-"])
                plate_list.remove(values["-ARCHIVE_PLATES-"])
                window["-ARCHIVE_PLATES-"].update(values=sorted(plate_list), value=plate_list[0])
                window["-ARCHIVE_PLATES-"].update()
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
                    dict_writer(plate_file, archive_plates_dict)

        if event.endswith("+MOVE"):
            try:
                temp_well = graph.get_figures_at_location(values['-CANVAS-'])[0]
                temp_well_id = well_dict[temp_well]["well_id"]
            except IndexError:
                temp_well_id = ""

            window["-INFO-"].update(value=f"mouse {values['-CANVAS-']} {temp_well_id}")

        if event == "-CANVAS-":
            x, y = values["-CANVAS-"]
            if not dragging:
                start_point = (x, y)
                dragging = True
                # drag_figures = graph.get_figures_at_location((x, y))
                # lastxy = x, y
            else:
                end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            # delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            # lastxy = x, y
            if None not in (start_point, end_point):
                if values["-RECT_SAMPLES-"]:
                    prior_rect = graph.draw_rectangle(start_point, end_point, fill_color="purple", line_color="green")
                    temp_selector = True
                    temp_tool = "sample"
                elif values["-RECT_DESELECT-"]:
                    prior_rect = graph.draw_rectangle(start_point, end_point, fill_color="", line_color="red")
                    temp_selector = True
                    temp_tool = "blank"
                elif values["-COLOUR-"]:
                    prior_rect = graph.draw_rectangle(start_point, end_point, fill_color="", line_color="orange")
                    temp_selector = True
                    temp_tool = "paint"

                # elif values['-ERASE-']:
                #     for figure in drag_figures:
                #         graph.delete_figure(figure)
                # elif values['-MOVE-']:
                #     for figure in drag_figures:
                #         graph.move_figure(figure, delta_x, delta_y)
                #         graph.update()

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
                            graphs_list.add(graph.get_figures_at_location((temp_x[index_x], temp_y[index_y]))[0])

                # colours the wells in different colour, depending on if they are samples or blanks
                for wells in graphs_list:
                    color = color_select[temp_tool]
                    well_state = temp_tool
                    if color == "paint":
                        color = values["-COLOUR_CHOICE-"]
                    graph.Widget.itemconfig(wells, fill=color)
                    well_dict[wells]["colour"] = color
                    well_dict[wells]["state"] = well_state

            # deletes the rectangle used for selection
            if prior_rect:
                graph.delete_figure(prior_rect)

            # reset everything
            start_point, end_point = None, None
            dragging = False
            prior_rect = None
            temp_selector = False
            temp_tool = None


def complete():
    window = gl.full_layout()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

if __name__ == "__main__":
    # table_view()
    # config = configparser.ConfigParser()
    # config.read("config.ini")
    # main(config)
    # update_view(config)
    complete()

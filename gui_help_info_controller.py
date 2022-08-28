import configparser

import PySimpleGUI as sg
from gui_help_info_layout import info_help_window
from gui_help_info_text import TextForInfo


def help_info_controller(config):

    window = info_help_window()
    tfi = TextForInfo(window, config)
    tfi.window_1_search_text()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "          Search          " \
                and not values["-INFO_HELP_SEARCH-"]:
            tfi.window_1_search_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "        Bio Data          "\
                and not values["-INFO_HELP_BIO_DATA-"]:
            tfi.window_1_bio_data_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "       Purity Data       "\
                and not values["-INFO_HELP_PURITY_DATA-"]:
            tfi.window_1_purity_data_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "      Plate Layout      "\
                and not values["-INFO_HELP_PLATE_LAYOUT-"]:
            tfi.window_1_plate_layout_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "          Update          "\
                and not values["-INFO_HELP_UPDATE-"]:
            tfi.window_1_update_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "           Sim             "\
                and not values["-INFO_HELP_SIM-"]:
            tfi.window_1_sim_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "    Compound Info    "\
                and not values["-INFO_HELP_COMPOUND_INFO-"]:
            tfi.window_2_info_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "         Bio Info          "\
                and not values["-INFO_HELP_BIO_INFO-"]:
            tfi.window_2_bio_info_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "       Purity Info        "\
                and not values["-INFO_HELP_PURITY_INFO-"]:
            tfi.window_2_purity_info_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "   Compound Table   "\
                and not values["-INFO_HELP_COMPOUND_TABLE-"]:
            tfi.window_3_compound_table_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "         Bio Table        "\
                and not values["-INFO_HELP_EXP_TABLE-"]:
            tfi.window_3_bio_exp_table_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "       Plate Table       "\
                and not values["-INFO_HELP_PLATE_TABLE-"]:
            tfi.window_3_plate_table_text()
        if event == "-HELP_INFO_TAB_GROUPS-" and values["-HELP_INFO_TAB_GROUPS-"] == "         Glossary         "\
                and not values["-INFO_HELP_GLOSSARY-"]:
            tfi.glossary()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    help_info_controller(config)
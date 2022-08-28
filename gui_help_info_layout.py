import PySimpleGUI as sg
from gui_help_info_text import *


def window_1_search():
    clm = sg.Frame("Search", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_SEARCH-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_1_bio_data():
    clm = sg.Frame("Bio Data", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_BIO_DATA-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_1_purity_data():
    clm = sg.Frame("Purity Data", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_PURITY_DATA-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_1_plate_layout():
    clm = sg.Frame("Plate Layout", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_PLATE_LAYOUT-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_1_update():
    clm = sg.Frame("Update", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_UPDATE-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_1_sim():
    clm = sg.Frame("Sim", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_SIM-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_2_compound_info():
    clm = sg.Frame("Compound Info", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_COMPOUND_INFO-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_2_bio_info():
    clm = sg.Frame("Bio Info", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_BIO_INFO-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_2_purity_info():
    clm = sg.Frame("Purity Info", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_PURITY_INFO-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_3_compound_table():
    clm = sg.Frame("Compound Table", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_COMPOUND_TABLE-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_3_bio_exp_table():
    clm = sg.Frame("Bio Experimental Table", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_EXP_TABLE-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def window_3_plate_table():
    clm = sg.Frame("Plate Table", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_PLATE_TABLE-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout


def glossary():
    clm = sg.Frame("Glossary", [[
        sg.Column([
            [sg.Multiline(key="-INFO_HELP_GLOSSARY-", disabled=True, size=(100, 50))]
        ])
    ]])

    layout = [[clm]]
    return layout



def tab_groups():

    tab_window_1_search = sg.Tab(
        "          Search          "
        , window_1_search(), expand_x=True)
    tab_window_1_bio_data = sg.Tab(
        "        Bio Data          "
        , window_1_bio_data(), expand_x=True, element_justification="center")
    tab_window_1_purity_data = sg.Tab(
        "       Purity Data       "
        , window_1_purity_data(), expand_x=True, element_justification="center")
    tab_window_1_plate_layout = sg.Tab(
        "      Plate Layout      "
        , window_1_plate_layout(), expand_x=True, element_justification="center")
    tab_window_1_update = sg.Tab(
        "          Update          "
        , window_1_update(), expand_x=True, element_justification="center")
    tab_window_1_sim = sg.Tab(
        "           Sim             "
        , window_1_sim(), expand_x=True, element_justification="center")
    tab_window_2_info = sg.Tab(
        "    Compound Info    "
        , window_2_compound_info(), expand_x=True, element_justification="center")
    tab_window_2_bio_info = sg.Tab(
        "         Bio Info          "
        , window_2_bio_info(), expand_x=True, element_justification="center")
    tab_window_2_purity_info = sg.Tab(
        "       Purity Info        "
        , window_2_purity_info(), expand_x=True, element_justification="center")
    tab_window_3_compound_table = sg.Tab(
        "   Compound Table   "
        , window_3_compound_table(), expand_x=True, element_justification="center")
    tab_window_3_bio_exp_table = sg.Tab(
        "         Bio Table        "
        , window_3_bio_exp_table(), expand_x=True, element_justification="center")
    tab_window_3_plate_table = sg.Tab(
        "       Plate Table       "
        , window_3_plate_table(), expand_x=True, element_justification="center")
    tab_glossary = sg.Tab(
        "         Glossary         "
        , glossary(), expand_x=True, element_justification="center")

    tab_group_tables = [tab_window_1_search, tab_window_1_bio_data, tab_window_1_purity_data,
                        tab_window_1_plate_layout, tab_window_1_update, tab_window_1_sim, tab_window_2_info,
                        tab_window_2_bio_info, tab_window_2_purity_info, tab_window_3_compound_table,
                        tab_window_3_bio_exp_table, tab_window_3_plate_table, tab_glossary]

    tab_layout = [[sg.TabGroup([tab_group_tables], tab_location="lefttop",
                               key="-HELP_INFO_TAB_GROUPS-", enable_events=True, selected_background_color="purple")]]
    return tab_layout


def info_help_window():

    tab_layout = tab_groups()

    return sg.Window("Info", tab_layout, finalize=True)

import copy
import os.path
import configparser

from gui_layout import GUILayout
from gui_settings_control import GUISettingsController
from gui_functions import *
from bio_data_functions import org, norm, pora, pora_internal
from json_handler import plate_dict_reader, dict_writer, dict_reader
from plate_formatting import plate_layout_re_formate
from gui_popup import matrix_popup
from gui_help_info_controller import help_info_controller
from config_writer import ConfigWriter
from database_startup import DatabaseSetUp
from visualization import *


def main(config):
    """
    The main control modul for the GUI.

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :return: This is a gui control modul. Returns depending on what is being done in the GUI
    """

    # importing config writer, to write data to the config file
    cw = ConfigWriter(config)
    try:
        if os.path.exists(config["Database"]["database"]):
            db_active = True
        else:
            cw.delete_all_info("Database")
            db_active = False
    except KeyError:
        db_active = False



    # File names, for files with dict over different kind of data.
    plate_file = config["files"]["plate_layouts"]
    bio_files = config["files"]["bio_experiments"]

    try:
        plate_list, archive_plates_dict = plate_dict_reader(plate_file)
    except TypeError:
        plate_list = []
        archive_plates_dict = {}

    gl = GUILayout(config, plate_list)

    window = gl.full_layout()
    window.maximize()

    #   Deaful Values / Simple Settings #
    simple_settings = {
        "plate_colouring": {
            "sample": config["plate_colouring"]["sample"],
            "blank": config["plate_colouring"]["blank"],
            "max": config["plate_colouring"]["max"],
            "minimum": config["plate_colouring"]["minimum"],
            "positive": config["plate_colouring"]["positive"],
            "negative": config["plate_colouring"]["negative"],
            "empty": config["plate_colouring"]["empty"]
        }
    }
    #   WINDOW 1 - SEARCH   #
    ac_use = False
    origin_use = False
    transferee_volume = None
    compound_table_clear = False
    current_table_data = None

    #   WINDOW 1 - BIO  #
    graph_bio = window["-BIO_CANVAS-"]
    bio_export_folder = None
    bio_final_report_setup = {
        "methods": {"original": config["Settings_bio"].getboolean("final_report_methods_original"),
                    "normalised": config["Settings_bio"].getboolean("final_report_methods_normalised"),
                    "pora": config["Settings_bio"].getboolean("final_report_methods_pora")},
        "analyse": {"sample": config["Settings_bio"].getboolean("final_report_analyse_sample"),
                    "minimum": config["Settings_bio"].getboolean("final_report_analyse_minimum"),
                    "max": config["Settings_bio"].getboolean("final_report_analyse_max"),
                    "empty": config["Settings_bio"].getboolean("final_report_analyse_empty"),
                    "negative": config["Settings_bio"].getboolean("final_report_analyse_negative"),
                    "positive": config["Settings_bio"].getboolean("final_report_analyse_positive"),
                    "blank": config["Settings_bio"].getboolean("final_report_analyse_blank")},
        "calc": {"original": {"overview": config["Settings_bio"].getboolean("final_report_calc_original_overview"),
                              "sample": config["Settings_bio"].getboolean("final_report_calc_original_sample"),
                              "minimum": config["Settings_bio"].getboolean("final_report_calc_original_minimum"),
                              "max": config["Settings_bio"].getboolean("final_report_calc_original_max"),
                              "empty": config["Settings_bio"].getboolean("final_report_calc_original_empty"),
                              "negative": config["Settings_bio"].
                                  getboolean("final_report_calc_original_negative"),
                              "positive": config["Settings_bio"].
                                  getboolean("final_report_calc_original_positive"),
                              "blank": config["Settings_bio"].getboolean("final_report_calc_original_blank")},
                 "normalised": {"overview": config["Settings_bio"].getboolean("final_report_calc_normalised_overview"),
                                "sample": config["Settings_bio"].getboolean("final_report_calc_normalised_sample"),
                                "minimum": config["Settings_bio"].getboolean("final_report_calc_normalised_minimum"),
                                "max": config["Settings_bio"].getboolean("final_report_calc_normalised_max"),
                                "empty": config["Settings_bio"].getboolean("final_report_calc_normalised_empty"),
                                "negative": config["Settings_bio"].
                                    getboolean("final_report_calc_normalised_negative"),
                                "positive": config["Settings_bio"].
                                    getboolean("final_report_calc_normalised_positive"),
                                "blank": config["Settings_bio"].getboolean("final_report_calc_normalised_blank")},
                 "pora": {"overview": config["Settings_bio"].getboolean("final_report_calc_pora_overview"),
                          "sample": config["Settings_bio"].getboolean("final_report_calc_pora_sample"),
                          "minimum": config["Settings_bio"].getboolean("final_report_calc_pora_minimum"),
                          "max": config["Settings_bio"].getboolean("final_report_calc_pora_max"),
                          "empty": config["Settings_bio"].getboolean("final_report_calc_pora_empty"),
                          "negative": config["Settings_bio"].getboolean("final_report_calc_pora_negative"),
                          "positive": config["Settings_bio"].getboolean("final_report_calc_pora_positive"),
                          "blank": config["Settings_bio"].getboolean("final_report_calc_pora_blank")},
                 "z_prime": config["Settings_bio"].getboolean("final_report_calc_Z_prime")},
        "pora_threshold": {"low": {"min": config["Settings_bio"].getfloat("final_report_pora_threshold_low_min"),
                                   "max": config["Settings_bio"].getfloat("final_report_pora_threshold_low_max")},
                           "mid": {"min": config["Settings_bio"].getfloat("final_report_pora_threshold_mid_min"),
                                   "max": config["Settings_bio"].getfloat("final_report_pora_threshold_mid_max")},
                           "high": {"min": config["Settings_bio"].getfloat("final_report_pora_threshold_high_min"),
                                    "max": config["Settings_bio"].getfloat("final_report_pora_threshold_high_max")}},
        "data": {"sample": {"matrix": config["Settings_bio"].getboolean("final_report_data_sample_matrix"),
                            "list": config["Settings_bio"].getboolean("final_report_data_sample_list"),
                            "max_min": config["Settings_bio"].getboolean("final_report_data_sample_max_min")},
                 "minimum": {"matrix": config["Settings_bio"].getboolean("final_report_data_minimum_matrix"),
                             "list": config["Settings_bio"].getboolean("final_report_data_minimum_list"),
                             "max_min": config["Settings_bio"].getboolean("final_report_data_minimum_max_min")},
                 "max": {"matrix": config["Settings_bio"].getboolean("final_report_data_max_matrix"),
                         "list": config["Settings_bio"].getboolean("final_report_data_max_list"),
                         "max_min": config["Settings_bio"].getboolean("final_report_data_max_max_min")},
                 "empty": {"matrix": config["Settings_bio"].getboolean("final_report_data_empty_matrix"),
                           "list": config["Settings_bio"].getboolean("final_report_data_empty_list"),
                           "max_min": config["Settings_bio"].getboolean("final_report_data_empty_max_min")},
                 "negative": {"matrix": config["Settings_bio"].getboolean("final_report_data_negative_matrix"),
                              "list": config["Settings_bio"].getboolean("final_report_data_negative_list"),
                              "max_min": config["Settings_bio"].getboolean("final_report_data_negative_max_min")},
                 "positive": {"matrix": config["Settings_bio"].getboolean("final_report_data_positive_matrix"),
                              "list": config["Settings_bio"].getboolean("final_report_data_positive_list"),
                              "max_min": config["Settings_bio"].getboolean("final_report_data_positive_max_min")},
                 "blank": {"matrix": config["Settings_bio"].getboolean("final_report_data_blank_matrix"),
                           "list": config["Settings_bio"].getboolean("final_report_data_blank_list"),
                           "max_min": config["Settings_bio"].getboolean("final_report_data_blank_max_min")},
                 "z_prime": {"matrix": config["Settings_bio"].getboolean("final_report_data_z_prime_matrix"),
                             "list": config["Settings_bio"].getboolean("final_report_data_z_prime_list"),
                             "max_min": config["Settings_bio"].getboolean("final_report_data_z_prime_max_min")}}}

    bio_plate_report_setup = {
        "well_states_report_method": {"original": config["Settings_bio"].
            getboolean("well_states_report_method_original"),
                                      "normalised": config["Settings_bio"].
                                          getboolean("well_states_report_method_normalised"),
                                      "pora": config["Settings_bio"].getboolean("well_states_report_method_pora"),
                                      "pora_internal": config["Settings_bio"].
                                          getboolean("well_states_report_method_pora_internal")},
        "well_states_report": {'sample': config["Settings_bio"].getboolean("plate_report_well_states_report_sample"),
                               'blank': config["Settings_bio"].getboolean("plate_report_well_states_report_blank"),
                               'max': config["Settings_bio"].getboolean("plate_report_well_states_report_max"),
                               'minimum': config["Settings_bio"].getboolean("plate_report_well_states_report_minimum"),
                               'positive': config["Settings_bio"].getboolean("plate_report_well_states_report_positive")
            ,
                               'negative': config["Settings_bio"].getboolean("plate_report_well_states_report_negative")
            ,
                               'empty': config["Settings_bio"].getboolean("plate_report_well_states_report_empty")},
        "calc_dict": {"original": {"use": config["Settings_bio"].getboolean("plate_report_calc_dict_original_use"),
                                   "avg": config["Settings_bio"].getboolean("plate_report_calc_dict_original_avg"),
                                   "stdev": config["Settings_bio"].getboolean("plate_report_calc_dict_original_stdev"),
                                   "state": {"sample": config["Settings_bio"].
                                       getboolean("plate_report_calc_dict_original_state_sample"),
                                             "minimum": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_minimum"),
                                             "max": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_max"),
                                             "empty": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_empty"),
                                             "negative": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_negative"),
                                             "positive": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_positive"),
                                             "blank": config["Settings_bio"].
                                                 getboolean("plate_report_calc_dict_original_state_blank")}},
                      "normalised": {"use": config["Settings_bio"].getboolean("plate_report_calc_dict_normalised_use"),
                                     "avg": config["Settings_bio"].
                                         getboolean("plate_report_calc_dict_normalised_avg"),
                                     "stdev": config["Settings_bio"].
                                         getboolean("plate_report_calc_dict_normalised_stdev"),
                                     "state": {"sample": config["Settings_bio"].
                                         getboolean("plate_report_calc_dict_normalised_"
                                                    "state_sample"),
                                               "minimum": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_minimum"),
                                               "max": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_max"),
                                               "empty": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_empty"),
                                               "negative": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_negative"),
                                               "positive": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_positive"),
                                               "blank": config["Settings_bio"].
                                                   getboolean("plate_report_calc_dict_normalised_"
                                                              "state_blank")}},
                      "pora": {"use": config["Settings_bio"].getboolean("plate_report_calc_dict_pora_use"),
                               "avg": config["Settings_bio"].getboolean("plate_report_calc_dict_pora_avg"),
                               "stdev": config["Settings_bio"].getboolean("plate_report_calc_dict_pora_stdev"),
                               "state": {"sample": config["Settings_bio"].
                                   getboolean("plate_report_calc_dict_pora_state_sample"),
                                         "minimum": config["Settings_bio"].
                                             getboolean("plate_report_calc_dict_pora_state_minimum"),
                                         "max": config["Settings_bio"].getboolean(
                                             "plate_report_calc_dict_pora_state_max"),
                                         "empty": config["Settings_bio"].
                                             getboolean("plate_report_calc_dict_pora_state_empty"),
                                         "negative": config["Settings_bio"].
                                             getboolean("plate_report_calc_dict_pora_state_negative"),
                                         "positive": config["Settings_bio"].
                                             getboolean("plate_report_calc_dict_pora_state_positive"),
                                         "blank": config["Settings_bio"].
                                             getboolean("plate_report_calc_dict_pora_state_blank")}},
                      "pora_internal": {"use": config["Settings_bio"].
                          getboolean("plate_report_calc_dict_pora_internal_use"),
                                        "avg": config["Settings_bio"].
                                            getboolean("plate_report_calc_dict_pora_internal_avg"),
                                        "stdev": config["Settings_bio"].
                                            getboolean("plate_report_calc_dict_pora_internal_stdev"),
                                        "state": {"sample": config["Settings_bio"].
                                            getboolean("plate_report_calc_dict_pora_internal_state_sample"),
                                                  "minimum": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_minimum"),
                                                  "max": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_max"),
                                                  "empty": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_empty"),
                                                  "negative": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_negative"),
                                                  "positive": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_positive"),
                                                  "blank": config["Settings_bio"].
                                                      getboolean("plate_report_calc_dict_pora_internal_state_blank")}},
                      "other": {"use": config["Settings_bio"].getboolean("plate_report_calc_dict_other_use"),
                                "calc": {"z_prime": config["Settings_bio"].
                                    getboolean("plate_report_calc_dict_other_calc_z_prime")}}},
        "plate_calc_dict": {
            "original": {"use": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_original_use"),
                         "avg": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_original_avg"),
                         "stdev": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_original_stdev"),
                         "state": {"sample": config["Settings_bio"].
                             getboolean("plate_report_plate_calc_dict_original_state_sample"),
                                   "minimum": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_minimum"),
                                   "max": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_max"),
                                   "empty": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_empty"),
                                   "negative": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_negative"),
                                   "positive": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_positive"),
                                   "blank": config["Settings_bio"].
                                       getboolean("plate_report_plate_calc_dict_original_state_blank")}},
            "normalised": {"use": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_normalised_use"),
                           "avg": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_normalised_avg"),
                           "stdev": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_normalised_stdev"),
                           "state": {"sample": config["Settings_bio"].
                               getboolean("plate_report_plate_calc_dict_normalised_state_sample"),
                                     "minimum": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_minimum"),
                                     "max": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_max"),
                                     "empty": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_empty"),
                                     "negative": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_negative"),
                                     "positive": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_positive"),
                                     "blank": config["Settings_bio"].
                                         getboolean("plate_report_plate_calc_dict_normalised_state_blank")}},
            "pora": {"use": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_pora_use"),
                     "avg": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_pora_avg"),
                     "stdev": config["Settings_bio"].getboolean("plate_report_plate_calc_dict_pora_stdev"),
                     "state": {"sample": config["Settings_bio"].
                         getboolean("plate_report_plate_calc_dict_pora_state_sample"),
                               "minimum": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_minimum"),
                               "max": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_max"),
                               "empty": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_empty"),
                               "negative": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_negative"),
                               "positive": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_positive"),
                               "blank": config["Settings_bio"].
                                   getboolean("plate_report_plate_calc_dict_pora_state_blank")}},
            "pora_internal": {"use": config["Settings_bio"].
                getboolean("plate_report_plate_calc_dict_pora_internal_use"),
                              "avg": config["Settings_bio"].
                                  getboolean("plate_report_plate_calc_dict_pora_internal_avg"),
                              "stdev": config["Settings_bio"].
                                  getboolean("plate_report_plate_calc_dict_pora_internal_stdev"),
                              "state": {"sample": config["Settings_bio"].
                                  getboolean("plate_report_plate_calc_dict_pora_internal_state_sample"),
                                        "minimum": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_minimum"),
                                        "max": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_max"),
                                        "empty": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_empty"),
                                        "negative": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_negative"),
                                        "positive": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_positive"),
                                        "blank": config["Settings_bio"].
                                            getboolean("plate_report_plate_calc_dict_pora_internal_state_blank")}},
        },
        "plate_analysis_dict": {"original": {"use": config["Settings_bio"].
            getboolean("plate_report_plate_analysis_dict_original_use"),
                                             "methode": org,
                                             "state_map": config["Settings_bio"].
                                                 getboolean("plate_report_plate_analysis_dict_original_state_map"),
                                             "heatmap": config["Settings_bio"].
                                                 getboolean("plate_report_plate_analysis_dict_original_heatmap"),
                                             "hit_map": config["Settings_bio"].
                                                 getboolean("plate_report_plate_analysis_dict_original_hit_map"),
                                             "none": config["Settings_bio"].
                                                 getboolean("plate_report_plate_analysis_dict_original_none")},
                                "normalised": {"use": config["Settings_bio"].
                                    getboolean("plate_report_plate_analysis_dict_normalised_use"),
                                               "methode": norm,
                                               "state_map": config["Settings_bio"].
                                                   getboolean("plate_report_plate_analysis_dict_normalised_state_map"),
                                               "heatmap": config["Settings_bio"].
                                                   getboolean("plate_report_plate_analysis_dict_normalised_heatmap"),
                                               "hit_map": config["Settings_bio"].
                                                   getboolean("plate_report_plate_analysis_dict_normalised_hit_map"),
                                               "none": config["Settings_bio"].
                                                   getboolean("plate_report_plate_analysis_dict_normalised_none")},
                                "pora": {"use": config["Settings_bio"].
                                    getboolean("plate_report_plate_analysis_dict_pora_use"),
                                         "methode": pora,
                                         "state_map": config["Settings_bio"].
                                             getboolean("plate_report_plate_analysis_dict_pora_state_map"),
                                         "heatmap": config["Settings_bio"].
                                             getboolean("plate_report_plate_analysis_dict_pora_heatmap"),
                                         "hit_map": config["Settings_bio"].
                                             getboolean("plate_report_plate_analysis_dict_pora_hit_map"),
                                         "none": config["Settings_bio"].
                                             getboolean("plate_report_plate_analysis_dict_pora_none")},
                                "pora_internal": {"use": config["Settings_bio"].
                                    getboolean("plate_report_plate_analysis_dict_pora_internal_use"),
                                                  "methode": pora_internal,
                                                  "state_map": config["Settings_bio"].
                                                      getboolean(
                                                      "plate_report_plate_analysis_dict_pora_internal_state_map")
                                    ,
                                                  "heatmap": config["Settings_bio"].
                                                      getboolean(
                                                      "plate_report_plate_analysis_dict_pora_internal_heatmap"),
                                                  "hit_map": config["Settings_bio"].
                                                      getboolean(
                                                      "plate_report_plate_analysis_dict_pora_internal_hit_map"),
                                                  "none": config["Settings_bio"].
                                                      getboolean("plate_report_plate_analysis_dict_pora_internal_none")}
                                },
        "z_prime_calc": config["Settings_bio"].getboolean("plate_report_z_prime_calc"),
        "heatmap_colours": {'low': config["Settings_bio"]["plate_report_heatmap_colours_low"],
                            'mid': config["Settings_bio"]["plate_report_heatmap_colours_mid"],
                            'high': config["Settings_bio"]["plate_report_heatmap_colours_high"]},
        "pora_threshold": {"low": {"min": config["Settings_bio"].getfloat("plate_report_pora_threshold_low_min"),
                                   "max": config["Settings_bio"].getfloat("plate_report_pora_threshold_low_max")},
                           "mid": {"min": config["Settings_bio"].getfloat("plate_report_pora_threshold_mid_min"),
                                   "max": config["Settings_bio"].getfloat("plate_report_pora_threshold_mid_max")},
                           "high": {"min": config["Settings_bio"].getfloat("plate_report_pora_threshold_high_min"),
                                    "max": config["Settings_bio"].getfloat("plate_report_pora_threshold_high_max")},
                           "colour": {"low": config["Settings_bio"]["plate_report_pora_threshold_colour_low"],
                                      "mid": config["Settings_bio"]["plate_report_pora_threshold_colour_mid"],
                                      "high": config["Settings_bio"]["plate_report_pora_threshold_colour_high"]}
                           }
    }

    #   WINDOW 1 - PURITY DATA
    ms_settings = {
        "ions": {"positive": {
            "m+3h": bool(config["Positive ion mode"]["m+3h"].split(",")[-1]),
            "m+2h+na": bool(config["Positive ion mode"]["m+2h+na"].split(",")[-1]),
            "m+h+2na": bool(config["Positive ion mode"]["m+h+2na"].split(",")[-1]),
            "m+3na": bool(config["Positive ion mode"]["m+3na"].split(",")[-1]),
            "m+2h": bool(config["Positive ion mode"]["m+2h"].split(",")[-1]),
            "m+h+nh4": bool(config["Positive ion mode"]["m+h+nh4"].split(",")[-1]),
            "m+h+na": bool(config["Positive ion mode"]["m+h+na"].split(",")[-1]),
            "m+h+k": bool(config["Positive ion mode"]["m+h+k"].split(",")[-1]),
            "m+acn+2h": bool(config["Positive ion mode"]["m+acn+2h"].split(",")[-1]),
            "m+2na": bool(config["Positive ion mode"]["m+2na"].split(",")[-1]),
            "m+2acn+2h": bool(config["Positive ion mode"]["m+2acn+2h"].split(",")[-1]),
            "m+3acn+2h": bool(config["Positive ion mode"]["m+3acn+2h"].split(",")[-1]),
            "m+h": bool(config["Positive ion mode"]["m+h"].split(",")[-1]),
            "m+nh4": bool(config["Positive ion mode"]["m+nh4"].split(",")[-1]),
            "m+na": bool(config["Positive ion mode"]["m+na"].split(",")[-1]),
            "m+ch3oh+h": bool(config["Positive ion mode"]["m+ch3oh+h"].split(",")[-1]),
            "m+k": bool(config["Positive ion mode"]["m+k"].split(",")[-1]),
            "m+acn+h": bool(config["Positive ion mode"]["m+acn+h"].split(",")[-1]),
            "m+2na-h": bool(config["Positive ion mode"]["m+2na-h"].split(",")[-1]),
            "m+isoprop+h": bool(config["Positive ion mode"]["m+isoprop+h"].split(",")[-1]),
            "m+acn+na": bool(config["Positive ion mode"]["m+acn+na"].split(",")[-1]),
            "m+2k+h": bool(config["Positive ion mode"]["m+2k+h"].split(",")[-1]),
            "m+dmso+h": bool(config["Positive ion mode"]["m+dmso+h"].split(",")[-1]),
            "m+2acn+h": bool(config["Positive ion mode"]["m+2acn+h"].split(",")[-1]),
            "m+isoprop+na+h": bool(config["Positive ion mode"]["m+isoprop+na+h"].split(",")[-1]),
            "2m+h": bool(config["Positive ion mode"]["2m+h"].split(",")[-1]),
            "2m+nh4": bool(config["Positive ion mode"]["2m+nh4"].split(",")[-1]),
            "2m+na": bool(config["Positive ion mode"]["2m+na"].split(",")[-1]),
            "2m+3h2o+2h": bool(config["Positive ion mode"]["2m+3h2o+2h"].split(",")[-1]),
            "2m+k": bool(config["Positive ion mode"]["2m+k"].split(",")[-1]),
            "2m+acn+h": bool(config["Positive ion mode"]["2m+acn+h"].split(",")[-1]),
            "2m+acn+na": bool(config["Positive ion mode"]["2m+acn+na"].split(",")[-1])
        },
            "negative": {
                "m-3h": bool(config["Negative ion mode"]["m-3h"].split(",")[-1]),
                "m-2h": bool(config["Negative ion mode"]["m-2h"].split(",")[-1]),
                "m-h2o-h": bool(config["Negative ion mode"]["m-h2o-h"].split(",")[-1]),
                "m-h": bool(config["Negative ion mode"]["m-h"].split(",")[-1]),
                "m+na-2h": bool(config["Negative ion mode"]["m+na-2h"].split(",")[-1]),
                "m+cl": bool(config["Negative ion mode"]["m+cl"].split(",")[-1]),
                "m+k-2h": bool(config["Negative ion mode"]["m+k-2h"].split(",")[-1]),
                "m+fa-h": bool(config["Negative ion mode"]["m+fa-h"].split(",")[-1]),
                "m+hac-h": bool(config["Negative ion mode"]["m+hac-h"].split(",")[-1]),
                "m+br": bool(config["Negative ion mode"]["m+br"].split(",")[-1]),
                "m+tfa-h": bool(config["Negative ion mode"]["m+tfa-h"].split(",")[-1]),
                "2m-h": bool(config["Negative ion mode"]["2m-h"].split(",")[-1]),
                "2m+fa-h": bool(config["Negative ion mode"]["2m+fa-h"].split(",")[-1]),
                "2m+hac-h": bool(config["Negative ion mode"]["2m+hac-h"].split(",")[-1]),
                "3m-h": bool(config["Negative ion mode"]["3m-h"].split(",")[-1]),
            }
        }
    }

    #   WINDOW 1 - PLATE LAYOUT #
    graph_plate = window["-CANVAS-"]
    dragging = False
    temp_selector = False
    plate_active = False

    #   WINDOW 2 - BIO EXP  #
    graph_bio_exp = window["-BIO_INFO_CANVAS-"]

    #   WINDOW 2 - PURITY INFO  #
    temp_purity_info_canvas = None

    color_select = {}
    for keys in list(config["plate_colouring"].keys()):
        color_select[keys] = config["plate_colouring"][keys]

    start_point = end_point = prior_rect = temp_tool = None
    well_dict = {}

    bio_info_sub_setting_tab_mapping_calc = False
    bio_info_sub_setting_tab_matrix_calc = False
    bio_info_sub_setting_tab_list_calc = False
    bio_info_sub_setting_tab_z_prime_calc = False
    bio_info_sub_setting_tab_plate_overview_calc = False
    bio_info_sub_setting_tab_overview_calc = False
    bio_info_sub_setting_tab_hit_list_calc = False

    # COMPOUND TABLE CONSTANTS #
    all_data = None
    treedata = None

    # BIO EXP TABLE CONSTANTS:
    bio_exp_table_data = None
    temp_well_id_bio_info = None
    plate_bio_info = None
    well_dict_bio_info = {}
    well_dict_bio_info_calc_handler = {}

    gsc = GUISettingsController(config, bio_final_report_setup, bio_plate_report_setup, ms_settings, simple_settings)
    window.Element("-BIO_INFO_MATRIX_TABLE-").Widget.configure(displaycolumns=[])
    plate_table_headings = ["Barcode", "Compound", "Well", "Volume", "Date", "Source Barcode", "Source Well"]
    window.Element("-PLATE_TABLE_TABLE-").Widget.configure(displaycolumns=plate_table_headings)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "-START_UP_DB-":
            if db_active:
                dsu = DatabaseSetUp(config, config["Database"]["database"])
            else:
                db = sg.PopupGetText("Choose database name")
                if db is not None:
                    db += ".db"
                    dsu = DatabaseSetUp(config, db)
            try:
                dsu.controller()
            except UnboundLocalError:
                print("No dp selected")
            else:
                config_update(config)
                window.close()
                window = gl.full_layout()

        #   WINDOW MENU         ###
        if event == "Open    Ctrl-O":
            db = sg.PopupGetFile("Choose database", file_types=(("Database", ".db"),))
            setting_dict = {"Database": {"database": db}}
            cw.run(setting_dict, "simple_settings", True)
            config_update(config)
            window.close()
            window = gl.full_layout()

        if event == "Save    Ctrl-S":
            sg.popup_error("Not working - Will never work... as all data is written to the DB... unless I want to add a temp DB...")

        if event == "About...":
            sg.popup_error("Not working")

        if event == "Info":
            help_info_controller(config)

        #   WINDOW 1 - SEARCH     ###
        if event == "-SEARCH_AC-":
            ac = values["-SEARCH_AC-"]
            origin_values = []
            if ac:
                for acs in ac:
                    acs = acs.casefold()
                    for values in config[f"database_specific_{acs}"]:
                        origin_values.append(config[f"database_specific_{acs}"][values])
            window["-SEARCH_ORIGIN-"].update(values=origin_values)

        if event == "-SUB_SEARCH_METHOD-":
            if values["-SUB_SEARCH_METHOD-"] == "morgan":
                window["-SUB_SEARCH_MORGAN_OPTIONS-"].update(visible=True)
                window["-SUB_SEARCH_MORGAN_CHIRALITY-"].update(visible=True)
                window["-SUB_SEARCH_MORGAN_FEATURES-"].update(visible=True)
                window["-SUB_SEARCH_BITS_TEXT-"].update(visible=True)
                window["-SUB_SEARCH_MORGAN_BITS-"].update(visible=True)
                window["-SUB_SEARCH_BOUND_TEXT-"].update(visible=True)
                window["-SUB_SEARCH_MORGAN_RANGE-"].update(visible=True)
            else:
                window["-SUB_SEARCH_MORGAN_OPTIONS-"].update(visible=False)
                window["-SUB_SEARCH_MORGAN_CHIRALITY-"].update(visible=False)
                window["-SUB_SEARCH_MORGAN_FEATURES-"].update(visible=False)
                window["-SUB_SEARCH_BITS_TEXT-"].update(visible=False)
                window["-SUB_SEARCH_MORGAN_BITS-"].update(visible=False)
                window["-SUB_SEARCH_BOUND_TEXT-"].update(visible=False)
                window["-SUB_SEARCH_MORGAN_RANGE-"].update(visible=False)

        if event == "-SEARCH_PLATE_PRODUCTION-" and values["-SEARCH_PLATE_PRODUCTION-"] == "Daughter Plates":
            window["-SEARCH_PLATE_LAYOUT-"].update(disabled=False)

        if event == "-SEARCH_PLATE_PRODUCTION-" and values["-SEARCH_PLATE_PRODUCTION-"] != "Daughter Plates":
            window["-SEARCH_PLATE_LAYOUT-"].update(disabled=True)
            window["-SEARCH_PLATE_LAYOUT_SAMPLE_AMOUNT-"].update(value=384)

        if event == "-SEARCH_PLATE_LAYOUT-":
            temp_counter = []
            for counter in archive_plates_dict[values["-SEARCH_PLATE_LAYOUT-"]]["well_layout"]:
                if archive_plates_dict[values["-SEARCH_PLATE_LAYOUT-"]]["well_layout"][counter]["state"] == "sample":
                    temp_counter.append(archive_plates_dict[values["-SEARCH_PLATE_LAYOUT-"]]["well_layout"][counter]
                                        ["well_id"])
            window["-SEARCH_PLATE_LAYOUT_SAMPLE_AMOUNT-"].update(value=len(temp_counter))

        if event == "-SUB_SEARCH_DRAW_MOL-":
            sg.popup("This does not work yet, sorry. Use Chemdraw and copy the smiles code in, instead")
        #
        # if event == "-SEARCH_ALL_COMPOUNDS-":
        #     window["-SEACH_ALL_NON_PLATED-"].update(value=False)
        #
        # if event == "-SEACH_ALL_NON_PLATED-":
        #     window["-SEARCH_ALL_COMPOUNDS-"].update(value=False)

        #     WINDOW 1 - BIO DATA         ###
        if event == "-BIO_PLATE_LAYOUT-":
            well_dict.clear()
            well_dict = copy.deepcopy(archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["well_layout"])
            well_dict = plate_layout_re_formate(well_dict)
            plate_size = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["plate_type"]
            archive = True
            gui_tab = "bio"
            sample_type = values["-BIO_SAMPLE_TYPE-"]
            draw_plate(config, graph_bio, plate_size, well_dict, gui_tab, archive, sample_layout=sample_type)

        if event == "-BIO_SAMPLE_TYPE-":
            if values["-BIO_PLATE_LAYOUT-"]:
                well_dict.clear()
                well_dict = copy.deepcopy(archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["well_layout"])
                well_dict = plate_layout_re_formate(well_dict)
                plate_size = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]["plate_type"]
                archive = True
                gui_tab = "bio"
                sample_type = values["-BIO_SAMPLE_TYPE-"]
                draw_plate(config, graph_bio, plate_size, well_dict, gui_tab, archive, sample_layout=sample_type)

        if event == "-BIO_COMPOUND_DATA-" and values["-BIO_COMPOUND_DATA-"]:
            window["-BIO_EXPERIMENT_ADD_TO_DATABASE-"].update(value=True)

        if event == "-BIO_EXPERIMENT_ADD_TO_DATABASE-" and not values["-BIO_ASSAY_NAME-"]:
            if values["-BIO_EXPERIMENT_ADD_TO_DATABASE-"]:
                assay_name = sg.popup_get_text("Assay Name?")
                if assay_name:
                    window["-BIO_ASSAY_NAME-"].update(value=assay_name)

        if event == "-EXPORT_BIO-":
            if not values["-BIO_PLATE_LAYOUT-"]:
                sg.popup_error("Please choose a plate layout")
            elif not values["-BIO_IMPORT_FOLDER-"]:
                sg.popup_error("Please choose an import folder")
            elif values["-BIO_COMBINED_REPORT-"] and not values["-BIO_EXPORT_FOLDER-"]:
                sg.popup_error("Please choose an export folder")
            elif values["-BIO_COMBINED_REPORT-"] and not values["-FINAL_BIO_NAME-"]:
                sg.popup_error("Please choose an Report name")
            elif values["-BIO_FINAL_REPORT_ADD_COMPOUNDS-"] and not values["-BIO_SAMPLE_LIST-"]:
                sg.popup_error("Please choose a file with compound information (NO CHECK FOR WRITE FORMATE FILE)")
            elif values["-BIO_EXPERIMENT_ADD_TO_DATABASE-"] and not values["-BIO_ASSAY_NAME-"]:
                sg.popup_error("Please choose an Assay name")
            elif values["-BIO_EXPERIMENT_ADD_TO_DATABASE-"] and not values["-BIO_RESPONSIBLE-"]:
                sg.popup_error("Please choose an Responsible ")
            # Missing setting move moving files after analyse is done.
            # elif not values["-BIO_ANALYSE_TYPE-"]:
            #     sg.popup_error("Please choose an analyse type")
            else:
                bio_import_folder = values["-BIO_IMPORT_FOLDER-"]
                plate_layout = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]

                final_report_name = values["-FINAL_BIO_NAME-"]
                if not bio_export_folder:
                    bio_export_folder = values["-BIO_EXPORT_FOLDER-"]

                analyse_method = values["-BIO_ANALYSE_TYPE-"]
                worked, all_plates_data, date = bio_data(config, bio_import_folder, plate_layout,
                                                         bio_plate_report_setup,
                                                         analyse_method)

                if values["-BIO_COMBINED_REPORT-"]:
                    bio_full_report("single point", all_plates_data, bio_final_report_setup, bio_export_folder,
                                    final_report_name)

                if values["-BIO_EXPERIMENT_ADD_TO_DATABASE-"]:
                    assay_name = values["-BIO_ASSAY_NAME-"]
                    responsible = values["-BIO_RESPONSIBLE-"]
                    plate_layout = values["-BIO_PLATE_LAYOUT-"]

                    bio_experiment_to_database(assay_name, all_plates_data, plate_layout, date, responsible, config,
                                               bio_files)

                if worked:
                    sg.popup("Done")

        if event == "-BIO_COMBINED_REPORT-" and not values["-FINAL_BIO_NAME-"]:
            final_report_name = sg.popup_get_text("Final Report Name?")
            window["-FINAL_BIO_NAME-"].update(value=final_report_name)

        if event == "-BIO_REPORT_SETTINGS-" or event == "-PURITY_ADVANCED_SETTINGS-":
            reports = gsc.main_settings_controller(bio_final_report_setup, bio_plate_report_setup, ms_settings)
            if reports:
                bio_final_report_setup, bio_plate_report_setup, ms_settings, simple_settings = reports
                set_colours(window, reports)

        if event == "-BIO_ANALYSE_TYPE-":
            sg.popup("This functions does nothing ATM ")

        if event == "-BIO_SEND_TO_INFO-":
            if not values["-BIO_PLATE_LAYOUT-"]:
                sg.popup_error("Please choose a plate layout")
            elif not values["-BIO_IMPORT_FOLDER-"]:
                sg.popup_error("Please choose an import folder")

            else:
                bio_import_folder = values["-BIO_IMPORT_FOLDER-"]
                plate_layout = archive_plates_dict[values["-BIO_PLATE_LAYOUT-"]]
                analyse_method = values["-BIO_ANALYSE_TYPE-"]
                write_to_excel = False
                _, all_plates_data, date = bio_data(config, bio_import_folder, plate_layout,
                                                         bio_plate_report_setup,
                                                         analyse_method, write_to_excel)

                gui_tab = "bio_exp"
                archive = True

                file_name = "bio_experiments.txt"
                # plate_dict_name = bio_exp_table_data[values["-BIO_EXP_TABLE-"][0]][2]
                plate_bio_info = all_plates_data

                bio_info_plate_layout = plate_layout
                bio_info_plate_size = plate_layout["plate_type"]
                bio_info_state_dict = copy.deepcopy(plate_layout["well_layout"])
                bio_info_state_dict = plate_layout_re_formate(bio_info_state_dict)

                well_dict_bio_info, bio_info_min_x, bio_info_min_y, bio_info_max_x, bio_info_max_y \
                    = draw_plate(config, graph_bio_exp, bio_info_plate_size, bio_info_state_dict, gui_tab, archive)

                bio_info_plates = []
                bio_info_states = []
                bio_info_analyse_method = []
                bio_info_calc = []
                for plates in plate_bio_info:
                    bio_info_plates.append(plates)
                    for method in plate_bio_info[plates]["calculations"]:
                        if method != "other":
                            if method not in bio_info_analyse_method:
                                bio_info_analyse_method.append(method)
                            for state in plate_bio_info[plates]["calculations"][method]:
                                if state not in bio_info_states:
                                    bio_info_states.append(state)
                                for calc in plate_bio_info[plates]["calculations"][method][state]:
                                    if calc not in bio_info_calc:
                                        bio_info_calc.append(calc)
                        if method == "other":
                            for calc_other in plate_bio_info[plates]["calculations"][method]:
                                if calc_other not in bio_info_calc:
                                    bio_info_calc.append(calc_other)

                # Main settings info
                window["-BIO_INFO_ANALYSE_METHOD-"].Update(value="original")
                window["-BIO_INFO_MAPPING-"].Update(value="state mapping")
                window["-BIO_INFO_ANALYSE_METHOD-"].update(values=bio_info_analyse_method,
                                                           value=bio_info_analyse_method[0])
                window["-BIO_INFO_PLATES-"].update(values=bio_info_plates, value=bio_info_plates[0])
                window["-BIO_INFO_STATES-"].update(values=bio_info_states)

                # Map settings
                list_box_index = None
                for index_state, values in enumerate(bio_info_states):
                    if values == "sample":
                        list_box_index = index_state
                    if not list_box_index:
                        list_box_index = 0

                window["-BIO_INFO_STATE_LIST_BOX-"].update(values=bio_info_states, set_to_index=list_box_index)

                # Matrix Settings
                window["-BIO_INFO_MATRIX_METHOD-"].update(values=bio_info_analyse_method)
                window["-BIO_INFO_MATRIX_STATE-"].update(values=bio_info_states)
                window["-BIO_INFO_MATRIX_CALC-"].update(values=bio_info_calc)

                # # List settings
                # window["-BIO_INFO_LIST_METHOD-"].update(values=bio_info_analyse_method, value=bio_info_analyse_method[0])
                # window["-BIO_INFO_LIST_STATE-"].update(values=bio_info_states, value=bio_info_states[0])
                # window["-BIO_INFO_LIST_CALC-"].update(values=bio_info_calc, value=bio_info_calc[0])

                # Overview settings
                window["-BIO_INFO_PLATE_OVERVIEW_METHOD_LIST-"].update(values=bio_info_analyse_method,
                                                                       set_to_index=len(bio_info_analyse_method) - 1)
                window["-BIO_INFO_PLATE_OVERVIEW_STATE_LIST-"].update(values=bio_info_states,
                                                                      set_to_index=len(bio_info_states) - 1)
                window["-BIO_INFO_PLATE_OVERVIEW_PLATE-"].update(values=bio_info_plates, value=bio_info_plates[0])
                window["-BIO_INFO_OVERVIEW_METHOD-"].update(values=bio_info_analyse_method,
                                                            value=bio_info_analyse_method[0])
                window["-BIO_INFO_OVERVIEW_STATE-"].update(values=bio_info_states, value=bio_info_states[0])

                # HIT List settings
                window["-BIO_INFO_HIT_LIST_PLATES-"].update(values=bio_info_plates, value=bio_info_plates[0])
                window["-BIO_INFO_HIT_LIST_METHOD-"].update(values=bio_info_analyse_method,
                                                            value=bio_info_analyse_method[-1])
                window["-BIO_INFO_HIT_LIST_STATE-"].update(values=bio_info_states, value="sample")

                # Popup Matrix
                method_values = bio_info_analyse_method
                state_values = bio_info_states
                calc_values = bio_info_calc

                # bio_info_sub_setting_tab_mapping_calc = True
                # bio_info_sub_setting_tab_matrix_calc = True
                # bio_info_sub_setting_tab_list_calc = True
                bio_info_sub_setting_tab_overview_calc = True
                bio_info_sub_setting_tab_plate_overview_calc = True
                bio_info_sub_setting_tab_z_prime_calc = True
                bio_info_sub_setting_tab_hit_list_calc = True

        #   WINDOW 1 - Purity           ###
        if event == "-PURITY_DATA_IMPORT-":
            folder = values["-PURITY_DATA_IMPORT_FOLDER-"]
            add_to_database = values["-PURITY_DATA_ADD_TO_DATABASE-"]
            purity_data, samples = import_ms_data(folder, add_to_database, config)

            window["-PURITY_INFO_SAMPLE_BOX-"].update(values=samples)
            window["-PURITY_INFO_SAMPLE_TABLE-"].update(values=purity_data)

        if event == "-PURITY_INFO_SAMPLE_BOX-":
            samples = values["-PURITY_INFO_SAMPLE_BOX-"]

            purity_info_canvas = window["-PURITY_INFO_CANVAS-"]
            if samples:
                plot_style = uv_chromatogram(purity_data, purity_info_canvas, samples)
            else:
                fig = plt.gcf()
                plt.close(fig)
                temp_purity_info_canvas.get_tk_widget().forget()

            if temp_purity_info_canvas is not None:
                if not temp_purity_info_canvas == plot_style:
                    fig = plt.gcf()
                    plt.close(fig)
                    temp_purity_info_canvas.get_tk_widget().forget()
                else:
                    plot_style.get_tk_widget().forget()
            if samples:
                plot_style.draw()
                plot_style.get_tk_widget().pack()
            try:
                window.refresh()
            except AttributeError:
                print("AttributeError")
            temp_purity_info_canvas = plot_style

        #     WINDOW 1 - PLATE LAYOUT     ###
        if event == "-TAB_GROUP_ONE-" and values["-TAB_GROUP_ONE-"] == "Plate layout":
            window["-BIO_INFO_MOVE-"].update(value=False)
            window["-RECT_BIO_MOVE-"].update(value=True)

        if event == "-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-":
            if values["-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-"] != "None":
                window["-PLATE_LAYOUT_COLOUR_CHOSE-"].update(button_color=values["-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-"])

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
                    well_dict = plate_layout_re_formate(well_dict)
                    window["-PLATE-"].update(archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"])
                    plate_type = archive_plates_dict[values["-ARCHIVE_PLATES-"]]["plate_type"]

                except KeyError:
                    window["-ARCHIVE-"].update(False)
                    values["-ARCHIVE-"] = False

            well_dict, min_x, min_y, max_x, max_y = draw_plate(config, graph, plate_type, well_dict, gui_tab,
                                                               archive_plates, sample_layout=sample_type)
            plate_active = True

        if event == "-EXPORT_LAYOUT-":
            if not well_dict:
                sg.PopupError("Please create a layout to Export")
            name = sg.PopupGetText("Name the file")
            if name:
                folder = sg.PopupGetFolder("Choose save location")
                if folder:
                    plate_layout_to_excel(well_dict, name, folder)

                    sg.Popup("Done")

        if event == "-SAVE_LAYOUT-":
            if not well_dict:
                sg.PopupError("Please create a layout to save")
            elif any("paint" in stuff.values() for stuff in well_dict.values()):
                sg.PopupError("Can't save layout with paint as well states")
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
                    plate_list, archive_plates_dict = plate_dict_reader(plate_file)
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

        if event == "-RECT_BIO_MOVE-":
            if values["-RECT_BIO_MOVE-"]:
                window["-BIO_INFO_MOVE-"].update(value=False)
            if not values["-RECT_BIO_MOVE-"]:
                window["-BIO_INFO_MOVE-"].update(value=True)

        # Used both for Plate layout and Bio Info
        # prints coordinate and well under the plate layout
        if event.endswith("+MOVE"):

            if values["-BIO_INFO_MOVE-"]:
                try:
                    temp_well_bio_info = graph_bio_exp.get_figures_at_location(values['-BIO_INFO_CANVAS-'])[0]
                    temp_well_id_bio_info = well_dict_bio_info[temp_well_bio_info]["well_id"]
                except IndexError:
                    temp_well_id_bio_info = ""
                window["-INFO_BIO_GRAPH_TARGET-"].update(value=f"{temp_well_id_bio_info}")

                if temp_well_id_bio_info:
                    temp_plate_name = values["-BIO_INFO_PLATES-"]
                    temp_analyse_method = values["-BIO_INFO_ANALYSE_METHOD-"]

                    temp_plate_wells_bio_info = plate_bio_info[temp_plate_name]["plates"][temp_analyse_method]["wells"]
                    window["-INFO_BIO_WELL_VALUE-"].update(value=temp_plate_wells_bio_info[temp_well_id_bio_info])

            if values["-RECT_BIO_MOVE-"]:
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
                                                        line_color="white")

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
                        color = values["-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-"]
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

        #     WINDOW 1 - UPDATE Database      ###
        if event == "-UPDATE_COMPOUND-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing compound data")
            else:
                update_database(values["-UPDATE_FOLDER-"], "compound_main", None, config)
                config_update(config)
                window.close()
                window = gl.full_layout()

        if event == "-UPDATE_MP-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing MotherPlate data")
            else:
                update_database(values["-UPDATE_FOLDER-"], "compound_mp", "pb_mp_output", config)
                sg.popup("Done")

        if event == "-UPDATE_DP-":
            if not values["-UPDATE_FOLDER-"]:
                sg.popup_error("Please select a folder containing AssayPlate data")
            else:
                update_database(values["-UPDATE_FOLDER-"], "compound_dp", "echo_dp_out", config)

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
            sg.popup_error("this is not working atm")

        if event == "-UPDATE_AUTO-":
            sg.PopupOKCancel("this is not working atm")

        #     WINDOW 1 - SIMULATE         ###
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

        if event == "-SIM_RUN-":
            if values["-SIM_INPUT_EQ-"] == "comPOUND":
                if not values["-SIM_INPUT_COMPOUND_FILE-"]:
                    sg.popup_error("Missing Compound file")
                else:
                    tube_file = values["-SIM_INPUT_COMPOUND_FILE-"]
                    output_folder = values["-SIM_OUTPUT-"]

                    compound_freezer_to_2d_simulate(tube_file, output_folder)

                    sg.Popup("Done")

            elif values["-SIM_INPUT_EQ-"] == "MP Production":
                if not values["-SIM_INPUT_MP_FILE-"]:
                    sg.popup_error("Missing 2D barcode file")
                else:
                    output_folder = values["-SIM_OUTPUT-"]
                    barcodes_2d = values["-SIM_INPUT_MP_FILE-"]
                    mp_name = values["-SIM_MP_NAME-"]
                    trans_vol = values["-SIM_MP_VOL-"]

                    mp_production_2d_to_pb_simulate(output_folder, barcodes_2d, mp_name, trans_vol)

                    sg.Popup("Done")

            elif values["-SIM_INPUT_EQ-"] == "DP production":
                if not values["-SIM_INPUT_DP_FILE-"]:
                    sg.popup_error("Missing PlateButler file")
                else:
                    sg.Popup("not working atm")

            else:
                print(values["-SIM_INPUT_EQ-"])

        # TABLE TABS ###

        #     TAB GROUP EVENTS    ###


        #     WINDOW TABLES - COMPOUND TABLE      ###
        if event == "-TREE_DB-":
            try:
                temp_id = window.Element("-TREE_DB-").SelectedRows[0]
            except IndexError:
                pass
            # temp_info = window.Element("-TREE_DB-").TreeData.tree_dict[temp_id].values
            window["-COMPOUND_INFO_ID-"].update(value=compound_data[temp_id]["compound_id"])
            window["-COMPOUND_INFO_SMILES-"].update(value=compound_data[temp_id]["smiles"])
            window["-COMPOUND_INFO_MP_VOLUME-"].update(value=compound_data[temp_id]["volume"])
            window["-COMPOUND_INFO_PIC-"].update(data=compound_data[temp_id]["png"])
            window["-COMPOUND_INFO_ORIGIN_ID-"].update(value=compound_data[temp_id]["origin_id"])
            window["-COMPOUND_INFO_CONCENTRATION-"].update(value=compound_data[temp_id]["concentration"])

            search_limiter_origin = {"academic_commercial": {"value": values["-SEARCH_AC-"],
                                                      "operator": "IN",
                                                      "target_column": "ac",
                                                      "use": ac_use}, "vendor_center": {"value": values["-SEARCH_ORIGIN-"],
                                                "operator": "IN",
                                                "target_column": "origin",
                                                "use": origin_use}}
            all_data_origin, _ = grab_table_data(config, "origin", search_limiter_origin)
            window["-COMPOUND_INFO_AC-"].update(value=all_data_origin[0][1])
            window["-COMPOUND_INFO_ORIGIN-"].update(value=all_data_origin[0][2])

            compound_id = compound_data[temp_id]["compound_id"]
            table_data = update_plate_table(compound_id, config)

        if event == "-C_TABLE_REFRESH-":
            if not compound_table_clear:
                if values["-SEARCH_ALL_COMPOUNDS-"]:
                    values["-IGNORE_ACTIVE-"] = True
                    values["-SUB_SEARCH-"] = False
                    values["-SEARCH_PLATE_AMOUNT_ALL-"] = True
                    values["-SEARCH_IGNORE_VOLUME-"] = True
                    values["-SEARCH_AC-"] = None
                    values["-SEARCH_ORIGIN-"] = None

                if values["-SEARCH_PLATE_PRODUCTION-"] == "Daughter Plates":
                    table = "join_main_mp"

                elif values["-SEARCH_PLATE_PRODUCTION-"] == "Mother Plates":
                    table = config["Tables"]["compound_main"]
                current_table_data = values["-SEARCH_PLATE_PRODUCTION-"]

                if values["-SEARCH_PLATE_AMOUNT-"] == "" and not values["-SEARCH_PLATE_AMOUNT_ALL-"]:
                    sg.popup_error("Please fill out plate amount")
                elif not values["-SEARCH_TRANS_VOL-"] and not values["-SEARCH_IGNORE_VOLUME-"]:
                    sg.popup_error("Please specify transferee amount")
                else:
                    if not values["-SEARCH_PLATE_AMOUNT_ALL-"]:
                        mp_amount = int(values["-SEARCH_PLATE_AMOUNT-"])
                    else:
                        mp_amount = None
                    if not values["-SEARCH_IGNORE_VOLUME-"]:
                        transferee_volume = float(values["-SEARCH_TRANS_VOL-"])
                    else:
                        transferee_volume = None

                    ignore_active = values["-SEARCH_IGNORE_PLATED_COMPOUNDS-"]
                    sub_search = values["-SUB_SEARCH-"]
                    smiles = values["-SUB_SEARCH_SMILES-"]
                    sub_search_methode = values["-SUB_SEARCH_METHOD-"]
                    threshold = float(values["-SUB_SEARCH_THRESHOLD-"])
                    source_table = table

                    if values["-SEARCH_AC-"]:
                        ac_use = True
                    else:
                        ac_use = False

                    if values["-SEARCH_ORIGIN-"]:
                        origin_use = True
                    else:
                        origin_use = False

                    samples_per_plate = int(values["-SEARCH_PLATE_LAYOUT_SAMPLE_AMOUNT-"])
                    search_limiter = {
                        config["Tables"]["compound_source"]: {"academic_commercial": {"value": values["-SEARCH_AC-"],
                                                                                      "operator": "IN",
                                                                                      "target_column": "ac",
                                                                                      "use": ac_use},
                                                              "vendor_center": {"value": values["-SEARCH_ORIGIN-"],
                                                                                "operator": "IN",
                                                                                "target_column": "origin",
                                                                                "use": origin_use}},
                        config["Tables"]["compound_main"]: {"origin_id": {"value": "",
                                                                          "operator": "IN",
                                                                          "target_column": "ac_id",
                                                                          "use": ac_use},
                                                            "volume": {"value": transferee_volume,
                                                                       "operator": "<",
                                                                       "target_column": "volume",
                                                                       "use": not values["-SEARCH_IGNORE_VOLUME-"]}},
                        "join_tables": {config["Tables"]["compound_main"]: {},
                                        config["Tables"]["compound_mp_table"]: {
                                             "compound_id": {"value": "",
                                                             "operator": "IN",
                                                             "target_column": "compound_id",
                                                             "use": False}},
                                         "shared_data": "compound_id"}
                    }

                    table_data = table_update_tree(mp_amount, samples_per_plate, ignore_active, sub_search, smiles,
                                                   sub_search_methode, threshold, source_table, search_limiter, config)
                    if table_data:
                        treedata, all_data, compound_data, counter = table_data
                        window['-TREE_DB-'].image_dict.clear()
                        window["-TREE_DB-"].update(treedata)
                        window["-C_TABLE_COUNT-"].update(f"Compounds: {counter}")
                        window["-C_TABLE_REFRESH-"].update(text="Clear Table")
                        compound_table_clear = True
                    else:
                        if values["-SEARCH_ALL_COMPOUNDS-"]:
                            sg.popup_error("All compounds are in MotherPlates")
                        else:
                            sg.popup_error("Database is empty")
                    #
                    # except ValueError:
                    #     sg.Popup("Fill in missing data")

            elif compound_table_clear:
                window['-TREE_DB-'].image_dict.clear()
                treedata = sg.TreeData()
                window['-TREE_DB-'].update(treedata)
                window["-C_TABLE_REFRESH-"].update(text="Refresh")
                window["-C_TABLE_COUNT-"].update(f"Compounds: 0")
                window['-TREE_DB-'].image_dict.clear()
                compound_table_clear = False

        if event == "-C_TABLE_EXPORT-":
            if not all_data:
                sg.popup_error("Missing table data")
            elif not values["-SEARCH_OUTPUT_FOLDER-"]:
                sg.popup_error("missing folder")
            else:
                if current_table_data == "Mother Plates":
                    output_folder = values["-SEARCH_OUTPUT_FOLDER-"]
                    all_compound_data = all_data["compound_list"]

                    compound_export(output_folder, all_compound_data)
                    file_location = f"{values['-SEARCH_OUTPUT_FOLDER-']}/comPOUND"

                elif current_table_data == "Daughter Plates":

                    if not values["-SEARCH_PLATE_AMOUNT-"]:
                        sg.PopupError("Please fill out plate Amount")
                    elif not values["-SEARCH_TRANS_VOL-"]:
                        sg.PopupError("Please fill out Transferee volume")
                    elif not values["-SEARCH_PLATE_LAYOUT-"]:
                        sg.PopupError("Please select a plate Layout for the DP production")
                    dp_name = sg.PopupGetText("Dp name? ")
                    if dp_name:
                        plate_layout = archive_plates_dict[values["-SEARCH_PLATE_LAYOUT-"]]
                        sample_amount = int(values["-SEARCH_PLATE_LAYOUT_SAMPLE_AMOUNT-"])
                        transferee_volume = values["-SEARCH_TRANS_VOL-"]
                        output_folder = values["-SEARCH_OUTPUT_FOLDER-"]
                        print(all_data)
                        mp_data = all_data["mp_data"]

                        dp_creator(plate_layout, sample_amount, mp_data, transferee_volume, dp_name, output_folder)

                        file_location = f"{values['-SEARCH_OUTPUT_FOLDER-']}/dp_output/"

                sg.popup(f"Done - files are located {file_location}")

        #   WINDOW TABLE - BIO EXPERIMENT TABLE     ###
        if event == "-TAB_GROUP_TWO-" and values["-TAB_GROUP_TWO-"] == "bio info":
            window["-RECT_BIO_MOVE-"].update(value=False)
            window["-BIO_INFO_MOVE-"].update(value=True)

        # Getting information to INFO BIO
        if event == "-BIO_EXP_TABLE-":
            if bio_exp_table_data:
                if not values["-BIO_INFO_ANALYSE_METHOD-"]:
                    window["-BIO_INFO_ANALYSE_METHOD-"].Update(value="original")
                if not values["-BIO_INFO_MAPPING-"]:
                    window["-BIO_INFO_MAPPING-"].Update(value="state mapping")

            gui_tab = "bio_exp"
            archive = True

            file_name = "bio_experiments.txt"
            plate_dict_name = bio_exp_table_data[values["-BIO_EXP_TABLE-"][0]][2]
            plate_bio_info = dict_reader(file_name)[plate_dict_name]

            bio_info_plate_layout = bio_exp_table_data[values["-BIO_EXP_TABLE-"][0]][3]
            bio_info_plate_size = archive_plates_dict[bio_info_plate_layout]["plate_type"]
            bio_info_state_dict = copy.deepcopy(archive_plates_dict[bio_info_plate_layout]["well_layout"])
            bio_info_state_dict = plate_layout_re_formate(bio_info_state_dict)

            well_dict_bio_info, bio_info_min_x, bio_info_min_y, bio_info_max_x, bio_info_max_y \
                = draw_plate(config, graph_bio_exp, bio_info_plate_size, bio_info_state_dict, gui_tab, archive)

            bio_info_plates = []
            bio_info_states = []
            bio_info_analyse_method = []
            bio_info_calc = []
            for plates in plate_bio_info:
                bio_info_plates.append(plates)
                for method in plate_bio_info[plates]["calculations"]:
                    if method != "other":
                        if method not in bio_info_analyse_method:
                            bio_info_analyse_method.append(method)
                        for state in plate_bio_info[plates]["calculations"][method]:
                            if state not in bio_info_states:
                                bio_info_states.append(state)
                            for calc in plate_bio_info[plates]["calculations"][method][state]:
                                if calc not in bio_info_calc:
                                    bio_info_calc.append(calc)
                    if method == "other":
                        for calc_other in plate_bio_info[plates]["calculations"][method]:
                            if calc_other not in bio_info_calc:
                                bio_info_calc.append(calc_other)

            # Main settings info
            window["-BIO_INFO_ANALYSE_METHOD-"].update(values=bio_info_analyse_method, value=bio_info_analyse_method[0])
            window["-BIO_INFO_PLATES-"].update(values=bio_info_plates, value=bio_info_plates[0])
            window["-BIO_INFO_STATES-"].update(values=bio_info_states)

            # Map settings
            list_box_index = None
            for index_state, values in enumerate(bio_info_states):
                if values == "sample":
                    list_box_index = index_state
                if not list_box_index:
                    list_box_index = 0

            window["-BIO_INFO_STATE_LIST_BOX-"].update(values=bio_info_states, set_to_index=list_box_index)

            # Matrix Settings
            window["-BIO_INFO_MATRIX_METHOD-"].update(values=bio_info_analyse_method)
            window["-BIO_INFO_MATRIX_STATE-"].update(values=bio_info_states)
            window["-BIO_INFO_MATRIX_CALC-"].update(values=bio_info_calc)

            # # List settings
            # window["-BIO_INFO_LIST_METHOD-"].update(values=bio_info_analyse_method, value=bio_info_analyse_method[0])
            # window["-BIO_INFO_LIST_STATE-"].update(values=bio_info_states, value=bio_info_states[0])
            # window["-BIO_INFO_LIST_CALC-"].update(values=bio_info_calc, value=bio_info_calc[0])

            # Overview settings
            window["-BIO_INFO_PLATE_OVERVIEW_METHOD_LIST-"].update(values=bio_info_analyse_method,
                                                                   set_to_index=len(bio_info_analyse_method) - 1)
            window["-BIO_INFO_PLATE_OVERVIEW_STATE_LIST-"].update(values=bio_info_states,
                                                                  set_to_index=len(bio_info_states) - 1)
            window["-BIO_INFO_PLATE_OVERVIEW_PLATE-"].update(values=bio_info_plates, value=bio_info_plates[0])
            window["-BIO_INFO_OVERVIEW_METHOD-"].update(values=bio_info_analyse_method,
                                                        value=bio_info_analyse_method[0])
            window["-BIO_INFO_OVERVIEW_STATE-"].update(values=bio_info_states, value=bio_info_states[0])

            # HIT List settings
            window["-BIO_INFO_HIT_LIST_PLATES-"].update(values=bio_info_plates, value=bio_info_plates[0])
            window["-BIO_INFO_HIT_LIST_METHOD-"].update(values=bio_info_analyse_method,
                                                        value=bio_info_analyse_method[-1])
            window["-BIO_INFO_HIT_LIST_STATE-"].update(values=bio_info_states, value="sample")

            # Popup Matrix
            method_values = bio_info_analyse_method
            state_values = bio_info_states
            calc_values = bio_info_calc

            # bio_info_sub_setting_tab_mapping_calc = True
            # bio_info_sub_setting_tab_matrix_calc = True
            # bio_info_sub_setting_tab_list_calc = True
            bio_info_sub_setting_tab_overview_calc = True
            bio_info_sub_setting_tab_plate_overview_calc = True
            bio_info_sub_setting_tab_z_prime_calc = True
            bio_info_sub_setting_tab_hit_list_calc = True

        if event == "-BIO_EXP_TABLE_REFRESH-":
            start_date = values["-BIO_EXP_TABLE_DATE_START_TARGET-"]
            end_date = values["-BIO_EXP_TABLE_DATE_END_TARGET-"]
            bio_exp_table_responsible = values["-BIO_EXP_TABLE_RESPONSIBLE-"]

            if start_date:
                use_start_date = True
            else:
                use_start_date = False
            if end_date:
                use_end_date = True
            else:
                use_end_date = False
            if bio_exp_table_responsible:
                use_responsible = True
            else:
                use_responsible = False


            search_limiter = {
                "start_date": {"value": start_date, "operator": "<", "target_column": "date", "use": use_start_date},
                "end_date": {"value": end_date, "operator": ">", "target_column": "date", "use": use_end_date},
                "responsible": {"value": bio_exp_table_responsible, "operator": "=", "target_column": "responsible",
                                "use": use_responsible}
            }

            table_name = "bio_experiment"

            bio_exp_table_data, headlines = grab_table_data(config, table_name, search_limiter)
            # print(table_data)

            window["-BIO_EXP_TABLE-"].update(values=bio_exp_table_data)

        #   WINDOW TABLE - LC EXPERIMENT    ###
        if event == "-TABLE_TAB_GRP-" and values["-TABLE_TAB_GRP-"] == "LC Experiment table":
            # print("update listbox with data, if list box is empty")
            all_data, headlines = grab_table_data(config, "lc_experiment", None)
            window["-LC_MS_TABLE_BATCH_LIST_BOX-"].update(values=all_data)

        if event == "-LC_MS_TABLE_DATE_START_TARGET-" or event == "-LC_MS_TABLE_DATE_END_TARGET-":
            start_date = values["-LC_MS_TABLE_DATE_START_TARGET-"]
            end_date = values["-LC_MS_TABLE_DATE_END_TARGET-"]

            if start_date:
                use_start_date = True
            else:
                use_start_date = False
            if end_date:
                use_end_date = True
            else:
                use_end_date = False

            search_limiter = {
                "start_date": {"value": start_date, "operator": "<", "target_column": "date", "use": use_start_date},
                "end_date": {"value": end_date, "operator": ">", "target_column": "date", "use": use_end_date},
            }

            table_name = "lc_experiment"

            table_data, _ = grab_table_data(config, table_name, search_limiter)
            table_data_2, _ = grab_table_data(config, table_name, None)

            window["-LC_MS_TABLE_BATCH_LIST_BOX-"].update(values=table_data)

        if event == "-LC_MS_TABLE_BATCH_LIST_BOX-":
            batch_date = values["-LC_MS_TABLE_BATCH_LIST_BOX-"]
            batch = []
            for data in batch_date:
                batch.append(data[0])

            if batch:
                search_limiter = {
                    "batch": {"value": batch, "operator": "IN", "target_column": "batch", "use": True},
                }
                table_name = "lc_raw"
                table_data, _ = grab_table_data(config, table_name, None)
                print(table_data)

                window["-LC_MS_SAMPLE_TABLE-"].update(values=table_data)


        #   WINDOW TABLE - PLATE TABLE      ###
        if event == "-PLATE_TABLE_CHOOSER-"\
                or event == "-PLATE_TABLE_START_DATE_TARGET-" and values["-PLATE_TABLE_CHOOSER-"]\
                or event == "-PLATE_TABLE_END_DATE_TARGET-" and values["-PLATE_TABLE_CHOOSER-"]:

            table_dict = {"Mother Plates": "mp_plates", "Daughter Plates": "dp_plates"}

            if values["-PLATE_TABLE_START_DATE_TARGET-"]:
                use_start_date = True
            else:
                use_start_date = False
            if values["-PLATE_TABLE_END_DATE_TARGET-"]:
                use_end_date = True
            else:
                use_end_date = False

            search_limiter = {
                "start_date": {"value": values["-PLATE_TABLE_START_DATE_TARGET-"], "operator": "<", "target_column":
                               "date", "use": use_start_date},
                "end_date": {"value": values["-PLATE_TABLE_END_DATE_TARGET-"], "operator": ">", "target_column":
                             "date", "use": use_end_date},
            }
            plate_data, _ = grab_table_data(config, table_dict[values["-PLATE_TABLE_CHOOSER-"]], search_limiter)
            if plate_data:
                plates = []
                for plate in plate_data:
                    plates.append(plate[0])

                window["-PLATE_TABLE_BARCODE_LIST_BOX-"].update(values=plates)
            else:
                window["-PLATE_TABLE_BARCODE_LIST_BOX-"].update(values=[[]])

        if event == "-PLATE_TABLE_BARCODE_LIST_BOX-":
            table_dict = {"Mother Plates": {"clm": "mp_barcode", "table": "compound_mp"},
                          "Daughter Plates": {"clm": "dp_barcode", "table": "compound_dp"}}
            search_limiter = {"academic_commercial": {"value": values["-PLATE_TABLE_BARCODE_LIST_BOX-"],
                                                      "operator": "IN",
                                                      "target_column": table_dict[values["-PLATE_TABLE_CHOOSER-"]]["clm"],
                                                      "use": True}}

            plate_data, _ = grab_table_data(config, table_dict[values["-PLATE_TABLE_CHOOSER-"]]["table"], search_limiter)

            # print(headings)
            if values["-PLATE_TABLE_BARCODE_LIST_BOX-"]:
                window["-PLATE_TABLE_TABLE-"].update(values=plate_data)
            else:
                window["-PLATE_TABLE_TABLE-"].update(values=[])

        #   WINDOW 2 - COMPOUND INFO    ###
        if event == "-COMPOUND_INFO_SEARCH_COMPOUND_ID-":
            search_limiter = {"academic_commercial": {"value": values["-COMPOUND_INFO_ID-"],
                                                      "operator": "=",
                                                      "target_column": "compound_id",
                                                      "use": True}}

            all_data_compound, _ = grab_table_data(config, "compound_main", search_limiter)
            if all_data_compound:
                window["-COMPOUND_INFO_SMILES-"].update(value=all_data_compound[0][1])
                window["-COMPOUND_INFO_PIC-"].update(data=all_data_compound[0][2])
                window["-COMPOUND_INFO_MP_VOLUME-"].update(value=all_data_compound[0][3])
                window["-COMPOUND_INFO_CONCENTRATION-"].update(value=all_data_compound[0][4])
                ac_id = all_data_compound[0][5]
                window["-COMPOUND_INFO_ORIGIN_ID-"].update(value=all_data_compound[0][6])
                search_limiter = {"academic_commercial": {"value": ac_id,
                                                          "operator": "=",
                                                          "target_column": "ac_id",
                                                          "use": True}}
                all_data_ac, _ = grab_table_data(config, "origin", search_limiter)
                window["-COMPOUND_INFO_AC-"].update(value=all_data_ac[0][1])
                window["-COMPOUND_INFO_ORIGIN-"].update(value=all_data_ac[0][2])

                compound_id = values["-COMPOUND_INFO_ID-"]
                table_data = update_plate_table(compound_id, config)
                window["-COMPOUND_INFO_PLATE_TABLE-"].update(values=table_data)

        #   WINDOW 2 - BIO INFO         ###
        if event == "-BIO_INFO_STATES-" and values["-BIO_INFO_STATES-"]:
            update_bio_info_values(values, window, plate_bio_info)
        if event == "-BIO_INFO_ANALYSE_METHOD-" and values["-BIO_INFO_STATES-"]:
            update_bio_info_values(values, window, plate_bio_info)
        if event == "-BIO_INFO_PLATES-" and values["-BIO_INFO_STATES-"]:
            update_bio_info_values(values, window, plate_bio_info)

        # Updating Sub setting data
        if event == "-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-":
            if values["-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HEATMAP_LOW_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-"])
        if event == "-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-":
            if values["-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HEATMAP_MID_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-"])
        if event == "-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-":
            if values["-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HEATMAP_HIGH_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-"])

        if event == "-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-":
            if values["-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HIT_MAP_LOW_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-"])
        if event == "-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-":
            if values["-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HIT_MAP_MID_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-"])
        if event == "-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-":
            if values["-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-"] != "None":
                window["-BIO_INFO_HIT_MAP_HIGH_COLOUR_BOX-"].\
                    update(background_color=values["-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-"])

        if event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_SUB_SETTINGS_TABS-"] == "Plate Overview" \
                and bio_info_sub_setting_tab_plate_overview_calc or event == "-BIO_INFO_PLATE_OVERVIEW_METHOD_LIST-" \
                or event == "-BIO_INFO_PLATE_OVERVIEW_STATE_LIST-" or event == "-BIO_INFO_PLATE_OVERVIEW_PLATE-":
            method = values["-BIO_INFO_PLATE_OVERVIEW_METHOD_LIST-"]
            state = values["-BIO_INFO_PLATE_OVERVIEW_STATE_LIST-"]
            plate = values["-BIO_INFO_PLATE_OVERVIEW_PLATE-"]
            sub_settings_plate_overview_table_data = sub_settings_plate_overview(plate_bio_info, method, plate, state)
            window["-BIO_INFO_OVERVIEW_TABLE-"].update(values=sub_settings_plate_overview_table_data)
            bio_info_sub_setting_tab_plate_overview_calc = False

        if event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_SUB_SETTINGS_TABS-"] == "Overview" \
                and bio_info_sub_setting_tab_overview_calc or event == "-BIO_INFO_OVERVIEW_METHOD-" \
                or event == "-BIO_INFO_OVERVIEW_STATE-":
            method = values["-BIO_INFO_OVERVIEW_METHOD-"]
            state = values["-BIO_INFO_OVERVIEW_STATE-"]
            sub_settings_overview_table_data = sub_settings_overview(plate_bio_info, method, state)
            table_overview_avg, table_overview_stdev, table_overview_z_prime = sub_settings_overview_table_data
            window["-BIO_INFO_OVERVIEW_AVG_TABLE-"].update(values=table_overview_avg)
            window["-BIO_INFO_OVERVIEW_STDEV_TABLE-"].update(values=table_overview_stdev)
            window["-BIO_INFO_OVERVIEW_Z_PRIME_TABLE-"].update(values=table_overview_z_prime)
            bio_info_sub_setting_tab_overview_calc = False

        # if event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_SUB_SETTINGS_TABS-"] == "List" \
        #         and bio_info_sub_setting_tab_list_calc or event == "-BIO_INFO_LIST_METHOD-" \
        #         or event == "-BIO_INFO_LIST_STATE-" or event == "-BIO_INFO_LIST_CALC-":
        #
        #     method = values["-BIO_INFO_LIST_METHOD-"]
        #     state = values["-BIO_INFO_LIST_STATE-"]
        #     calc = values["-BIO_INFO_LIST_CALC-"]
        #     sub_setting_list_table_data = sub_settings_list(plate_bio_info, method, state, calc)
        #     window["-BIO_INFO_LIST_TABLE-"].update(values=sub_setting_list_table_data)
        #     bio_info_sub_setting_tab_list_calc = False

        if event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_SUB_SETTINGS_TABS-"] == "Z-Prime" \
                and bio_info_sub_setting_tab_z_prime_calc:
            z_prime_data = sub_settings_z_prime(plate_bio_info)
            sub_settings_z_prime_table_data, z_prime_max_barcode, z_prime_max_value, z_prime_min_barcode, \
            z_prime_min_value = z_prime_data
            window["-BIO_INFO_Z_PRIME_LIST_TABLE-"].update(values=sub_settings_z_prime_table_data)
            window["-BIO_INFO_Z_PRIME_MAX_BARCODE-"].update(value=z_prime_max_barcode)
            window["-BIO_INFO_Z_PRIME_MAX_VALUE-"].update(value=z_prime_max_value)
            window["-BIO_INFO_Z_PRIME_MIN_BARCODE-"].update(value=z_prime_min_barcode)
            window["-BIO_INFO_Z_PRIME_MIN_VALUE-"].update(value=z_prime_min_value)

            bio_info_sub_setting_tab_z_prime_calc = False

        if event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_SUB_SETTINGS_TABS-"] == "Hit List" \
                and bio_info_sub_setting_tab_hit_list_calc:
            plate = values["-BIO_INFO_HIT_LIST_PLATES-"]
            method = values["-BIO_INFO_HIT_LIST_METHOD-"]
            state = values["-BIO_INFO_HIT_LIST_STATE-"]

            pora_thresholds = {
                "low": {"min": float(values["-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-"]),
                        "max": float(values["-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-"])},
                "mid": {"min": float(values["-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-"]),
                        "max": float(values["-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-"])},
                "high": {"min": float(values["-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-"]),
                         "max": float(values["-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-"])}
            }

            sub_settings_hit_list_table_data = sub_settings_hit_list(plate_bio_info, plate, method, state,
                                                                     bio_info_state_dict, pora_thresholds)

            hit_list_table_low, hit_list_table_mid, hit_list_table_high = sub_settings_hit_list_table_data
            window["-BIO_INFO_HIT_LIST_LOW_TABLE-"].update(values=hit_list_table_low)
            window["-BIO_INFO_HIT_LIST_MID_TABLE-"].update(values=hit_list_table_mid)
            window["-BIO_INFO_HIT_LIST_HIGH_TABLE-"].update(values=hit_list_table_high)

            bio_info_sub_setting_tab_hit_list_calc = False

        if event == "-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-" or event == "-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-" or \
                event == "-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-" or event == "-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-" or \
                event == "-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-" or event == "-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-":

            if not bio_info_sub_setting_tab_hit_list_calc:
                bio_info_sub_setting_tab_hit_list_calc = True

        if event == "-BIO_INFO_MAPPING-" or event == "-BIO_INFO_ANALYSE_METHOD-" or event == "-BIO_INFO_PLATES-" \
                or event == "-BIO_INFO_RE_DRAW-" \
                or event == "-BIO_INFO_SUB_SETTINGS_TABS-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                or event == "-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                or event == "-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                or event == "-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                or event == "-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                and values["-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-"] \
                or event == "-BIO_INFO_STATE_LIST_BOX-" and values["-BIO_INFO_MAPPING-"] == "Hit Map" \
                or event == "-BIO_INFO_STATE_LIST_BOX-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                or event == "-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                or event == "-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                or event == "-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                or event == "-BIO_INFO_HEAT_PERCENTILE_LOW-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                and values["-BIO_INFO_HEAT_PERCENTILE_LOW-"] \
                or event == "-BIO_INFO_HEAT_PERCENTILE_MID-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                and values["-BIO_INFO_HEAT_PERCENTILE_MID-"] \
                or event == "-BIO_INFO_HEAT_PERCENTILE_HIGH-" and values["-BIO_INFO_MAPPING-"] == "Heatmap" \
                and values["-BIO_INFO_HEAT_PERCENTILE_HIGH-"]:

            if plate_bio_info:
                if values["-BIO_INFO_MAPPING-"] == "State Mapping":
                    gui_tab = "bio_exp"
                    archive = True

                    well_dict_bio_info, bio_info_min_x, bio_info_min_y, bio_info_max_x, bio_info_max_y \
                        = draw_plate(config, graph_bio_exp, bio_info_plate_size, bio_info_state_dict, gui_tab, archive)

                if values["-BIO_INFO_MAPPING-"] == "Heatmap":
                    mapping = {
                        "mapping": values["-BIO_INFO_MAPPING-"],
                        "colours": {"low": [values["-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-"],
                                            values["-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-"]],
                                    "high": [values["-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-"],
                                             values["-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-"]]},
                        "states": values["-BIO_INFO_STATE_LIST_BOX-"],
                        "percentile": {"low": float(values["-BIO_INFO_HEAT_PERCENTILE_LOW-"]),
                                       "mid": float(values["-BIO_INFO_HEAT_PERCENTILE_MID-"]),
                                       "high": float(values["-BIO_INFO_HEAT_PERCENTILE_HIGH-"])}
                    }

                    gui_tab = "bio_exp"
                    plate = values["-BIO_INFO_PLATES-"]
                    analyse_method = values["-BIO_INFO_ANALYSE_METHOD-"]

                    temp_plate_bio_info = plate_bio_info[plate]["plates"][analyse_method]["wells"]
                    well_dict_bio_info, bio_info_min_x, bio_info_min_y, bio_info_max_x, bio_info_max_y \
                        = draw_plate(config, graph_bio_exp, bio_info_plate_size, temp_plate_bio_info, gui_tab,
                                     mapping=mapping, state_dict=bio_info_state_dict)

                if values["-BIO_INFO_MAPPING-"] == "Hit Map":
                    mapping = {
                        "mapping": values["-BIO_INFO_MAPPING-"],
                        "lower_bound_start": float(values["-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-"]),
                        "lower_bound_end": float(values["-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-"]),
                        "middle_bound_start": float(values["-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-"]),
                        "middle_bound_end": float(values["-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-"]),
                        "higher_bound_start": float(values["-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-"]),
                        "higher_bound_end": float(values["-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-"]),
                        "low_colour": values["-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-"],
                        "mid_colour": values["-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-"],
                        "high_colour": values["-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-"],
                        "states": values["-BIO_INFO_STATE_LIST_BOX-"]
                    }

                    plate = values["-BIO_INFO_PLATES-"]
                    analyse_method = values["-BIO_INFO_ANALYSE_METHOD-"]
                    gui_tab = "bio_exp"

                    temp_plate_bio_info = plate_bio_info[plate]["plates"][analyse_method]["wells"]
                    well_dict_bio_info, bio_info_min_x, bio_info_min_y, bio_info_max_x, bio_info_max_y \
                        = draw_plate(config, graph_bio_exp, bio_info_plate_size, temp_plate_bio_info, gui_tab,
                                     mapping=mapping, state_dict=bio_info_state_dict)

        if event == "-BIO_INFO_MATRIX_POPUP-" and plate_bio_info:
            method = values["-BIO_INFO_MATRIX_METHOD-"]
            state = values["-BIO_INFO_MATRIX_STATE-"]
            calc = values["-BIO_INFO_MATRIX_CALC-"]

            matrix_popup(plate_bio_info, calc_values, state_values, method_values, calc, state, method)

        if event == "-BIO_INFO_Z_PRIME_MATRIX_BUTTON-" and plate_bio_info:
            matrix_popup(plate_bio_info, calc_values, state_values, method_values, "z_prime")

        if event == "-BIO_INFO_MATRIX_BUTTON-" and plate_bio_info:
            data_dict = plate_bio_info
            state = values["-BIO_INFO_MATRIX_STATE-"]
            if state == "z_prime":
                calc = None
                method = None
            else:
                calc = values["-BIO_INFO_MATRIX_CALC-"]
                method = values["-BIO_INFO_MATRIX_METHOD-"]

            try:
                table_data, display_columns = sub_settings_matrix(data_dict, calc, method, state)
            except KeyError:
                sg.popup_error("Please select all information")
            else:
                window.Element("-BIO_INFO_MATRIX_TABLE-").Widget.configure(displaycolumns=display_columns)

                window["-BIO_INFO_MATRIX_TABLE-"].update(values=table_data)
            # window["-BIO_INFO_MATRIX_TABLE-"].update(headings=headings)

        if event == "-BIO_INFO_MOVE-":
            if values["-BIO_INFO_MOVE-"]:
                window["-RECT_BIO_MOVE-"].update(value=False)
            if not values["-BIO_INFO_MOVE-"]:
                window["-RECT_BIO_MOVE-"].update(value=True)

        if event == "-BIO_INFO_EXPORT-":
            sg.popup("This functions does nothing ATM ")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)

    # sg.main_get_debug_data()

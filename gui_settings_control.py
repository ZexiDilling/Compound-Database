import PySimpleGUI as sg
from config_writer import ConfigWriter

from bio_data_functions import org, norm, pora, pora_internal
from gui_settings_layout import GUISettingsLayout


class GUISettingsController:
    """

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    """

    def __init__(self, config, bio_final_report_setup, bio_plate_report_setup, ms_settings, simple_settings):
        self.final_setup_default = bio_final_report_setup
        self.plate_setup_default = bio_plate_report_setup
        self.ms_settings_default = ms_settings
        self.simple_settings = simple_settings
        self.cofig = config
        self.cw = ConfigWriter(config)
        self.gls = GUISettingsLayout(config)

    @staticmethod
    def _set_reports(values):
        bio_final_report_setup = {
            "methods": {"original": values["-FINAL_BIO_ORG-"],
                        "normalised": values["-FINAL_BIO_NORM-"],
                        "pora": values["-FINAL_BIO_PORA-"]},
            "analyse": {"sample": values["-FINAL_BIO_SAMPLE-"],
                        "minimum": values["-FINAL_BIO_MIN-"],
                        "max": values["-FINAL_BIO_MAX-"],
                        "empty": values["-FINAL_BIO_EMPTY-"],
                        "negative": values["-FINAL_BIO_NEG_C-"],
                        "positive": values["-FINAL_BIO_POS_C-"],
                        "blank": values["-FINAL_BIO_BLANK-"]},
            "calc": {
                "original": {"overview": values["-FINAL_BIO_CAL_ORG-"],
                             "sample": values["-FINAL_BIO_CALC_ORG_SAMPLE-"],
                             "minimum": values["-FINAL_BIO_CALC_ORG_MIN-"],
                             "max": values["-FINAL_BIO_CALC_ORG_MAX-"],
                             "empty": values["-FINAL_BIO_CALC_ORG_EMPTY-"],
                             "negative": values["-FINAL_BIO_CALC_ORG_NEG_C-"],
                             "positive": values["-FINAL_BIO_CALC_ORG_POS_C-"],
                             "blank": values["-FINAL_BIO_CALC_ORG_BLANK-"]},
                "normalised": {"overview": values["-FINAL_BIO_CAL_NORM-"],
                               "sample": values["-FINAL_BIO_CALC_NORM_SAMPLE-"],
                               "minimum": values["-FINAL_BIO_CALC_NORM_MIN-"],
                               "max": values["-FINAL_BIO_CALC_NORM_MAX-"],
                               "empty": values["-FINAL_BIO_CALC_NORM_EMPTY-"],
                               "negative": values["-FINAL_BIO_CALC_NORM_NEG_C-"],
                               "positive": values["-FINAL_BIO_CALC_NORM_POS_C-"],
                               "blank": values["-FINAL_BIO_CALC_NORM_BLANK-"]},
                "pora": {"overview": values["-FINAL_BIO_CAL_PORA-"],
                         "sample": values["-FINAL_BIO_CALC_PORA_SAMPLE-"],
                         "minimum": values["-FINAL_BIO_CALC_PORA_MIN-"],
                         "max": values["-FINAL_BIO_CALC_PORA_MAX-"],
                         "empty": values["-FINAL_BIO_CALC_PORA_EMPTY-"],
                         "negative": values["-FINAL_BIO_CALC_PORA_NEG_C-"],
                         "positive": values["-FINAL_BIO_CALC_PORA_POS_C-"],
                         "blank": values["-FINAL_BIO_CALC_PORA_BLANK-"]},
                "z_prime": values["-FINAL_BIO_Z_PRIME-"]},
            "pora_threshold": {"low": {"min": values["-PORA_LOW_MIN_HIT_THRESHOLD-"],
                                       "max": values["-PORA_LOW_MAX_HIT_THRESHOLD-"]},
                               "mid": {"min": values["-PORA_MID_MIN_HIT_THRESHOLD-"],
                                       "max": values["-PORA_MID_MAX_HIT_THRESHOLD-"]},
                               "high": {"min": values["-PORA_HIGH_MIN_HIT_THRESHOLD-"],
                                        "max": values["-PORA_HIGH_MAX_HIT_THRESHOLD-"]}},
            "data": {"sample": {"matrix": values["-FINAL_REPORT_MATRIX_SAMPLE-"],
                                "list": values["-FINAL_REPORT_LIST_SAMPLE-"],
                                "max_min": values["-FINAL_REPORT_MAX_MIN_SAMPLE-"]},
                     "minimum": {"matrix": values["-FINAL_REPORT_MATRIX_MINIMUM-"],
                                 "list": values["-FINAL_REPORT_LIST_MINIMUM-"],
                                 "max_min": values["-FINAL_REPORT_MAX_MIN_MINIMUM-"]},
                     "max": {"matrix": values["-FINAL_REPORT_MATRIX_MAXIMUM-"],
                             "list": values["-FINAL_REPORT_LIST_MAXIMUM-"],
                             "max_min": values["-FINAL_REPORT_MAX_MIN_MAXIMUM-"]},
                     "empty": {"matrix": values["-FINAL_REPORT_MATRIX_EMPTY-"],
                               "list": values["-FINAL_REPORT_LIST_EMPTY-"],
                               "max_min": values["-FINAL_REPORT_MAX_MIN_EMPTY-"]},
                     "negative": {"matrix": values["-FINAL_REPORT_MATRIX_NEGATIVE-"],
                                  "list": values["-FINAL_REPORT_LIST_NEGATIVE-"],
                                  "max_min": values["-FINAL_REPORT_MAX_MIN_NEGATIVE-"]},
                     "positive": {"matrix": values["-FINAL_REPORT_MATRIX_POSITIVE-"],
                                  "list": values["-FINAL_REPORT_LIST_POSITIVE-"],
                                  "max_min": values["-FINAL_REPORT_MAX_MIN_POSITIVE-"]},
                     "blank": {"matrix": values["-FINAL_REPORT_MATRIX_BLANK-"],
                               "list": values["-FINAL_REPORT_LIST_BLANK-"],
                               "max_min": values["-FINAL_REPORT_MAX_MIN_BLANK-"]},
                     "z_prime": {"matrix": values["-FINAL_REPORT_MATRIX_Z_PRIME-"],
                                 "list": values["-FINAL_REPORT_LIST_Z_PRIME-"],
                                 "max_min": values["-FINAL_REPORT_MAX_MIN_Z_PRIME-"]}},

        }
        bio_plate_report_setup = {
            "well_states_report_method": {"original": values["-BIO_PLATE_REPORT_ORG-"],
                                          "normalised": values["-BIO_PLATE_REPORT_NORM-"],
                                          "pora": values["-BIO_PLATE_REPORT_PORA-"],
                                          # "pora_internal": values["-BIO_PLATE_REPORT_PORA_INTERNAL-"]
                                          },

            "well_states_report": {"sample": values["-BIO_SAMPLE-"], "minimum": values["-BIO_MIN-"],
                                   "max": values["-BIO_MAX-"], "empty": values["-BIO_EMPTY-"],
                                   "negative": values["-BIO_NEG_C-"], "positive": values["-BIO_POS_C-"],
                                   "blank": values["-BIO_BLANK-"]},
            "calc_dict":
                {"original": {"use": values["-BIO_REPORT_SHEET_ORG_CALC-"],
                              "avg": values["-BIO_REPORT_CAL_ORG_AVG-"],
                              "stdev": values["-BIO_REPORT_CAL_ORG_STDEV-"],
                              "state": {"sample": values["-BIO_REPORT_CAL_ORG_SAMPLE-"],
                                        "minimum": values["-BIO_REPORT_CAL_ORG_MIN-"],
                                        "max": values["-BIO_REPORT_CAL_ORG_MAX-"],
                                        "empty": values["-BIO_REPORT_CAL_ORG_EMPTY-"],
                                        "negative": values["-BIO_REPORT_CAL_ORG_NEG_C-"],
                                        "positive": values["-BIO_REPORT_CAL_ORG_POS_C-"],
                                        "blank": values["-BIO_REPORT_CAL_ORG_BLANK-"]}},
                 "normalised": {"use": values["-BIO_REPORT_SHEET_NORM_CALC-"],
                                "avg": values["-BIO_REPORT_CAL_NORM_AVG-"],
                                "stdev": values["-BIO_REPORT_CAL_NORM_STDEV-"],
                                "state": {"sample": values["-BIO_REPORT_CAL_NORM_SAMPLE-"],
                                          "minimum": values["-BIO_REPORT_CAL_NORM_MIN-"],
                                          "max": values["-BIO_REPORT_CAL_NORM_MAX-"],
                                          "empty": values["-BIO_REPORT_CAL_NORM_EMPTY-"],
                                          "negative": values["-BIO_REPORT_CAL_NORM_NEG_C-"],
                                          "positive": values["-BIO_REPORT_CAL_NORM_POS_C-"],
                                          "blank": values["-BIO_REPORT_CAL_NORM_BLANK-"]}},
                 "pora": {"use": values["-BIO_REPORT_SHEET_PORA_CAL-"],
                          "avg": values["-BIO_REPORT_CAL_PORA_AVG-"],
                          "stdev": values["-BIO_REPORT_CAL_PORA_STDEV-"],
                          "state": {"sample": values["-BIO_REPORT_CAL_PORA_SAMPLE-"],
                                    "minimum": values["-BIO_REPORT_CAL_PORA_MIN-"],
                                    "max": values["-BIO_REPORT_CAL_PORA_MAX-"],
                                    "empty": values["-BIO_REPORT_CAL_PORA_EMPTY-"],
                                    "negative": values["-BIO_REPORT_CAL_PORA_NEG_C-"],
                                    "positive": values["-BIO_REPORT_CAL_PORA_POS_C-"],
                                    "blank": values["-BIO_REPORT_CAL_PORA_BLANK-"]}},
                 # "pora_internal": {"use": values["-BIO_REPORT_SHEET_PORA_INTERNAL_CAL-"],
                 #                   "avg": values["-BIO_REPORT_CAL_PORA_INT_AVG-"],
                 #                   "stdev": values["-BIO_REPORT_CAL_PORA_INT_STDEV-"],
                 #                   "state": {"sample": values["-BIO_REPORT_CAL_PORA_INT_SAMPLE-"],
                 #                             "minimum": values["-BIO_REPORT_CAL_PORA_INT_MIN-"],
                 #                             "max": values["-BIO_REPORT_CAL_PORA_INT_MAX-"],
                 #                             "empty": values["-BIO_REPORT_CAL_PORA_INT_EMPTY-"],
                 #                             "negative": values["-BIO_REPORT_CAL_PORA_INT_NEG_C-"],
                 #                             "positive": values["-BIO_REPORT_CAL_PORA_INT_POS_C-"],
                 #                             "blank": values["-BIO_REPORT_CAL_PORA_INT_BLANK-"]}},
                 "other": {"use": values["-BIO_REPORT_SHEET_OTHER-"],
                           "calc": {"z_prime": values["-BIO_REPORT_SHEET_Z_PRIME-"]}}},
            "plate_calc_dict": {
                "original": {"use": values["-BIO_PLATE_REPORT_ORG_CALC-"],
                             "avg": values["-BIO_PLATE_CAL_ORG_AVG-"],
                             "stdev": values["-BIO_PLATE_CAL_ORG_STDEV-"],
                             "state": {"sample": values["-BIO_CAL_ORG_SAMPLE-"],
                                       "minimum": values["-BIO_CAL_ORG_MIN-"],
                                       "max": values["-BIO_CAL_ORG_MAX-"],
                                       "empty": values["-BIO_CAL_ORG_EMPTY-"],
                                       "negative": values["-BIO_CAL_ORG_NEG_C-"],
                                       "positive": values["-BIO_CAL_ORG_POS_C-"],
                                       "blank": values["-BIO_CAL_ORG_BLANK-"]}},
                "normalised": {"use": values["-BIO_PLATE_REPORT_NORM_CALC-"],
                               "avg": values["-BIO_PLATE_CAL_NORM_AVG-"],
                               "stdev": values["-BIO_PLATE_CAL_NORM_STDEV-"],
                               "state": {"sample": values["-BIO_CAL_NORM_SAMPLE-"],
                                         "minimum": values["-BIO_CAL_NORM_MIN-"],
                                         "max": values["-BIO_CAL_NORM_MAX-"],
                                         "empty": values["-BIO_CAL_NORM_EMPTY-"],
                                         "negative": values["-BIO_CAL_NORM_NEG_C-"],
                                         "positive": values["-BIO_CAL_NORM_POS_C-"],
                                         "blank": values["-BIO_CAL_NORM_BLANK-"]}},
                "pora": {"use": values["-BIO_PLATE_REPORT_PORA_CAL-"],
                         "avg": values["-BIO_PLATE_CAL_PORA_AVG-"],
                         "stdev": values["-BIO_PLATE_CAL_PORA_STDEV-"],
                         "state": {"sample": values["-BIO_CAL_PORA_SAMPLE-"],
                                   "minimum": values["-BIO_CAL_PORA_MIN-"],
                                   "max": values["-BIO_CAL_PORA_MAX-"],
                                   "empty": values["-BIO_CAL_PORA_EMPTY-"],
                                   "negative": values["-BIO_CAL_PORA_NEG_C-"],
                                   "positive": values["-BIO_CAL_PORA_POS_C-"],
                                   "blank": values["-BIO_CAL_PORA_BLANK-"]}},
                # "pora_internal": {"use": values["-BIO_PLATE_REPORT_PORA_INTERNAL_CAL-"],
                #                   "avg": values["-BIO_PLATE_CAL_PORA_INT_AVG-"],
                #                   "stdev": values["-BIO_PLATE_CAL_PORA_INT_STDEV-"],
                #                   "state": {"sample": values["-BIO_CAL_PORA_INT_SAMPLE-"],
                #                             "minimum": values["-BIO_CAL_PORA_INT_MIN-"],
                #                             "max": values["-BIO_CAL_PORA_INT_MAX-"],
                #                             "empty": values["-BIO_CAL_PORA_INT_EMPTY-"],
                #                             "negative": values["-BIO_CAL_PORA_INT_NEG_C-"],
                #                             "positive": values["-BIO_CAL_PORA_INT_POS_C-"],
                #                             "blank": values["-BIO_CAL_PORA_INT_BLANK-"]}}
            },
            "plate_analysis_dict": {"original": {
                # "use": values["-SINGLE_ORG_USE-"],
                                    "use": True, "methode": org,
                                    "state_map": values["-SINGLE_ORG_STATE-"],
                                    "heatmap": values["-SINGLE_ORG_HEAT-"],
                                    "hit_map": False,
                                    "none": values["-SINGLE_ORG_NONE-"]},
                                    "normalised": {
                                        # "use": values["-SINGLE_NORM_USE-"],
                                    "use": True, "methode": norm,
                                    "state_map": values["-SINGLE_norm_STATE-"],
                                    "heatmap": values["-SINGLE_norm_HEAT-"],
                                    "hit_map": False,
                                    "none": values["-SINGLE_norm_NONE-"]},
                                    "pora": {
                                        # "use": values["-SINGLE_PORA_USE-"],
                                    "use": True, "methode": pora,
                                    "state_map": values["-SINGLE_PORA_STATE-"],
                                    "heatmap": values["-SINGLE_PORA_HEAT-"],
                                    "hit_map": values["-SINGLE_PORA_HIT-"],
                                    "none": values["-SINGLE_PORA_NONE-"]},
                                    # "pora_internal": {"used": values["-SINGLE_PORA_INTERNAL_USE-"],
                                    #                   "methode": pora_internal,
                                    #                   "state_mapping": values["-SINGLE_PORA_INTERNAL_STATE-"],
                                    #                   "heatmap": values["-SINGLE_PORA_INTERNAL_HEAT-"],
                                    #                   "Hit_Mapping": values["-SINGLE_PORA_INTERNAL_HIT-"]}

                                    },
            "z_prime_calc": values["-BIO_Z_PRIME-"],
            "heatmap_colours": {"low": values["-PLATE_REPORT_HEATMAP_LOW_COLOUR_TARGET-"],
                                "mid": values["-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-"],
                                "high": values["-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-"]},
            "pora_threshold": {"low": {"min": values["-PLATE_PORA_LOW_MIN_HIT_THRESHOLD-"],
                                       "max": values["-PLATE_PORA_LOW_MAX_HIT_THRESHOLD-"]},
                               "mid": {"min": values["-PLATE_PORA_MID_MIN_HIT_THRESHOLD-"],
                                       "max": values["-PLATE_PORA_MID_MAX_HIT_THRESHOLD-"]},
                               "high": {"min": values["-PLATE_PORA_HIGH_MIN_HIT_THRESHOLD-"],
                                        "max": values["-PLATE_PORA_HIGH_MAX_HIT_THRESHOLD-"]},
                               "colour": {"low": values["-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-"],
                                          "mid": values["-PLATE_REPORT_HIT_MID_COLOUR_TARGET-"],
                                          "high": values["-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-"]}}
        }
        ms_settings = {
            "ions": {"positive": {
                "m+3h": values["-MS_POS_ION_m+3h-"],
                "m+2h+na": values["-MS_POS_ION_m+2h+na-"],
                "m+h+2na": values["-MS_POS_ION_m+h+2na-"],
                "m+3na": values["-MS_POS_ION_m+3na-"],
                "m+2h": values["-MS_POS_ION_m+2h-"],
                "m+h+nh4": values["-MS_POS_ION_m+h+nh4-"],
                "m+h+na": values["-MS_POS_ION_m+h+na-"],
                "m+h+k": values["-MS_POS_ION_m+h+k-"],
                "m+acn+2h": values["-MS_POS_ION_m+acn+2h-"],
                "m+2na": values["-MS_POS_ION_m+2na-"],
                "m+2acn+2h": values["-MS_POS_ION_m+2acn+2h-"],
                "m+3acn+2h": values["-MS_POS_ION_m+3acn+2h-"],
                "m+h": values["-MS_POS_ION_m+h-"],
                "m+nh4": values["-MS_POS_ION_m+nh4-"],
                "m+na": values["-MS_POS_ION_m+na-"],
                "m+ch3oh+h": values["-MS_POS_ION_m+ch3oh+h-"],
                "m+k": values["-MS_POS_ION_m+k-"],
                "m+acn+h": values["-MS_POS_ION_m+acn+h-"],
                "m+2na-h": values["-MS_POS_ION_m+2na-h-"],
                "m+isoprop+h": values["-MS_POS_ION_m+isoprop+h-"],
                "m+acn+na": values["-MS_POS_ION_m+acn+na-"],
                "m+2k+h": values["-MS_POS_ION_m+2k+h-"],
                "m+dmso+h": values["-MS_POS_ION_m+dmso+h-"],
                "m+2acn+h": values["-MS_POS_ION_m+2acn+h-"],
                "m+isoprop+na+h": values["-MS_POS_ION_m+isoprop+na+h-"],
                "2m+h": values["-MS_POS_ION_2m+h-"],
                "2m+nh4": values["-MS_POS_ION_2m+nh4-"],
                "2m+na": values["-MS_POS_ION_2m+na-"],
                "2m+3h2o+2h": values["-MS_POS_ION_2m+3h2o+2h-"],
                "2m+k": values["-MS_POS_ION_2m+k-"],
                "2m+acn+h": values["-MS_POS_ION_2m+acn+h-"],
                "2m+acn+na": values["-MS_POS_ION_2m+acn+na-"]
            },
                "negative": {
                    "m-3h": values["-MS_NEG_ION_m-3h-"],
                    "m-2h": values["-MS_NEG_ION_m-2h-"],
                    "m-h2o-h": values["-MS_NEG_ION_m-h2o-h-"],
                    "m-h": values["-MS_NEG_ION_m-h-"],
                    "m+na-2h": values["-MS_NEG_ION_m+na-2h-"],
                    "m+cl": values["-MS_NEG_ION_m+cl-"],
                    "m+k-2h": values["-MS_NEG_ION_m+k-2h-"],
                    "m+fa-h": values["-MS_NEG_ION_m+fa-h-"],
                    "m+hac-h": values["-MS_NEG_ION_m+hac-h-"],
                    "m+br": values["-MS_NEG_ION_m+br-"],
                    "m+tfa-h": values["-MS_NEG_ION_m+tfa-h-"],
                    "2m-h": values["-MS_NEG_ION_m+tfa-h-"],
                    "2m+fa-h": values["-MS_NEG_ION_2m-h-"],
                    "2m+hac-h": values["-MS_NEG_ION_2m+fa-h-"],
                    "3m-h": values["-MS_NEG_ION_2m+hac-h-"]
                }
            }
        }
        simple_settings = {
            "plate_colouring": {
                "sample": values["-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-"],
                "blank": values["-PLATE_LAYOUT_COLOUR_BLANK_TARGET-"],
                "max": values["-PLATE_LAYOUT_COLOUR_MAX_TARGET-"],
                "minimum": values["-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-"],
                "positive": values["-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-"],
                "negative": values["-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-"],
                "empty": values["-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-"]
            }
        }
        reports = bio_final_report_setup, bio_plate_report_setup, ms_settings, simple_settings
        return reports

    def main_settings_controller(self, bio_final_report_setup, bio_plate_report_setup, ms_settings):
        """
        The control modul for the settings menu - for now only bio data
        :return: The data selected from the window
        """
        default_sat = False

        window = self.gls.settings_window(bio_final_report_setup, bio_plate_report_setup, ms_settings)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "-CANCEL-" and not default_sat:
                break
                window.close()
            if event == "-CANCEL-" and default_sat:
                return reports
                break
            if event == "-TAB_GROUPS-":
                if values["-TAB_GROUPS-"] == "Bio Plate Report":
                    report_name = "bio_plate_report"
                    report_counter = 1
                elif values["-TAB_GROUPS-"] == "Bio Final Report":
                    report_name = "bio_full_report"
                    report_counter = 0
                elif values["-TAB_GROUPS-"] == "MS Ions":
                    report_name = "ms_ions_settings"
                    report_counter = 2
                elif values["-TAB_GROUPS-"] == "Plate Layout":
                    report_name = "simple_settings"
                    report_counter = 3

            if event == "-BIO_SETTINGS_OK-":
                reports = self._set_reports(values)

                window.close()
                return reports

            if event == "-SETTINGS_DEFAULT-":
                reports = self._set_reports(values)
                self.cw.run(reports[report_counter], report_name)
                self.final_setup_default, self.plate_setup_default, self.ms_settings_default, self.simple_settings \
                    = reports
                sg.popup(f"New default values for {report_name}")
                default_sat = True

            if event == "-SETTINGS_LOAD_DEFAULT-":
                window.close()
                window = self.gls.settings_window(self.final_setup_default, self.plate_setup_default)
                # window.Refresh()

            # BIO PLATE REPORT - SINGLE POINT
            if event == "-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HIT_LOW_COLOUR-"].\
                        update(button_color=values["-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-"])
            if event == "-PLATE_REPORT_HIT_MID_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HIT_MID_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HIT_MID_COLOUR-"].\
                        update(button_color=values["-PLATE_REPORT_HIT_MID_COLOUR_TARGET-"])
            if event == "-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HIT_HIGH_COLOUR-"].\
                        update(button_color=values["-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-"])

            if event == "-PLATE_REPORT_HEATMAP_LOW_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HEATMAP_LOW_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HEATMAP_LOW_COLOUR-"].\
                           update(button_color=values["-PLATE_REP  ORT_HEATMAP_LOW_COLOUR_TARGET-"])
            if event == "-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HEATMAP_MID_COLOUR-"].\
                           update(button_color=values["-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-"])
            if event == "-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-":
                if values["-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-"] != "None":
                    window["-PLATE_REPORT_HEATMAP_HIGH_COLOUR-"].\
                           update(button_color=values["-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-"])

            # PLATE LAYOUT - COLOURS #

            if event == "-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_SAMPLE_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_BLANK_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_BLANK_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_BLANK_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_BLANK_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_MAX_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_MAX_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_MAX_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_MAX_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_MINIMUM_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_POSITIVE_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_NEGATIVE_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-"])
            if event == "-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-":
                if values["-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-"] != "None":
                    window["-PLATE_LAYOUT_COLOUR_EMPTY_BOX-"].\
                        update(background_color=values["-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-"])

            # CHECK MARKS THAT AFFECT OTHER STUFF!!!

            # BIO Final Report - Calculations:
            if event == "-FINAL_BIO_CAL_ORG-":
                if not values["-FINAL_BIO_CAL_ORG-"]:
                    window["-FINAL_BIO_CALC_ORG_SAMPLE-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_MIN-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_MAX-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_EMPTY-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_NEG_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_POS_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_ORG_BLANK-"].update(disabled=True)
                else:
                    window["-FINAL_BIO_CALC_ORG_SAMPLE-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_MIN-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_MAX-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_EMPTY-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_NEG_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_POS_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_ORG_BLANK-"].update(disabled=False)
            if event == "-FINAL_BIO_CAL_NORM-":
                if not values["-FINAL_BIO_CAL_NORM-"]:
                    window["-FINAL_BIO_CALC_NORM_SAMPLE-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_MIN-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_MAX-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_EMPTY-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_NEG_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_POS_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_NORM_BLANK-"].update(disabled=True)
                else:
                    window["-FINAL_BIO_CALC_NORM_SAMPLE-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_MIN-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_MAX-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_EMPTY-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_NEG_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_POS_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_NORM_BLANK-"].update(disabled=False)
            if event == "-FINAL_BIO_CAL_PORA-":
                if not values["-FINAL_BIO_CAL_PORA-"]:
                    window["-FINAL_BIO_CALC_PORA_SAMPLE-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_MIN-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_MAX-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_EMPTY-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_NEG_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_POS_C-"].update(disabled=True)
                    window["-FINAL_BIO_CALC_PORA_BLANK-"].update(disabled=True)
                else:
                    window["-FINAL_BIO_CALC_PORA_SAMPLE-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_MIN-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_MAX-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_EMPTY-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_NEG_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_POS_C-"].update(disabled=False)
                    window["-FINAL_BIO_CALC_PORA_BLANK-"].update(disabled=False)

            # BIO Final Report - list and max_min for matr
            if event == "-FINAL_REPORT_MATRIX_SAMPLE-":
                if not values["-FINAL_REPORT_MATRIX_SAMPLE-"]:
                    window["-FINAL_REPORT_LIST_SAMPLE-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_SAMPLE-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_SAMPLE-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_SAMPLE-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_MINIMUM-":
                if not values["-FINAL_REPORT_MATRIX_MINIMUM-"]:
                    window["-FINAL_REPORT_LIST_MINIMUM-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_MINIMUM-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_MINIMUM-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_MINIMUM-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_MAXIMUM-":
                if not values["-FINAL_REPORT_MATRIX_MAXIMUM-"]:
                    window["-FINAL_REPORT_LIST_MAXIMUM-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_MAXIMUM-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_MAXIMUM-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_MAXIMUM-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_EMPTY-":
                if not values["-FINAL_REPORT_MATRIX_EMPTY-"]:
                    window["-FINAL_REPORT_LIST_EMPTY-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_EMPTY-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_EMPTY-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_EMPTY-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_NEGATIVE-":
                if not values["-FINAL_REPORT_MATRIX_NEGATIVE-"]:
                    window["-FINAL_REPORT_LIST_NEGATIVE-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_NEGATIVE-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_NEGATIVE-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_NEGATIVE-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_POSITIVE-":
                if not values["-FINAL_REPORT_MATRIX_POSITIVE-"]:
                    window["-FINAL_REPORT_LIST_POSITIVE-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_POSITIVE-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_POSITIVE-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_POSITIVE-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_BLANK-":
                if not values["-FINAL_REPORT_MATRIX_BLANK-"]:
                    window["-FINAL_REPORT_LIST_BLANK-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_BLANK-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_BLANK-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_BLANK-"].update(disabled=False)
            if event == "-FINAL_REPORT_MATRIX_Z_PRIME-":
                if not values["-FINAL_REPORT_MATRIX_Z_PRIME-"]:
                    window["-FINAL_REPORT_LIST_Z_PRIME-"].update(disabled=True)
                    window["-FINAL_REPORT_MAX_MIN_Z_PRIME-"].update(disabled=True)
                else:
                    window["-FINAL_REPORT_LIST_Z_PRIME-"].update(disabled=False)
                    window["-FINAL_REPORT_MAX_MIN_Z_PRIME-"].update(disabled=False)

            # BIO Plate Report - Analysis sheet
            if event == "-BIO_PLATE_REPORT_ORG_CALC-":
                if not values["-BIO_PLATE_REPORT_ORG_CALC-"]:
                    window["-BIO_PLATE_CAL_ORG_AVG-"].update(disabled=True)
                    window["-BIO_PLATE_CAL_ORG_STDEV-"].update(disabled=True)
                    window["-BIO_CAL_ORG_SAMPLE-"].update(disabled=True)
                    window["-BIO_CAL_ORG_MIN-"].update(disabled=True)
                    window["-BIO_CAL_ORG_MAX-"].update(disabled=True)
                    window["-BIO_CAL_ORG_EMPTY-"].update(disabled=True)
                    window["-BIO_CAL_ORG_NEG_C-"].update(disabled=True)
                    window["-BIO_CAL_ORG_POS_C-"].update(disabled=True)
                    window["-BIO_CAL_ORG_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_PLATE_CAL_ORG_AVG-"].update(disabled=False)
                    window["-BIO_PLATE_CAL_ORG_STDEV-"].update(disabled=False)
                    window["-BIO_CAL_ORG_SAMPLE-"].update(disabled=False)
                    window["-BIO_CAL_ORG_MIN-"].update(disabled=False)
                    window["-BIO_CAL_ORG_MAX-"].update(disabled=False)
                    window["-BIO_CAL_ORG_EMPTY-"].update(disabled=False)
                    window["-BIO_CAL_ORG_NEG_C-"].update(disabled=False)
                    window["-BIO_CAL_ORG_POS_C-"].update(disabled=False)
                    window["-BIO_CAL_ORG_BLANK-"].update(disabled=False)
            if event == "-BIO_PLATE_REPORT_NORM_CALC-":
                if not values["-BIO_PLATE_REPORT_NORM_CALC-"]:
                    window["-BIO_PLATE_CAL_NORM_AVG-"].update(disabled=True)
                    window["-BIO_PLATE_CAL_NORM_STDEV-"].update(disabled=True)
                    window["-BIO_CAL_NORM_SAMPLE-"].update(disabled=True)
                    window["-BIO_CAL_NORM_MIN-"].update(disabled=True)
                    window["-BIO_CAL_NORM_MAX-"].update(disabled=True)
                    window["-BIO_CAL_NORM_EMPTY-"].update(disabled=True)
                    window["-BIO_CAL_NORM_NEG_C-"].update(disabled=True)
                    window["-BIO_CAL_NORM_POS_C-"].update(disabled=True)
                    window["-BIO_CAL_NORM_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_PLATE_CAL_NORM_AVG-"].update(disabled=False)
                    window["-BIO_PLATE_CAL_NORM_STDEV-"].update(disabled=False)
                    window["-BIO_CAL_NORM_SAMPLE-"].update(disabled=False)
                    window["-BIO_CAL_NORM_MIN-"].update(disabled=False)
                    window["-BIO_CAL_NORM_MAX-"].update(disabled=False)
                    window["-BIO_CAL_NORM_EMPTY-"].update(disabled=False)
                    window["-BIO_CAL_NORM_NEG_C-"].update(disabled=False)
                    window["-BIO_CAL_NORM_POS_C-"].update(disabled=False)
                    window["-BIO_CAL_NORM_BLANK-"].update(disabled=False)
            if event == "-BIO_PLATE_REPORT_PORA_CAL-":
                if not values["-BIO_PLATE_REPORT_PORA_CAL-"]:
                    window["-BIO_PLATE_CAL_PORA_AVG-"].update(disabled=True)
                    window["-BIO_PLATE_CAL_PORA_STDEV-"].update(disabled=True)
                    window["-BIO_CAL_PORA_SAMPLE-"].update(disabled=True)
                    window["-BIO_CAL_PORA_MIN-"].update(disabled=True)
                    window["-BIO_CAL_PORA_MAX-"].update(disabled=True)
                    window["-BIO_CAL_PORA_EMPTY-"].update(disabled=True)
                    window["-BIO_CAL_PORA_NEG_C-"].update(disabled=True)
                    window["-BIO_CAL_PORA_POS_C-"].update(disabled=True)
                    window["-BIO_CAL_PORA_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_PLATE_CAL_PORA_AVG-"].update(disabled=False)
                    window["-BIO_PLATE_CAL_PORA_STDEV-"].update(disabled=False)
                    window["-BIO_CAL_PORA_SAMPLE-"].update(disabled=False)
                    window["-BIO_CAL_PORA_MIN-"].update(disabled=False)
                    window["-BIO_CAL_PORA_MAX-"].update(disabled=False)
                    window["-BIO_CAL_PORA_EMPTY-"].update(disabled=False)
                    window["-BIO_CAL_PORA_NEG_C-"].update(disabled=False)
                    window["-BIO_CAL_PORA_POS_C-"].update(disabled=False)
                    window["-BIO_CAL_PORA_BLANK-"].update(disabled=False)

            # BIO Plate Report - Final report for the plate:
            if event == "-BIO_REPORT_SHEET_ORG_CALC-":
                if not values["-BIO_REPORT_SHEET_ORG_CALC-"]:
                    window["-BIO_REPORT_CAL_ORG_AVG-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_STDEV-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_SAMPLE-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_MIN-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_MAX-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_EMPTY-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_NEG_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_POS_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_ORG_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_REPORT_CAL_ORG_AVG-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_STDEV-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_SAMPLE-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_MIN-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_MAX-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_EMPTY-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_NEG_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_POS_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_ORG_BLANK-"].update(disabled=False)
            if event == "-BIO_REPORT_SHEET_NORM_CALC-":
                if not values["-BIO_REPORT_SHEET_NORM_CALC-"]:
                    window["-BIO_REPORT_CAL_NORM_AVG-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_STDEV-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_SAMPLE-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_MIN-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_MAX-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_EMPTY-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_NEG_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_POS_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_NORM_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_REPORT_CAL_NORM_AVG-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_STDEV-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_SAMPLE-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_MIN-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_MAX-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_EMPTY-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_NEG_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_POS_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_NORM_BLANK-"].update(disabled=False)
            if event == "-BIO_REPORT_SHEET_PORA_CAL-":
                if not values["-BIO_REPORT_SHEET_PORA_CAL-"]:
                    window["-BIO_REPORT_CAL_PORA_AVG-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_STDEV-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_SAMPLE-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_MIN-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_MAX-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_EMPTY-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_NEG_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_POS_C-"].update(disabled=True)
                    window["-BIO_REPORT_CAL_PORA_BLANK-"].update(disabled=True)
                else:
                    window["-BIO_REPORT_CAL_PORA_AVG-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_STDEV-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_SAMPLE-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_MIN-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_MAX-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_EMPTY-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_NEG_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_POS_C-"].update(disabled=False)
                    window["-BIO_REPORT_CAL_PORA_BLANK-"].update(disabled=False)

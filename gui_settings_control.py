from gui_settings import GUISettingsLayout
import PySimpleGUI as sg
from bio_data_functions import  org, norm, pora, pora_internal


class GUISettingsController:
    def __init__(self, config):
        self.cofig = config
        self.gls = GUISettingsLayout(config)

    def main_settings_controller(self):
        window_bio = self.gls.bio_settings_window()

        while True:
            event, values = window_bio.read()
            if event == sg.WIN_CLOSED or event == "-CANCEL-":
                break
            if event == "-BIO_SETTINGS_DEFAULT-":
                sg.popup("Is not working atm, sorry")
            if event == "-BIO_SETTINGS_OK-":

                bio_final_report_setup = {
                    "methods": {"original": values["-FINAL_BIO_ORG-"],
                                "normalised": values["-FINAL_BIO_NORM-"],
                                "pora": values["-FINAL_BIO_PORA-"]},
                    "analyse": {"sample": values["-FINAL_BIO_SAMPLE-"],
                                "minimum": values["-FINAL_BIO_MIN-"],
                                "max": values["-FINAL_BIO_MAX-"],
                                "empty": values["-FINAL_BIO_EMPTY-"],
                                "negative control": values["-FINAL_BIO_NEG_C-"],
                                "positive control": values["-FINAL_BIO_POS_C-"],
                                "blank": values["-FINAL_BIO_BLANK-"]},
                    "calc": {
                        "original": {"overview": values["-FINAL_BIO_CAL_ORG-"],
                                     "sample": values["-FINAL_BIO_CALC_ORG_SAMPLE-"],
                                     "minimum": values["-FINAL_BIO_CALC_ORG_MIN-"],
                                     "max": values["-FINAL_BIO_CALC_ORG_MAX-"],
                                     "empty": values["-FINAL_BIO_CALC_ORG_EMPTY-"],
                                     "negative control": values["-FINAL_BIO_CALC_ORG_NEG_C-"],
                                     "positive control": values["-FINAL_BIO_CALC_ORG_POS_C-"],
                                     "blank": values["-FINAL_BIO_CALC_ORG_BLANK-"]},
                        "normalised": {"overview": values["-FINAL_BIO_CAL_NORM-"],
                                       "sample": values["-FINAL_BIO_CALC_NORM_SAMPLE-"],
                                       "minimum": values["-FINAL_BIO_CALC_NORM_MIN-"],
                                       "max": values["-FINAL_BIO_CALC_NORM_MAX-"],
                                       "empty": values["-FINAL_BIO_CALC_NORM_EMPTY-"],
                                       "negative control": values["-FINAL_BIO_CALC_NORM_NEG_C-"],
                                       "positive control": values["-FINAL_BIO_CALC_NORM_POS_C-"],
                                       "blank": values["-FINAL_BIO_CALC_NORM_BLANK-"]},
                        "pora": {"overview": values["-FINAL_BIO_CAL_PORA-"],
                                 "sample": values["-FINAL_BIO_CALC_PORA_SAMPLE-"],
                                 "minimum": values["-FINAL_BIO_CALC_PORA_MIN-"],
                                 "max": values["-FINAL_BIO_CALC_PORA_MAX-"],
                                 "empty": values["-FINAL_BIO_CALC_PORA_EMPTY-"],
                                 "negative control": values["-FINAL_BIO_CALC_PORA_NEG_C-"],
                                 "positive control": values["-FINAL_BIO_CALC_PORA_POS_C-"],
                                 "blank": values["-FINAL_BIO_CALC_PORA_BLANK-"]},
                        "z_prime": values["-FINAL_BIO_Z_PRIME-"]},
                    "pora_threshold": {"low": {"min": values["-PORA_LOW_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PORA_LOW_MAX_HIT_THRESHOLD-"]},
                                       "mid": {"min": values["-PORA_MID_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PORA_MID_MAX_HIT_THRESHOLD-"]},
                                       "high": {"min": values["-PORA_HIGH_MIN_HIT_THRESHOLD-"],
                                                "max": values["-PORA_HIGH_MAX_HIT_THRESHOLD-"]}}
                }

                bio_plate_report_setup = {
                    "well_states_report": {"sample": values["-BIO_SAMPLE-"], "minimum": values["-BIO_MIN-"],
                                           "max": values["-BIO_MAX-"], "empty": values["-BIO_EMPTY-"],
                                           "negative": values["-BIO_NEG_C-"], "positive": values["-BIO_POS_C-"],
                                           "blank": values["-BIO_BLANK-"]},
                    "plate_calc_dict": {
                        "original": {"use": values["-BIO_PLATE_REPORT_ORG_CALC-"],
                                     "avg": values["-BIO_PLATE_CAL_ORG_AVG-"],
                                     "stdev": values["-BIO_PLATE_CAL_ORG_STDEV-"],
                                     "State": {"sample": values["-BIO_CAL_ORG_SAMPLE-"],
                                               "minimum": values["-BIO_CAL_ORG_MIN-"],
                                               "max": values["-BIO_CAL_ORG_MAX-"],
                                               "empty": values["-BIO_CAL_ORG_EMPTY-"],
                                               "negative": values["-BIO_CAL_ORG_NEG_C-"],
                                               "positive": values["-BIO_CAL_ORG_POS_C-"],
                                               "blank": values["-BIO_CAL_ORG_BLANK-"]}},
                        "normalised": {"use": values["-BIO_PLATE_REPORT_NORM_CALC-"],
                                       "avg": values["-BIO_PLATE_CAL_NORM_AVG-"], 
                                       "stdev": values["-BIO_PLATE_CAL_NORM_STDEV-"],
                                       "State": {"sample": values["-BIO_CAL_NORM_SAMPLE-"],
                                                 "minimum": values["-BIO_CAL_NORM_MIN-"],
                                                 "max": values["-BIO_CAL_NORM_MAX-"],
                                                 "empty": values["-BIO_CAL_NORM_EMPTY-"],
                                                 "negative": values["-BIO_CAL_NORM_NEG_C-"],
                                                 "positive": values["-BIO_CAL_NORM_POS_C-"],
                                                 "blank": values["-BIO_CAL_NORM_BLANK-"]}},
                        "pora": {"use": values["-BIO_PLATE_REPORT_PORA_CAL-"],
                                 "avg": values["-BIO_PLATE_CAL_PORA_AVG-"],
                                 "stdev": values["-BIO_PLATE_CAL_PORA_STDEV-"],
                                 "State": {"sample": values["-BIO_CAL_PORA_SAMPLE-"],
                                           "minimum": values["-BIO_CAL_PORA_MIN-"],
                                           "max": values["-BIO_CAL_PORA_MAX-"],
                                           "empty": values["-BIO_CAL_PORA_EMPTY-"],
                                           "negative": values["-BIO_CAL_PORA_NEG_C-"],
                                           "positive": values["-BIO_CAL_PORA_POS_C-"],
                                           "blank": values["-BIO_CAL_PORA_BLANK-"]}},
                        "pora_internal": {"use": values["-BIO_PLATE_REPORT_PORA_INTERNAL_CAL-"],
                                          "avg": values["-BIO_PLATE_CAL_PORA_INT_AVG-"],
                                          "stdev": values["-BIO_PLATE_CAL_PORA_INT_STDEV-"],
                                          "State": {"sample": values["-BIO_CAL_PORA_INT_SAMPLE-"],
                                                    "minimum": values["-BIO_CAL_PORA_INT_MIN-"],
                                                    "max": values["-BIO_CAL_PORA_INT_MAX-"],
                                                    "empty": values["-BIO_CAL_PORA_INT_EMPTY-"],
                                                    "negative": values["-BIO_CAL_PORA_INT_NEG_C-"],
                                                    "positive": values["-BIO_CAL_PORA_INT_POS_C-"],
                                                    "blank": values["-BIO_CAL_PORA_INT_BLANK-"]}}
                                          },
                    "plate_analysis_dict": {"original": {"used": values["-SINGLE_ORG_USE-"], "methode": org,
                                                         "state_mapping": values["-SINGLE_ORG_STATE-"],
                                                         "heatmap": values["-SINGLE_ORG_HEAT-"],
                                                         "Hit_Mapping": False},
                                            "normalised": {"used": values["-SINGLE_NORM_USE-"], "methode": norm,
                                                           "state_mapping": values["-SINGLE_norm_STATE-"],
                                                           "heatmap": values["-SINGLE_norm_HEAT-"],
                                                           "Hit_Mapping": False},
                                            "pora": {"used": values["-SINGLE_PORA_USE-"], "methode": pora,
                                                     "state_mapping": values["-SINGLE_PORA_STATE-"],
                                                     "heatmap": values["-SINGLE_PORA_HEAT-"],
                                                     "Hit_Mapping": values["-SINGLE_PORA_HIT-"]},
                                            "pora_internal": {"used": values["-SINGLE_PORA_INTERNAL_USE-"],
                                                              "methode": pora_internal,
                                                              "state_mapping": values["-SINGLE_PORA_INTERNAL_STATE-"],
                                                              "heatmap": values["-SINGLE_PORA_INTERNAL_HEAT-"],
                                                              "Hit_Mapping": values["-SINGLE_PORA_INTERNAL_HIT-"]}

                                            },
                    "z_prime_calc": values["-BIO_Z_PRIME-"],
                    "heatmap_colours": {"start": values["-HEAT_START-"],
                                        "mid": values["-HEAT_MID-"],
                                        "end": values["-HEAT_END-"]},
                    "pora_threshold": {"low": {"min": values["-PLATE_PORA_LOW_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PLATE_PORA_LOW_MAX_HIT_THRESHOLD-"]},
                                       "mid": {"min": values["-PLATE_PORA_MID_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PLATE_PORA_MID_MAX_HIT_THRESHOLD-"]},
                                       "high": {"min": values["-PLATE_PORA_HIGH_MIN_HIT_THRESHOLD-"],
                                                "max": values["-PLATE_PORA_HIGH_MAX_HIT_THRESHOLD-"]},
                                       "colour": {"low": "green",
                                                  "mid": "yellow",
                                                  "high": "blue"}}
                }

                return bio_final_report_setup, bio_plate_report_setup

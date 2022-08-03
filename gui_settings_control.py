from gui_settings import GUISettingsLayout
import PySimpleGUI as sg


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
                        "zprime": values["-FINAL_BIO_Z_PRIME-"]},
                    "pora_threshold": {"low": {"min": values["-PORA_LOW_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PORA_LOW_MAX_HIT_THRESHOLD-"]},
                                       "mid": {"min": values["-PORA_MID_MIN_HIT_THRESHOLD-"],
                                               "max": values["-PORA_MID_MAX_HIT_THRESHOLD-"]},
                                       "high": {"min": values["-PORA_HIGH_MIN_HIT_THRESHOLD-"],
                                                "max": values["-PORA_HIGH_MAX_HIT_THRESHOLD-"]}}
                }

                return bio_final_report_setup

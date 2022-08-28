import PySimpleGUI
import PySimpleGUI as sg
import configparser


class GUISettingsLayout:
    """

    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    """
    def __init__(self, config):

        self.config = config
        self.final_setup = None
        self.plate_setup = None
        self.ms_settings = None
        self.default = False

    # def settings_bio_final_report_default(self):
    #     """
    #
    #     :return: A layout for the final report settings
    #     :rtype: list
    #     """
    #     # setup disable state depending on bool statement for the headline of the group
    #     calc_org = not self.config["Settings_bio"].getboolean("final_report_calc_original_overview")
    #     calc_norm = not self.config["Settings_bio"].getboolean("final_report_calc_normalised_overview")
    #     calc_pora = not self.config["Settings_bio"].getboolean("final_report_calc_pora_overview")
    #
    #     matrix_sample = not self.config["Settings_bio"].getboolean("final_report_data_sample_matrix")
    #     matrix_minimum = not self.config["Settings_bio"].getboolean("final_report_data_minimum_matrix")
    #     matrix_maximum = not self.config["Settings_bio"].getboolean("final_report_data_max_matrix")
    #     matrix_empty = not self.config["Settings_bio"].getboolean("final_report_data_empty_matrix")
    #     matrix_negative = not self.config["Settings_bio"].getboolean("final_report_data_negative_control_matrix")
    #     matrix_positive = not self.config["Settings_bio"].getboolean("final_report_data_positive_control_matrix")
    #     matrix_blank = not self.config["Settings_bio"].getboolean("final_report_data_blank_matrix")
    #     matrix_z_prime = not self.config["Settings_bio"].getboolean("final_report_data_z_prime_matrix")
    #
    #     calc_col = sg.Frame("Calculations", [[
    #         sg.Column([
    #             [sg.T("What well status to include calculations for (avg, stdiv...)")],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("Original data", relief="groove"),
    #              sg.Checkbox("Include?", key="-FINAL_BIO_CAL_ORG-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_overview"))],
    #             [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_ORG_SAMPLE-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_sample")),
    #              sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_ORG_MIN-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_minimum")),
    #              sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_ORG_MAX-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_max")),
    #              sg.Checkbox("Empty", key="-FINAL_BIO_CALC_ORG_EMPTY-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_empty"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_ORG_NEG_C-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_negative")),
    #              sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_ORG_POS_C-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_positive")),
    #              sg.Checkbox("Blank", key="-FINAL_BIO_CALC_ORG_BLANK-", disabled=calc_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_original_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("Normalized data", relief="groove"),
    #              sg.Checkbox("Include?", key="-FINAL_BIO_CAL_NORM-",  enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_overview"))],
    #             [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_NORM_SAMPLE-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_sample")),
    #              sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_NORM_MIN-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_minimum")),
    #              sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_NORM_MAX-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_max")),
    #              sg.Checkbox("Empty", key="-FINAL_BIO_CALC_NORM_EMPTY-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_empty"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_NORM_NEG_C-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_negative")),
    #              sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_NORM_POS_C-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_positive")),
    #              sg.Checkbox("Blank", key="-FINAL_BIO_CALC_NORM_BLANK-",  disabled=calc_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_normalised_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("PORA data", relief="groove"),
    #              sg.Checkbox("Include?", key="-FINAL_BIO_CAL_PORA-", enable_events=True,
    #                          default=self.config["Settings_bio"].getboolean("final_report_calc_pora_overview"))],
    #             [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_PORA_SAMPLE-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_sample")),
    #              sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_PORA_MIN-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_minimum")),
    #              sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_PORA_MAX-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_max")),
    #              sg.Checkbox("Empty", key="-FINAL_BIO_CALC_PORA_EMPTY-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_empty"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_PORA_NEG_C-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_negative")),
    #              sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_PORA_POS_C-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_positive")),
    #              sg.Checkbox("Blank", key="-FINAL_BIO_CALC_PORA_BLANK-",  disabled=calc_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_pora_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Z-prime", key="-FINAL_BIO_Z_PRIME-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_calc_Z_prime"))]
    #
    #         ])
    #     ]])
    #
    #     well_col = sg.Frame("Well report", [[
    #         sg.Column([
    #             [sg.T("What wells to include in the final report, depending on status and analysed method")],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("What tables to include wells for:", relief="groove")],
    #             [sg.Checkbox("Original", key="-FINAL_BIO_ORG-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_methods_original")),
    #              sg.Checkbox("normalized", key="-FINAL_BIO_NORM-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_methods_normalised")),
    #              sg.Checkbox("Pora", key="-FINAL_BIO_PORA-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_methods_pora"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("What state to include wells for:", relief="groove")],
    #             [sg.Checkbox("Sample", key="-FINAL_BIO_SAMPLE-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_sample")),
    #              sg.Checkbox("Minimum", key="-FINAL_BIO_MIN-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_minimum")),
    #              sg.Checkbox("Maximum", key="-FINAL_BIO_MAX-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_max")),
    #              sg.Checkbox("Empty", key="-FINAL_BIO_EMPTY-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_empty"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_BIO_NEG_C-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_negative")),
    #              sg.Checkbox("Positive Control", key="-FINAL_BIO_POS_C-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_positive")),
    #              sg.Checkbox("Blank", key="-FINAL_BIO_BLANK-", default=self.config["Settings_bio"].
    #                          getboolean("final_report_analyse_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
    #             [sg.T("Lower bound", size=10),
    #              sg.InputText(key="-PORA_LOW_MIN_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_low_min")),
    #              sg.InputText(key="-PORA_LOW_MAX_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_low_max"))],
    #             [sg.T("Middle bound", size=10),
    #              sg.InputText(key="-PORA_MID_MIN_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_mid_min")),
    #              sg.InputText(key="-PORA_MID_MAX_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_mid_max"))],
    #             [sg.T("Higher bound", size=10),
    #              sg.InputText(key="-PORA_HIGH_MIN_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_high_min")),
    #              sg.InputText(key="-PORA_HIGH_MAX_HIT_THRESHOLD-", size=8, default_text=self.config["Settings_bio"].
    #                           getfloat("final_report_pora_threshold_high_max"))]
    #         ])
    #     ]])
    #
    #     data_col = sg.Frame("Matrix setup", [[
    #         sg.Column([
    #             [sg.T("Witch matrix to include.")],
    #             [sg.T("A Matrix is the avg and stdev for each plate compared to the other plates")],
    #             [sg.T("Only if the state is included in the analysis")],
    #             [sg.Checkbox("Sample", key="-FINAL_REPORT_MATRIX_SAMPLE-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_sample_matrix")),
    #              sg.Checkbox("Minimum", key="-FINAL_REPORT_MATRIX_MINIMUM-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_minimum_matrix")),
    #              sg.Checkbox("Max", key="-FINAL_REPORT_MATRIX_MAXIMUM-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_max_matrix")),
    #              sg.Checkbox("Empty", key="-FINAL_REPORT_MATRIX_EMPTY-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_empty_matrix"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_REPORT_MATRIX_NEGATIVE-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_negative_matrix")),
    #              sg.Checkbox("Positive Control", key="-FINAL_REPORT_MATRIX_POSITIVE-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_positive_matrix")),
    #              sg.Checkbox("Blank", key="-FINAL_REPORT_MATRIX_BLANK-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_blank_matrix")),
    #              sg.Checkbox("Z-Prime", key="-FINAL_REPORT_MATRIX_Z_PRIME-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_z_prime_matrix"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("Sorted list of values for the data chosen.")],
    #             [sg.T("Matrix data is needed for this option")],
    #             [sg.Checkbox("Sample", key="-FINAL_REPORT_LIST_SAMPLE-", disabled=matrix_sample,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_sample_list")),
    #              sg.Checkbox("Minimum", key="-FINAL_REPORT_LIST_MINIMUM-", disabled=matrix_minimum,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_minimum_list")),
    #              sg.Checkbox("Max", key="-FINAL_REPORT_LIST_MAXIMUM-", disabled=matrix_maximum,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_max_list")),
    #              sg.Checkbox("Empty", key="-FINAL_REPORT_LIST_EMPTY-", disabled=matrix_empty,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_empty_list"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_REPORT_LIST_NEGATIVE-", disabled=matrix_negative,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_negative_list")),
    #              sg.Checkbox("Positive Control", key="-FINAL_REPORT_LIST_POSITIVE-", disabled=matrix_positive,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_positive_list")),
    #              sg.Checkbox("Blank", key="-FINAL_REPORT_LIST_BLANK-", disabled=matrix_blank,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_blank_list")),
    #              sg.Checkbox("Z-Prime", key="-FINAL_REPORT_LIST_Z_PRIME-", disabled=matrix_z_prime,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("final_report_data_z_prime_list"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("Maximum and Minimums value for for the data chosen.")],
    #             [sg.T("Matrix data is needed for this option")],
    #             [sg.Checkbox("Sample", key="-FINAL_REPORT_MAX_MIN_SAMPLE-", disabled=matrix_sample,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_sample_max_min")),
    #              sg.Checkbox("Minimum", key="-FINAL_REPORT_MAX_MIN_MINIMUM-", disabled=matrix_minimum,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_minimum_max_min")),
    #              sg.Checkbox("Max", key="-FINAL_REPORT_MAX_MIN_MAXIMUM-", disabled=matrix_maximum,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_max_max_min")),
    #              sg.Checkbox("Empty", key="-FINAL_REPORT_MAX_MIN_EMPTY-", disabled=matrix_empty,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_empty_max_min"))],
    #             [sg.Checkbox("Negative Control", key="-FINAL_REPORT_MAX_MIN_NEGATIVE-", disabled=matrix_negative,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_negative_max_min"
    #                                                                         )),
    #              sg.Checkbox("Positive Control", key="-FINAL_REPORT_MAX_MIN_POSITIVE-", disabled=matrix_positive,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_positive_max_min"
    #                                                                         )),
    #              sg.Checkbox("Blank", key="-FINAL_REPORT_MAX_MIN_BLANK-", disabled=matrix_blank,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_blank_max_min")),
    #              sg.Checkbox("Z-Prime", key="-FINAL_REPORT_MAX_MIN_Z_PRIME-", disabled=matrix_z_prime,
    #                          default=self.config["Settings_bio"].getboolean("final_report_data_z_prime_max_min"))],
    #             [sg.HorizontalSeparator()],
    #         ])
    #     ]])
    #
    #     layout = [sg.vtop([calc_col, well_col, data_col])]
    #
    #     return layout
    #
    # def settings_bio_plate_report_default(self):
    #     """
    #
    #     :return: A layout for the plate report settings
    #     :rtype: list
    #     """
    #     # setup disable state depending on bool statement for the headline of the group
    #     analysis_sheet_org = not self.config["Settings_bio"].getboolean("plate_report_plate_calc_dict_original_use")
    #     analysis_sheet_norm = not self.config["Settings_bio"].getboolean("plate_report_plate_calc_dict_normalised_use")
    #     analysis_sheet_pora = not self.config["Settings_bio"].getboolean("plate_report_plate_calc_dict_pora_use")
    #
    #     report_sheet_org = not self.config["Settings_bio"].getboolean("plate_report_calc_dict_original_use")
    #     report_sheet_norm = not self.config["Settings_bio"].getboolean("plate_report_calc_dict_normalised_use")
    #     report_sheet_pora = not self.config["Settings_bio"].getboolean("plate_report_calc_dict_pora_use")
    #
    #     col_analysis_sheet = sg.Frame("Setup for analysis sheet", [[
    #         sg.Column([
    #             [sg.T("What calculation to include and for witch analysed method")],
    #             [sg.T("Will only take in samples and method that have been used")],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG_CALC-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_use")),
    #              sg.Checkbox("avg", key="-BIO_PLATE_CAL_ORG_AVG-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_avg"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("stdev", key="-BIO_PLATE_CAL_ORG_STDEV-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_stdev"),
    #                          disabled=analysis_sheet_org)],
    #             [sg.Checkbox("Sample", key="-BIO_CAL_ORG_SAMPLE-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_sample"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("Minimum", key="-BIO_CAL_ORG_MIN-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_minimum"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("Maximum", key="-BIO_CAL_ORG_MAX-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_max"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("Empty", key="-BIO_CAL_ORG_EMPTY-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_empty"),
    #                          disabled=analysis_sheet_org)],
    #             [sg.Checkbox("Negative Control", key="-BIO_CAL_ORG_NEG_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_negative"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("Positive Control", key="-BIO_CAL_ORG_POS_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_positive"),
    #                          disabled=analysis_sheet_org),
    #              sg.Checkbox("Blank", key="-BIO_CAL_ORG_BLANK-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_original_state_blank"),
    #                          disabled=analysis_sheet_org)],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM_CALC-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_use")),
    #              sg.Checkbox("avg", key="-BIO_PLATE_CAL_NORM_AVG-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_avg"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("stdev", key="-BIO_PLATE_CAL_NORM_STDEV-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_stdev"),
    #                          disabled=analysis_sheet_norm)],
    #             [sg.Checkbox("Sample", key="-BIO_CAL_NORM_SAMPLE-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_sample"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("Minimum", key="-BIO_CAL_NORM_MIN-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_minimum"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("Maximum", key="-BIO_CAL_NORM_MAX-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_max"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("Empty", key="-BIO_CAL_NORM_EMPTY-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_empty"),
    #                          disabled=analysis_sheet_norm)],
    #             [sg.Checkbox("Negative Control", key="-BIO_CAL_NORM_NEG_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_negative"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("Positive Control", key="-BIO_CAL_NORM_POS_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_positive"),
    #                          disabled=analysis_sheet_norm),
    #              sg.Checkbox("Blank", key="-BIO_CAL_NORM_BLANK-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_normalised_state_blank"),
    #                          disabled=analysis_sheet_norm)],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA_CAL-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_use")),
    #              sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_AVG-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_avg"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_STDEV-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_stdev"),
    #                          disabled=analysis_sheet_pora)],
    #             [sg.Checkbox("Sample", key="-BIO_CAL_PORA_SAMPLE-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_sample"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("Minimum", key="-BIO_CAL_PORA_MIN-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_minimum"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("Maximum", key="-BIO_CAL_PORA_MAX-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_max"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("Empty", key="-BIO_CAL_PORA_EMPTY-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_empty"),
    #                          disabled=analysis_sheet_pora)],
    #             [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_NEG_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_negative"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_POS_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_positive"),
    #                          disabled=analysis_sheet_pora),
    #              sg.Checkbox("Blank", key="-BIO_CAL_PORA_BLANK-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_plate_calc_dict_pora_state_blank"),
    #                          disabled=analysis_sheet_pora)],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Z prime", key="-BIO_Z_PRIME-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_z_prime_calc"))],
    #             [sg.HorizontalSeparator()],
    #             # [sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL_CAL-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_plate_calc_dict_pora_internal_use")),
    #             #  sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_INT_AVG-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_avg")),
    #             #  sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_INT_STDEV-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_stdev"))],
    #             # [sg.Checkbox("Sample", key="-BIO_CAL_PORA_INT_SAMPLE-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_plate_calc_dict_pora_internal_state_sample")),
    #             #  sg.Checkbox("Minimum", key="-BIO_CAL_PORA_INT_MIN-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_state_minimum")),
    #             #  sg.Checkbox("Maximum", key="-BIO_CAL_PORA_INT_MAX-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_state_max")),
    #             #  sg.Checkbox("Empty", key="-BIO_CAL_PORA_INT_EMPTY-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_state_empty"))],
    #             # [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_INT_NEG_C-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_plate_calc_dict_pora_internal_state_negative")),
    #             #  sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_INT_POS_C-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_state_positive")),
    #             #  sg.Checkbox("Blank", key="-BIO_CAL_PORA_INT_BLANK-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_plate_calc_dict_pora_internal_state_blank"))],
    #             # [sg.HorizontalSeparator()],
    #         ])
    #     ]])
    #
    #     col_report_sheet = sg.Frame("Setup for report sheet", [[
    #         sg.Column([
    #             [sg.T("Report setup per reading:", relief="groove")],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("What analysed method to include wells from, for the final report")],
    #             [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG-",
    #                          default=self.config["Settings_bio"].getboolean("well_states_report_method_original"))],
    #             [sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM-",
    #                          default=self.config["Settings_bio"].getboolean("well_states_report_method_normalised"))],
    #             [sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA-",
    #                          default=self.config["Settings_bio"].getboolean("well_states_report_method_pora"))],
    #             # [sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL-",
    #             # default=self.config["Settings_bio"].getboolean("well_states_report_method_pora_internal"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("What well-state to include for the final report")],
    #             [sg.Checkbox("Sample", key="-BIO_SAMPLE-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_sample")),
    #              sg.Checkbox("Minimum", key="-BIO_MIN-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_minimum")),
    #              sg.Checkbox("Maximum", key="-BIO_MAX-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_max")),
    #              sg.Checkbox("Empty", key="-BIO_EMPTY-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_empty"))],
    #             [sg.Checkbox("Negative Control", key="-BIO_NEG_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_negative")),
    #              sg.Checkbox("Positive Control", key="-BIO_POS_C-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_positive")),
    #              sg.Checkbox("Blank", key="-BIO_BLANK-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_well_states_report_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Text("What calculations that will be included on the final report")],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Other calculations", key="-BIO_REPORT_SHEET_OTHER-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_other_use")),
    #              sg.Checkbox("Z prime", key="-BIO_REPORT_SHEET_Z_PRIME-", default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_other_calc_z_prime"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Original", key="-BIO_REPORT_SHEET_ORG_CALC-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_use")),
    #              sg.Checkbox("avg", key="-BIO_REPORT_CAL_ORG_AVG-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_avg")),
    #              sg.Checkbox("stdev", key="-BIO_REPORT_CAL_ORG_STDEV-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_stdev"))],
    #             [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_ORG_SAMPLE-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_sample")),
    #              sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_ORG_MIN-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_minimum")),
    #              sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_ORG_MAX-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_max")),
    #              sg.Checkbox("Empty", key="-BIO_REPORT_CAL_ORG_EMPTY-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_empty"))],
    #             [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_ORG_NEG_C-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_negative")),
    #              sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_ORG_POS_C-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_positive")),
    #              sg.Checkbox("Blank", key="-BIO_REPORT_CAL_ORG_BLANK-", disabled=report_sheet_org,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_original_state_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Normalised", key="-BIO_REPORT_SHEET_NORM_CALC-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_use")),
    #              sg.Checkbox("avg", key="-BIO_REPORT_CAL_NORM_AVG-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_avg")),
    #              sg.Checkbox("stdev", key="-BIO_REPORT_CAL_NORM_STDEV-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_stdev"))],
    #             [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_NORM_SAMPLE-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_sample")),
    #              sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_NORM_MIN-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_minimum")),
    #              sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_NORM_MAX-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_max")),
    #              sg.Checkbox("Empty", key="-BIO_REPORT_CAL_NORM_EMPTY-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_empty"))],
    #             [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_NORM_NEG_C-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_negative")),
    #              sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_NORM_POS_C-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_positive")),
    #              sg.Checkbox("Blank", key="-BIO_REPORT_CAL_NORM_BLANK-", disabled=report_sheet_norm,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_normalised_state_blank"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.Checkbox("Pora", key="-BIO_REPORT_SHEET_PORA_CAL-", enable_events=True,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_use")),
    #              sg.Checkbox("avg", key="-BIO_REPORT_CAL_PORA_AVG-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_avg")),
    #              sg.Checkbox("stdev", key="-BIO_REPORT_CAL_PORA_STDEV-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_stdev"))],
    #             [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_PORA_SAMPLE-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_sample")),
    #              sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_PORA_MIN-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_minimum")),
    #              sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_PORA_MAX-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_max")),
    #              sg.Checkbox("Empty", key="-BIO_REPORT_CAL_PORA_EMPTY-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_empty"))],
    #             [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_PORA_NEG_C-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_negative")),
    #              sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_PORA_POS_C-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_positive")),
    #              sg.Checkbox("Blank", key="-BIO_REPORT_CAL_PORA_BLANK-", disabled=report_sheet_pora,
    #                          default=self.config["Settings_bio"].
    #                          getboolean("plate_report_calc_dict_pora_state_blank"))],
    #             [sg.HorizontalSeparator()],
    #             # [sg.Checkbox("Pora Internal", key="-BIO_REPORT_SHEET_PORA_INTERNAL_CAL-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_calc_dict_pora_internal_use")),
    #             #  sg.Checkbox("avg", key="-BIO_REPORT_CAL_PORA_INT_AVG-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_avg")),
    #             #  sg.Checkbox("stdev", key="-BIO_REPORT_CAL_PORA_INT_STDEV-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_stdev"))],
    #             # [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_PORA_INT_SAMPLE-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_calc_dict_pora_internal_state_sample")),
    #             #  sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_PORA_INT_MIN-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_state_minimum")),
    #             #  sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_PORA_INT_MAX-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_state_max")),
    #             #  sg.Checkbox("Empty", key="-BIO_REPORT_CAL_PORA_INT_EMPTY-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_state_empty"))],
    #             # [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_PORA_INT_NEG_C-",
    #             # default=self.config["Settings_bio"].
    #             # getboolean("plate_report_calc_dict_pora_internal_state_negative")),
    #             #  sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_PORA_INT_POS_C-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_state_positive")),
    #             #  sg.Checkbox("Blank", key="-BIO_REPORT_CAL_PORA_INT_BLANK-",
    #             #  default=self.config["Settings_bio"].
    #             #  getboolean("plate_report_calc_dict_pora_internal_state_blank"))],
    #
    #         ])
    #     ]], expand_y=True)
    #     single_point_layout = self.method_single_point_default()
    #     tab_single_point = sg.Tab("Single point", single_point_layout)
    #
    #     tab_group_analysis_method = [tab_single_point]
    #     col_analysis_method = sg.TabGroup([tab_group_analysis_method], selected_background_color="purple")
    #
    #     # layout = [[col_analysis_sheet, col_report_sheet, col_analysis_method]]
    #     layout = [sg.vtop([col_analysis_sheet, col_report_sheet, col_analysis_method])]
    #
    #     return layout
    #
    # def method_single_point_default(self):
    #     """
    #
    #     :return: A layout for the analys method settings
    #     :rtype: list
    #     """
    #     colours = [keys for keys in list(self.config["colours to hex"].keys())]
    #
    #     single_point = sg.Frame("Single point report setup", [[
    #         sg.Column([
    #             [sg.T("Original data", relief="groove"),
    #              # sg.Checkbox("use?", key="-SINGLE_ORG_USE-", default=self.config["Settings_bio"].
    #              #             getboolean("plate_report_plate_analysis_dict_original_use"))
    #                          ],
    #             [sg.Radio("Colour Well State", group_id=1, key="-SINGLE_ORG_STATE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_original_state_map")),
    #              sg.Radio("Heatmap", group_id=1, key="-SINGLE_ORG_HEAT-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_original_heatmap")),
    #              sg.Radio("None", group_id=1, key="-SINGLE_ORG_NONE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_original_none"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("normalised data", relief="groove"),
    #              # sg.Checkbox("use?", key="-SINGLE_NORM_USE-", default=self.config["Settings_bio"].
    #              #             getboolean("plate_report_plate_analysis_dict_normalised_use"))
    #              ],
    #             [sg.Radio("Colour Well State", group_id=2, key="-SINGLE_norm_STATE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_normalised_state_map")),
    #              sg.Radio("Heatmap", group_id=2, key="-SINGLE_norm_HEAT-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_normalised_heatmap")),
    #              sg.Radio("None", group_id=2, key="-SINGLE_norm_NONE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_normalised_none"))],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("PORA data", relief="groove"),
    #              # sg.Checkbox("use?", key="-SINGLE_PORA_USE-", default=self.config["Settings_bio"].
    #              #             getboolean("plate_report_plate_analysis_dict_pora_use"))
    #              ],
    #             [sg.Radio("Colour Well State", group_id=3, key="-SINGLE_PORA_STATE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_pora_state_map")),
    #              sg.Radio("Heatmap", group_id=3, key="-SINGLE_PORA_HEAT-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_pora_heatmap")),
    #              sg.Radio("Hit Mapping", group_id=3, key="-SINGLE_PORA_HIT-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_pora_hit_map")),
    #              sg.Radio("None", group_id=3, key="-SINGLE_PORA_NONE-", default=self.config["Settings_bio"].
    #                       getboolean("plate_report_plate_analysis_dict_pora_none"))],
    #             [sg.HorizontalSeparator()],
    #             # [sg.T("PORA Internal data", relief="groove"),
    #             #  sg.Checkbox("use?", key="-SINGLE_PORA_INTERNAL_USE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_use"))],
    #             # [sg.Radio("Colour Well State", group_id=4, key="-SINGLE_PORA_INTERNAL_STATE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_state_map")),
    #             #  sg.Radio("Heatmap", group_id=4, key="-SINGLE_PORA_INTERNAL_HEAT-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_heat_map")),
    #             #  sg.Radio("Hit Mapping", group_id=4, key="-SINGLE_PORA_INTERNAL_HIT-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_hit_map")),
    #             #  sg.Radio("None", group_id=4, key="-SINGLE_PORA_INTERNAL_NONE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_none"))],
    #             # [sg.HorizontalSeparator()],
    #             # This Could be the same as the full report...
    #             [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
    #             [sg.T("Lower bound", size=10),
    #              sg.InputText(key="-PLATE_PORA_LOW_MIN_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_low_min")),
    #              sg.InputText(key="-PLATE_PORA_LOW_MAX_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_low_max"))],
    #             [sg.T("Middle bound", size=10),
    #              sg.InputText(key="-PLATE_PORA_MID_MIN_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_mid_min")),
    #              sg.InputText(key="-PLATE_PORA_MID_MAX_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_mid_max"))],
    #             [sg.T("Higher bound", size=10),
    #              sg.InputText(key="-PLATE_PORA_HIGH_MIN_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_high_min")),
    #              sg.InputText(key="-PLATE_PORA_HIGH_MAX_HIT_THRESHOLD-", size=8, default_text=self.
    #                           config["Settings_bio"].getfloat("plate_report_pora_threshold_high_max"))],
    #             [sg.T("Hit map colours")],
    #             [sg.DropDown(colours, key="-PLATE_REPORT_HIT_LOW-", size=15, default_value=self.
    #                          config["Settings_bio"]["plate_report_pora_threshold_colour_low"]),
    #             sg.DropDown(colours, key="-PLATE_REPORT_HIT_MID-", size=15, default_value=self.
    #                         config["Settings_bio"]["plate_report_pora_threshold_colour_mid"]),
    #             sg.DropDown(colours, key="-PLATE_REPORT_HIT_HIGH-", size=15, default_value=self.
    #                         config["Settings_bio"]["plate_report_pora_threshold_colour_high"])],
    #             [sg.HorizontalSeparator()],
    #             [sg.T("Heatmap settings")],
    #             [sg.Text("start Colour:", size=15), sg.Text("Mid Colour:", size=15), sg.Text("End Colour:", size=15)],
    #             [sg.DropDown(colours, key="-PLATE_REPORT_HEAT_START-", size=15, default_value=self.
    #                          config["Settings_bio"]["plate_report_heatmap_colours_start"]),
    #              sg.DropDown(colours, key="-PLATE_REPORT_HEAT_MID-", size=15, default_value=self.
    #                          config["Settings_bio"]["plate_report_heatmap_colours_mid"]),
    #              sg.DropDown(colours, key="-PLATE_REPORT_HEAT_END-", size=15, default_value=
    #              self.config["Settings_bio"]["plate_report_heatmap_colours_end"])],
    #
    #
    #         ])
    #     ]])
    #
    #     layout = [[single_point]]
    #
    #     return layout

    def settings_bio_final_report(self):
        """

        :return: A layout for the final report settings
        :rtype: list
        """
        # setup disable state depending on bool statement for the headline of the group
        calc_org = not self.final_setup["calc"]["original"]["overview"]
        calc_norm = not self.final_setup["calc"]["normalised"]["overview"]
        calc_pora = not self.final_setup["calc"]["pora"]["overview"]

        matrix_sample = not self.final_setup["data"]["sample"]["matrix"]
        matrix_minimum = not self.final_setup["data"]["minimum"]["matrix"]
        matrix_maximum = not self.final_setup["data"]["max"]["matrix"]
        matrix_empty = not self.final_setup["data"]["empty"]["matrix"]
        matrix_negative = not self.final_setup["data"]["negative"]["matrix"]
        matrix_positive = not self.final_setup["data"]["positive"]["matrix"]
        matrix_blank = not self.final_setup["data"]["blank"]["matrix"]
        matrix_z_prime = not self.final_setup["data"]["z_prime"]["matrix"]

        calc_col = sg.Frame("Calculations", [[
            sg.Column([
                [sg.T("What well status to include calculations for (avg, stdiv...)")],
                [sg.HorizontalSeparator()],
                [sg.T("Original data", relief="groove"),
                 sg.Checkbox("Include?", key="-FINAL_BIO_CAL_ORG-", enable_events=True,
                             default=self.final_setup["calc"]["original"]["overview"])],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_ORG_SAMPLE-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["sample"]),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_ORG_MIN-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["minimum"]),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_ORG_MAX-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["max"]),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_ORG_EMPTY-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["empty"])],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_ORG_NEG_C-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["negative"]),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_ORG_POS_C-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["positive"]),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_ORG_BLANK-", disabled=calc_org,
                             default=self.final_setup["calc"]["original"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.T("Normalized data", relief="groove"),
                 sg.Checkbox("Include?", key="-FINAL_BIO_CAL_NORM-",  enable_events=True,
                             default=self.final_setup["calc"]["normalised"]["overview"])],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_NORM_SAMPLE-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["sample"]),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_NORM_MIN-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["minimum"]),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_NORM_MAX-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["max"]),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_NORM_EMPTY-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["empty"])],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_NORM_NEG_C-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["negative"]),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_NORM_POS_C-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["positive"]),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_NORM_BLANK-",  disabled=calc_norm,
                             default=self.final_setup["calc"]["normalised"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.T("PORA data", relief="groove"),
                 sg.Checkbox("Include?", key="-FINAL_BIO_CAL_PORA-", enable_events=True,
                             default=self.final_setup["calc"]["pora"]["overview"])],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_PORA_SAMPLE-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["sample"]),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_PORA_MIN-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["minimum"]),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_PORA_MAX-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["max"]),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_PORA_EMPTY-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["empty"])],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_PORA_NEG_C-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["negative"]),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_PORA_POS_C-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["positive"]),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_PORA_BLANK-",  disabled=calc_pora,
                             default=self.final_setup["calc"]["pora"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Z-prime", key="-FINAL_BIO_Z_PRIME-", default=self.final_setup["calc"]["z_prime"])]

            ])
        ]])

        well_col = sg.Frame("Well report", [[
            sg.Column([
                [sg.T("What wells to include in the final report, depending on status and analysed method")],
                [sg.HorizontalSeparator()],
                [sg.T("What tables to include wells for:", relief="groove")],
                [sg.Checkbox("Original", key="-FINAL_BIO_ORG-", default=self.final_setup["methods"]["original"]),
                 sg.Checkbox("normalized", key="-FINAL_BIO_NORM-", default=self.final_setup["methods"]["normalised"]),
                 sg.Checkbox("Pora", key="-FINAL_BIO_PORA-", default=self.final_setup["methods"]["pora"])],
                [sg.HorizontalSeparator()],
                [sg.T("What state to include wells for:", relief="groove")],
                [sg.Checkbox("Sample", key="-FINAL_BIO_SAMPLE-", default=self.final_setup["analyse"]["sample"]),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_MIN-", default=self.final_setup["analyse"]["minimum"]),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_MAX-", default=self.final_setup["analyse"]["max"]),
                 sg.Checkbox("Empty", key="-FINAL_BIO_EMPTY-", default=self.final_setup["analyse"]["empty"])],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_NEG_C-",
                             default=self.final_setup["analyse"]["negative"]),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_POS_C-",
                             default=self.final_setup["analyse"]["positive"]),
                 sg.Checkbox("Blank", key="-FINAL_BIO_BLANK-", default=self.final_setup["analyse"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
                [sg.T("Lower bound", size=10),
                 sg.InputText(key="-PORA_LOW_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["low"]["min"]),
                 sg.InputText(key="-PORA_LOW_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["low"]["max"])],
                [sg.T("Middle bound", size=10),
                 sg.InputText(key="-PORA_MID_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["mid"]["min"]),
                 sg.InputText(key="-PORA_MID_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["mid"]["max"])],
                [sg.T("Higher bound", size=10),
                 sg.InputText(key="-PORA_HIGH_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["high"]["min"]),
                 sg.InputText(key="-PORA_HIGH_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.final_setup["pora_threshold"]["high"]["max"])]
            ])
        ]])

        data_col = sg.Frame("Matrix setup", [[
            sg.Column([
                [sg.T("Witch matrix to include.")],
                [sg.T("A Matrix is the avg and stdev for each plate compared to the other plates")],
                [sg.T("Only if the state is included in the analysis")],
                [sg.Checkbox("Sample", key="-FINAL_REPORT_MATRIX_SAMPLE-", enable_events=True,
                             default=self.final_setup["data"]["sample"]["matrix"]),
                 sg.Checkbox("Minimum", key="-FINAL_REPORT_MATRIX_MINIMUM-", enable_events=True,
                             default=self.final_setup["data"]["minimum"]["matrix"]),
                 sg.Checkbox("Max", key="-FINAL_REPORT_MATRIX_MAXIMUM-", enable_events=True,
                             default=self.final_setup["data"]["max"]["matrix"]),
                 sg.Checkbox("Empty", key="-FINAL_REPORT_MATRIX_EMPTY-", enable_events=True,
                             default=self.final_setup["data"]["empty"]["matrix"])],
                [sg.Checkbox("Negative Control", key="-FINAL_REPORT_MATRIX_NEGATIVE-", enable_events=True,
                             default=self.final_setup["data"]["negative"]["matrix"]),
                 sg.Checkbox("Positive Control", key="-FINAL_REPORT_MATRIX_POSITIVE-", enable_events=True,
                             default=self.final_setup["data"]["positive"]["matrix"]),
                 sg.Checkbox("Blank", key="-FINAL_REPORT_MATRIX_BLANK-", enable_events=True,
                             default=self.final_setup["data"]["blank"]["matrix"]),
                 sg.Checkbox("Z-Prime", key="-FINAL_REPORT_MATRIX_Z_PRIME-", enable_events=True,
                             default=self.final_setup["data"]["z_prime"]["matrix"])],
                [sg.HorizontalSeparator()],
                [sg.T("Sorted list of values for the data chosen.")],
                [sg.T("Matrix data is needed for this option")],
                [sg.Checkbox("Sample", key="-FINAL_REPORT_LIST_SAMPLE-", disabled=matrix_sample,
                             default=self.final_setup["data"]["sample"]["list"]),
                 sg.Checkbox("Minimum", key="-FINAL_REPORT_LIST_MINIMUM-", disabled=matrix_minimum,
                             default=self.final_setup["data"]["minimum"]["list"]),
                 sg.Checkbox("Max", key="-FINAL_REPORT_LIST_MAXIMUM-", disabled=matrix_maximum,
                             default=self.final_setup["data"]["max"]["list"]),
                 sg.Checkbox("Empty", key="-FINAL_REPORT_LIST_EMPTY-", disabled=matrix_empty,
                             default=self.final_setup["data"]["empty"]["list"])],
                [sg.Checkbox("Negative Control", key="-FINAL_REPORT_LIST_NEGATIVE-", disabled=matrix_negative,
                             default=self.final_setup["data"]["negative"]["list"]),
                 sg.Checkbox("Positive Control", key="-FINAL_REPORT_LIST_POSITIVE-", disabled=matrix_positive,
                             default=self.final_setup["data"]["positive"]["list"]),
                 sg.Checkbox("Blank", key="-FINAL_REPORT_LIST_BLANK-", disabled=matrix_blank,
                             default=self.final_setup["data"]["blank"]["list"]),
                 sg.Checkbox("Z-Prime", key="-FINAL_REPORT_LIST_Z_PRIME-", disabled=matrix_z_prime,
                             default=self.final_setup["data"]["z_prime"]["list"])],
                [sg.HorizontalSeparator()],
                [sg.T("Maximum and Minimums value for for the data chosen.")],
                [sg.T("Matrix data is needed for this option")],
                [sg.Checkbox("Sample", key="-FINAL_REPORT_MAX_MIN_SAMPLE-", disabled=matrix_sample,
                             default=self.final_setup["data"]["sample"]["max_min"]),
                 sg.Checkbox("Minimum", key="-FINAL_REPORT_MAX_MIN_MINIMUM-", disabled=matrix_minimum,
                             default=self.final_setup["data"]["minimum"]["max_min"]),
                 sg.Checkbox("Max", key="-FINAL_REPORT_MAX_MIN_MAXIMUM-", disabled=matrix_maximum,
                             default=self.final_setup["data"]["max"]["max_min"]),
                 sg.Checkbox("Empty", key="-FINAL_REPORT_MAX_MIN_EMPTY-", disabled=matrix_empty,
                             default=self.final_setup["data"]["empty"]["max_min"])],
                [sg.Checkbox("Negative Control", key="-FINAL_REPORT_MAX_MIN_NEGATIVE-", disabled=matrix_negative,
                             default=self.final_setup["data"]["negative"]["max_min"]),
                 sg.Checkbox("Positive Control", key="-FINAL_REPORT_MAX_MIN_POSITIVE-", disabled=matrix_positive,
                             default=self.final_setup["data"]["positive"]["max_min"]),
                 sg.Checkbox("Blank", key="-FINAL_REPORT_MAX_MIN_BLANK-", disabled=matrix_blank,
                             default=self.final_setup["data"]["blank"]["max_min"]),
                 sg.Checkbox("Z-Prime", key="-FINAL_REPORT_MAX_MIN_Z_PRIME-", disabled=matrix_z_prime,
                             default=self.final_setup["data"]["z_prime"]["max_min"])],
                [sg.HorizontalSeparator()],
            ])
        ]])

        layout = [sg.vtop([calc_col, well_col, data_col])]

        return layout

    def settings_bio_plate_report(self):
        """

        :return: A layout for the plate report settings
        :rtype: list
        """

        # setup disable state depending on bool statement for the headline of the group
        analysis_sheet_org = not self.plate_setup["plate_calc_dict"]["original"]["use"]
        analysis_sheet_norm = not self.plate_setup["plate_calc_dict"]["normalised"]["use"]
        analysis_sheet_pora = not self.plate_setup["plate_calc_dict"]["pora"]["use"]

        report_sheet_org = not self.plate_setup["calc_dict"]["original"]["use"]
        report_sheet_norm = not self.plate_setup["calc_dict"]["normalised"]["use"]
        report_sheet_pora = not self.plate_setup["calc_dict"]["pora"]["use"]

        col_analysis_sheet = sg.Frame("Setup for analysis sheet", [[
            sg.Column([
                [sg.T("What calculation to include and for witch analysed method")],
                [sg.T("Will only take in samples and method that have been used")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG_CALC-", enable_events=True,
                             default=self.plate_setup["plate_calc_dict"]["original"]["use"]),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_ORG_AVG-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["avg"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_ORG_STDEV-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["stdev"],
                             disabled=analysis_sheet_org)],
                [sg.Checkbox("Sample", key="-BIO_CAL_ORG_SAMPLE-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["sample"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("Minimum", key="-BIO_CAL_ORG_MIN-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["minimum"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("Maximum", key="-BIO_CAL_ORG_MAX-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["max"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("Empty", key="-BIO_CAL_ORG_EMPTY-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["empty"],
                             disabled=analysis_sheet_org)],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_ORG_NEG_C-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["negative"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_ORG_POS_C-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["positive"],
                             disabled=analysis_sheet_org),
                 sg.Checkbox("Blank", key="-BIO_CAL_ORG_BLANK-",
                             default=self.plate_setup["plate_calc_dict"]["original"]["state"]["blank"],
                             disabled=analysis_sheet_org)],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM_CALC-", enable_events=True,
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["use"]),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_NORM_AVG-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["avg"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_NORM_STDEV-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["stdev"],
                             disabled=analysis_sheet_norm)],
                [sg.Checkbox("Sample", key="-BIO_CAL_NORM_SAMPLE-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["sample"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("Minimum", key="-BIO_CAL_NORM_MIN-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["minimum"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("Maximum", key="-BIO_CAL_NORM_MAX-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["max"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("Empty", key="-BIO_CAL_NORM_EMPTY-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["empty"],
                             disabled=analysis_sheet_norm)],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_NORM_NEG_C-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["negative"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_NORM_POS_C-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["positive"],
                             disabled=analysis_sheet_norm),
                 sg.Checkbox("Blank", key="-BIO_CAL_NORM_BLANK-",
                             default=self.plate_setup["plate_calc_dict"]["normalised"]["state"]["blank"],
                             disabled=analysis_sheet_norm)],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA_CAL-", enable_events=True,
                             default=self.plate_setup["plate_calc_dict"]["pora"]["use"]),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_AVG-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["avg"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_STDEV-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["stdev"],
                             disabled=analysis_sheet_pora)],
                [sg.Checkbox("Sample", key="-BIO_CAL_PORA_SAMPLE-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["sample"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("Minimum", key="-BIO_CAL_PORA_MIN-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["minimum"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("Maximum", key="-BIO_CAL_PORA_MAX-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["max"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("Empty", key="-BIO_CAL_PORA_EMPTY-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["empty"],
                             disabled=analysis_sheet_pora)],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_NEG_C-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["negative"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_POS_C-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["positive"],
                             disabled=analysis_sheet_pora),
                 sg.Checkbox("Blank", key="-BIO_CAL_PORA_BLANK-",
                             default=self.plate_setup["plate_calc_dict"]["pora"]["state"]["blank"],
                             disabled=analysis_sheet_pora)],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Z prime", key="-BIO_Z_PRIME-", default=self.plate_setup["z_prime_calc"])],
                [sg.HorizontalSeparator()],
                # [sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL_CAL-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_plate_calc_dict_pora_internal_use")),
                #  sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_INT_AVG-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_avg")),
                #  sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_INT_STDEV-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_stdev"))],
                # [sg.Checkbox("Sample", key="-BIO_CAL_PORA_INT_SAMPLE-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_plate_calc_dict_pora_internal_state_sample")),
                #  sg.Checkbox("Minimum", key="-BIO_CAL_PORA_INT_MIN-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_state_minimum")),
                #  sg.Checkbox("Maximum", key="-BIO_CAL_PORA_INT_MAX-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_state_max")),
                #  sg.Checkbox("Empty", key="-BIO_CAL_PORA_INT_EMPTY-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_state_empty"))],
                # [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_INT_NEG_C-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_plate_calc_dict_pora_internal_state_negative")),
                #  sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_INT_POS_C-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_state_positive")),
                #  sg.Checkbox("Blank", key="-BIO_CAL_PORA_INT_BLANK-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_plate_calc_dict_pora_internal_state_blank"))],
                # [sg.HorizontalSeparator()],
            ])
        ]])

        col_report_sheet = sg.Frame("Setup for report sheet", [[
            sg.Column([
                [sg.T("Report setup per reading:", relief="groove")],
                [sg.HorizontalSeparator()],
                [sg.T("What analysed method to include wells from, for the final report")],
                [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG-",
                             default=self.plate_setup["well_states_report_method"]["original"])],
                [sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM-",
                             default=self.plate_setup["well_states_report_method"]["normalised"])],
                [sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA-",
                             default=self.plate_setup["well_states_report_method"]["pora"])],
                # [sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL-",
                # default=self.plate_setup["well_states_report_method"]["pora_internal"])],
                [sg.HorizontalSeparator()],
                [sg.T("What well-state to include for the final report")],
                [sg.Checkbox("Sample", key="-BIO_SAMPLE-",
                             default=self.plate_setup["well_states_report"]["sample"]),
                 sg.Checkbox("Minimum", key="-BIO_MIN-",
                             default=self.plate_setup["well_states_report"]["blank"]),
                 sg.Checkbox("Maximum", key="-BIO_MAX-",
                             default=self.plate_setup["well_states_report"]["max"]),
                 sg.Checkbox("Empty", key="-BIO_EMPTY-",
                             default=self.plate_setup["well_states_report"]["minimum"])],
                [sg.Checkbox("Negative Control", key="-BIO_NEG_C-",
                             default=self.plate_setup["well_states_report"]["positive"]),
                 sg.Checkbox("Positive Control", key="-BIO_POS_C-",
                             default=self.plate_setup["well_states_report"]["negative"]),
                 sg.Checkbox("Blank", key="-BIO_BLANK-",
                             default=self.plate_setup["well_states_report"]["empty"])],
                [sg.HorizontalSeparator()],
                [sg.Text("What calculations that will be included on the final report")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Other calculations", key="-BIO_REPORT_SHEET_OTHER-",
                             default=self.plate_setup["calc_dict"]["other"]["use"]),
                 sg.Checkbox("Z prime", key="-BIO_REPORT_SHEET_Z_PRIME-",
                             default=self.plate_setup["calc_dict"]["other"]["calc"]["z_prime"])],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Original", key="-BIO_REPORT_SHEET_ORG_CALC-", enable_events=True,
                             default=self.plate_setup["calc_dict"]["original"]["use"]),
                 sg.Checkbox("avg", key="-BIO_REPORT_CAL_ORG_AVG-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["avg"]),
                 sg.Checkbox("stdev", key="-BIO_REPORT_CAL_ORG_STDEV-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["stdev"])],
                [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_ORG_SAMPLE-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["sample"]),
                 sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_ORG_MIN-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["minimum"]),
                 sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_ORG_MAX-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["max"]),
                 sg.Checkbox("Empty", key="-BIO_REPORT_CAL_ORG_EMPTY-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["empty"])],
                [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_ORG_NEG_C-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["negative"]),
                 sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_ORG_POS_C-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["positive"]),
                 sg.Checkbox("Blank", key="-BIO_REPORT_CAL_ORG_BLANK-", disabled=report_sheet_org,
                             default=self.plate_setup["calc_dict"]["original"]["state"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Normalised", key="-BIO_REPORT_SHEET_NORM_CALC-", enable_events=True,
                             default=self.plate_setup["calc_dict"]["normalised"]["use"]),
                 sg.Checkbox("avg", key="-BIO_REPORT_CAL_NORM_AVG-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["avg"]),
                 sg.Checkbox("stdev", key="-BIO_REPORT_CAL_NORM_STDEV-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["stdev"])],
                [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_NORM_SAMPLE-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["sample"]),
                 sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_NORM_MIN-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["minimum"]),
                 sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_NORM_MAX-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["max"]),
                 sg.Checkbox("Empty", key="-BIO_REPORT_CAL_NORM_EMPTY-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["empty"])],
                [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_NORM_NEG_C-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["negative"]),
                 sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_NORM_POS_C-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["positive"]),
                 sg.Checkbox("Blank", key="-BIO_REPORT_CAL_NORM_BLANK-", disabled=report_sheet_norm,
                             default=self.plate_setup["calc_dict"]["normalised"]["state"]["blank"])],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Pora", key="-BIO_REPORT_SHEET_PORA_CAL-", enable_events=True,
                             default=self.plate_setup["calc_dict"]["pora"]["use"]),
                 sg.Checkbox("avg", key="-BIO_REPORT_CAL_PORA_AVG-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["avg"]),
                 sg.Checkbox("stdev", key="-BIO_REPORT_CAL_PORA_STDEV-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["stdev"])],
                [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_PORA_SAMPLE-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["sample"]),
                 sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_PORA_MIN-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["minimum"]),
                 sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_PORA_MAX-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["max"]),
                 sg.Checkbox("Empty", key="-BIO_REPORT_CAL_PORA_EMPTY-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["empty"])],
                [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_PORA_NEG_C-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["negative"]),
                 sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_PORA_POS_C-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["positive"]),
                 sg.Checkbox("Blank", key="-BIO_REPORT_CAL_PORA_BLANK-", disabled=report_sheet_pora,
                             default=self.plate_setup["calc_dict"]["pora"]["state"]["blank"])],
                [sg.HorizontalSeparator()],
                # [sg.Checkbox("Pora Internal", key="-BIO_REPORT_SHEET_PORA_INTERNAL_CAL-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_calc_dict_pora_internal_use")),
                #  sg.Checkbox("avg", key="-BIO_REPORT_CAL_PORA_INT_AVG-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_avg")),
                #  sg.Checkbox("stdev", key="-BIO_REPORT_CAL_PORA_INT_STDEV-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_stdev"))],
                # [sg.Checkbox("Sample", key="-BIO_REPORT_CAL_PORA_INT_SAMPLE-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_calc_dict_pora_internal_state_sample")),
                #  sg.Checkbox("Minimum", key="-BIO_REPORT_CAL_PORA_INT_MIN-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_state_minimum")),
                #  sg.Checkbox("Maximum", key="-BIO_REPORT_CAL_PORA_INT_MAX-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_state_max")),
                #  sg.Checkbox("Empty", key="-BIO_REPORT_CAL_PORA_INT_EMPTY-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_state_empty"))],
                # [sg.Checkbox("Negative Control", key="-BIO_REPORT_CAL_PORA_INT_NEG_C-",
                # default=self.config["Settings_bio"].
                # getboolean("plate_report_calc_dict_pora_internal_state_negative")),
                #  sg.Checkbox("Positive Control", key="-BIO_REPORT_CAL_PORA_INT_POS_C-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_state_positive")),
                #  sg.Checkbox("Blank", key="-BIO_REPORT_CAL_PORA_INT_BLANK-",
                #  default=self.config["Settings_bio"].
                #  getboolean("plate_report_calc_dict_pora_internal_state_blank"))],

            ])
        ]], expand_y=True)
        single_point_layout = self.bio_method_single_point()
        tab_single_point = sg.Tab("Single point", single_point_layout)

        tab_group_analysis_method = [tab_single_point]
        col_analysis_method = sg.TabGroup([tab_group_analysis_method], selected_background_color="purple")

        # layout = [[col_analysis_sheet, col_report_sheet, col_analysis_method]]
        layout = [sg.vtop([col_analysis_sheet, col_report_sheet, col_analysis_method])]

        return layout

    def bio_method_single_point(self):
        """

        :return: A layout for the analys method settings
        :rtype: list
        """
        colours = [keys for keys in list(self.config["colours to hex"].keys())]

        single_point = sg.Frame("Single point report setup", [[
            sg.Column([
                [sg.T("Original data", relief="groove"),
                 # sg.Checkbox("use?", key="-SINGLE_ORG_USE-",
                 # default=self.plate_setup["plate_analysis_dict"]["original"]["use"])
                             ],
                [sg.Radio("Colour Well State", group_id=1, key="-SINGLE_ORG_STATE-",
                          default=self.plate_setup["plate_analysis_dict"]["original"]["state_map"]),
                 sg.Radio("Heatmap", group_id=1, key="-SINGLE_ORG_HEAT-",
                          default=self.plate_setup["plate_analysis_dict"]["original"]["heatmap"]),
                 sg.Radio("None", group_id=1, key="-SINGLE_ORG_NONE-",
                          default=self.plate_setup["plate_analysis_dict"]["original"]["none"])],
                [sg.HorizontalSeparator()],
                [sg.T("normalised data", relief="groove"),
                 # sg.Checkbox("use?", key="-SINGLE_NORM_USE-",
                 # default=self.plate_setup["plate_analysis_dict"]["normalised"]["use"])
                 ],
                [sg.Radio("Colour Well State", group_id=2, key="-SINGLE_norm_STATE-",
                          default=self.plate_setup["plate_analysis_dict"]["normalised"]["state_map"]),
                 sg.Radio("Heatmap", group_id=2, key="-SINGLE_norm_HEAT-",
                          default=self.plate_setup["plate_analysis_dict"]["normalised"]["heatmap"]),
                 sg.Radio("None", group_id=2, key="-SINGLE_norm_NONE-",
                          default=self.plate_setup["plate_analysis_dict"]["normalised"]["none"])],
                [sg.HorizontalSeparator()],
                [sg.T("PORA data", relief="groove"),
                 # sg.Checkbox("use?", key="-SINGLE_PORA_USE-",
                 # default=self.plate_setup["plate_analysis_dict"]["pora"]["use"])
                 ],
                [sg.Radio("Colour Well State", group_id=3, key="-SINGLE_PORA_STATE-",
                          default=self.plate_setup["plate_analysis_dict"]["pora"]["state_map"]),
                 sg.Radio("Heatmap", group_id=3, key="-SINGLE_PORA_HEAT-",
                          default=self.plate_setup["plate_analysis_dict"]["pora"]["heatmap"]),
                 sg.Radio("Hit Mapping", group_id=3, key="-SINGLE_PORA_HIT-",
                          default=self.plate_setup["plate_analysis_dict"]["pora"]["hit_map"]),
                 sg.Radio("None", group_id=3, key="-SINGLE_PORA_NONE-",
                          default=self.plate_setup["plate_analysis_dict"]["pora"]["none"])],
                [sg.HorizontalSeparator()],
                # [sg.T("PORA Internal data", relief="groove"),
                #  sg.Checkbox("use?", key="-SINGLE_PORA_INTERNAL_USE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_use"))],
                # [sg.Radio("Colour Well State", group_id=4, key="-SINGLE_PORA_INTERNAL_STATE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_state_map")),
                #  sg.Radio("Heatmap", group_id=4, key="-SINGLE_PORA_INTERNAL_HEAT-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_heat_map")),
                #  sg.Radio("Hit Mapping", group_id=4, key="-SINGLE_PORA_INTERNAL_HIT-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_hit_map")),
                #  sg.Radio("None", group_id=4, key="-SINGLE_PORA_INTERNAL_NONE-", default=self.config["Settings_bio"].getboolean("plate_report_plate_analysis_dict_pora_internal_none"))],
                # [sg.HorizontalSeparator()],
                # This Could be the same as the full report...
                [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
                [sg.T("Lower bound", size=10),
                 sg.InputText(key="-PLATE_PORA_LOW_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["low"]["min"]),
                 sg.InputText(key="-PLATE_PORA_LOW_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["low"]["max"])],
                [sg.T("Middle bound", size=10),
                 sg.InputText(key="-PLATE_PORA_MID_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["mid"]["min"]),
                 sg.InputText(key="-PLATE_PORA_MID_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["mid"]["max"])],
                [sg.T("Higher bound", size=10),
                 sg.InputText(key="-PLATE_PORA_HIGH_MIN_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["high"]["min"]),
                 sg.InputText(key="-PLATE_PORA_HIGH_MAX_HIT_THRESHOLD-", size=8,
                              default_text=self.plate_setup["pora_threshold"]["high"]["max"])],
                [sg.HorizontalSeparator()],
                [sg.T("Hit map colours", relief="groove")],
                [sg.ColorChooserButton("Low Colour", key="-PLATE_REPORT_HIT_LOW_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_pora_threshold_colour_low"]),
                 sg.Input(key="-PLATE_REPORT_HIT_LOW_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_low"]),

                 sg.ColorChooserButton("Mid Colour", key="-PLATE_REPORT_HIT_MID_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HIT_MID_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_pora_threshold_colour_mid"]),
                 sg.Input(key="-PLATE_REPORT_HIT_MID_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_mid"]),

                 sg.ColorChooserButton("High Colour", key="-PLATE_REPORT_HIT_HIGH_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_pora_threshold_colour_high"]),
                 sg.Input(key="-PLATE_REPORT_HIT_HIGH_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_high"])],
                [sg.HorizontalSeparator()],
                [sg.T("Heatmap settings", relief="groove")],
                [sg.ColorChooserButton("Low Colour", key="-PLATE_REPORT_HEATMAP_LOW_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HEATMAP_LOW_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_heatmap_colours_low"]),
                 sg.Input(key="-PLATE_REPORT_HEATMAP_LOW_COLOUR_TARGET-", visible=False, enable_events=True,
                          disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_low"]),

                 sg.ColorChooserButton("Mid Colour", key="-PLATE_REPORT_HEATMAP_MID_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_heatmap_colours_mid"]),
                 sg.Input(key="-PLATE_REPORT_HEATMAP_MID_COLOUR_TARGET-", visible=False, enable_events=True,
                          disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_mid"]),

                 sg.ColorChooserButton("High Colour", key="-PLATE_REPORT_HEATMAP_HIGH_COLOUR-", size=(15, None),
                                       target="-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-",
                                       button_color=self.config["Settings_bio"]
                                       ["plate_report_heatmap_colours_high"]),
                 sg.Input(key="-PLATE_REPORT_HEATMAP_HIGH_COLOUR_TARGET-", visible=False, enable_events=True,
                          disabled=True,
                          default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_high"])],


            ])
        ]])

        layout = [[single_point]]

        return layout

    def purity_ions(self):
        check_size = 10
        col_ion_pos = sg.Frame("Positive ions", [[
            sg.Column([
                [sg.Checkbox("m+3h", size=check_size, key="-MS_POS_ION_m+3h-"
                             , default=self.ms_settings["ions"]["positive"]["m+3h"]),
                 sg.Checkbox("m+2h+na", size=check_size, key="-MS_POS_ION_m+2h+na-"
                             , default=self.ms_settings["ions"]["positive"]["m+2h+na"]),
                 sg.Checkbox("m+h+2na", size=check_size, key="-MS_POS_ION_m+h+2na-"
                             , default=self.ms_settings["ions"]["positive"]["m+h+2na"]),
                 sg.Checkbox("m+3na", size=check_size, key="-MS_POS_ION_m+3na-"
                             , default=self.ms_settings["ions"]["positive"]["m+3na"]),
                 sg.Checkbox("m+2h", size=check_size, key="-MS_POS_ION_m+2h-"
                             , default=self.ms_settings["ions"]["positive"]["m+2h"]),
                 sg.Checkbox("m+h+nh4", size=check_size, key="-MS_POS_ION_m+h+nh4-"
                              , default=self.ms_settings["ions"]["positive"]["m+h+nh4"])],
                [sg.Checkbox("m+h+na", size=check_size, key="-MS_POS_ION_m+h+na-"
                             , default=self.ms_settings["ions"]["positive"]["m+h+na"]),
                 sg.Checkbox("m+h+k", size=check_size, key="-MS_POS_ION_m+h+k-"
                             , default=self.ms_settings["ions"]["positive"]["m+h+k"]),
                 sg.Checkbox("m+acn+2h", size=check_size, key="-MS_POS_ION_m+acn+2h-"
                             , default=self.ms_settings["ions"]["positive"]["m+acn+2h"]),
                 sg.Checkbox("m+2na", size=check_size, key="-MS_POS_ION_m+2na-"
                             , default=self.ms_settings["ions"]["positive"]["m+2na"]),
                 sg.Checkbox("m+2acn+2h", size=check_size, key="-MS_POS_ION_m+2acn+2h-"
                             , default=self.ms_settings["ions"]["positive"]["m+2acn+2h"]),
                 sg.Checkbox("m+3acn+2h", size=check_size, key="-MS_POS_ION_m+3acn+2h-"
                              , default=self.ms_settings["ions"]["positive"]["m+3acn+2h"])],
                [sg.Checkbox("m+h", size=check_size, key="-MS_POS_ION_m+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+h"]),
                 sg.Checkbox("m+nh4", size=check_size, key="-MS_POS_ION_m+nh4-"
                             , default=self.ms_settings["ions"]["positive"]["m+nh4"]),
                 sg.Checkbox("m+na", size=check_size, key="-MS_POS_ION_m+na-"
                             , default=self.ms_settings["ions"]["positive"]["m+na"]),
                 sg.Checkbox("m+ch3oh+h", size=check_size, key="-MS_POS_ION_m+ch3oh+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+ch3oh+h"]),
                 sg.Checkbox("m+k", size=check_size, key="-MS_POS_ION_m+k-"
                             , default=self.ms_settings["ions"]["positive"]["m+k"]),
                 sg.Checkbox("m+acn+h", size=check_size, key="-MS_POS_ION_m+acn+h-"
                              , default=self.ms_settings["ions"]["positive"]["m+acn+h"])],
                [sg.Checkbox("m+2na-h", size=check_size, key="-MS_POS_ION_m+2na-h-"
                             , default=self.ms_settings["ions"]["positive"]["m+2na-h"]),
                 sg.Checkbox("m+isoprop+h", size=check_size, key="-MS_POS_ION_m+isoprop+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+isoprop+h"]),
                 sg.Checkbox("m+acn+na", size=check_size, key="-MS_POS_ION_m+acn+na-"
                             , default=self.ms_settings["ions"]["positive"]["m+acn+na"]),
                 sg.Checkbox("m+2k+h", size=check_size, key="-MS_POS_ION_m+2k+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+2k+h"]),
                 sg.Checkbox("m+dmso+h", size=check_size, key="-MS_POS_ION_m+dmso+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+dmso+h"]),
                 sg.Checkbox("m+2acn+h", size=check_size, key="-MS_POS_ION_m+2acn+h-"
                              , default=self.ms_settings["ions"]["positive"]["m+2acn+h"])],
                [sg.Checkbox("m+isoprop+na+h", size=check_size, key="-MS_POS_ION_m+isoprop+na+h-"
                             , default=self.ms_settings["ions"]["positive"]["m+isoprop+na+h"]),
                 sg.Checkbox("2m+h", size=check_size, key="-MS_POS_ION_2m+h-"
                             , default=self.ms_settings["ions"]["positive"]["2m+h"]),
                 sg.Checkbox("2m+nh4", size=check_size, key="-MS_POS_ION_2m+nh4-"
                             , default=self.ms_settings["ions"]["positive"]["2m+nh4"]),
                 sg.Checkbox("2m+na", size=check_size, key="-MS_POS_ION_2m+na-"
                             , default=self.ms_settings["ions"]["positive"]["2m+na"]),
                 sg.Checkbox("2m+3h2o+2h", size=check_size, key="-MS_POS_ION_2m+3h2o+2h-"
                             , default=self.ms_settings["ions"]["positive"]["2m+3h2o+2h"]),
                 sg.Checkbox("2m+k", size=check_size, key="-MS_POS_ION_2m+k-"
                             , default=self.ms_settings["ions"]["positive"]["2m+k"])],
                [sg.Checkbox("2m+acn+h", size=check_size, key="-MS_POS_ION_2m+acn+h-"
                             , default=self.ms_settings["ions"]["positive"]["2m+acn+h"]),
                 sg.Checkbox("2m+acn+na", size=check_size, key="-MS_POS_ION_2m+acn+na-"
                             , default=self.ms_settings["ions"]["positive"]["2m+acn+na"])],
            ])
        ]])

        col_ion_neg = sg.Frame("Negative Ions", [[
            sg.Column([
                [sg.Checkbox("m-3h", size=check_size, key="-MS_NEG_ION_m-3h-"
                             , default=self.ms_settings["ions"]["negative"]["m-3h"]),
                    sg.Checkbox("m-2h", size=check_size, key="-MS_NEG_ION_m-2h-"
                                , default=self.ms_settings["ions"]["negative"]["m-2h"]),
                    sg.Checkbox("m-h2o-h", size=check_size, key="-MS_NEG_ION_m-h2o-h-"
                                , default=self.ms_settings["ions"]["negative"]["m-h2o-h"]),
                    sg.Checkbox("m-h", size=check_size, key="-MS_NEG_ION_m-h-"
                                , default=self.ms_settings["ions"]["negative"]["m-h"]),
                    sg.Checkbox("m+na-2h", size=check_size, key="-MS_NEG_ION_m+na-2h-"
                                , default=self.ms_settings["ions"]["negative"]["m+na-2h"]),
                    sg.Checkbox("m+cl", size=check_size, key="-MS_NEG_ION_m+cl-"
                                , default=self.ms_settings["ions"]["negative"]["m+cl"])],
                [sg.Checkbox("m+k-2h", size=check_size, key="-MS_NEG_ION_m+k-2h-"
                             , default=self.ms_settings["ions"]["negative"]["m+k-2h"]),
                    sg.Checkbox("m+fa-h", size=check_size, key="-MS_NEG_ION_m+fa-h-"
                                , default=self.ms_settings["ions"]["negative"]["m+fa-h"]),
                    sg.Checkbox("m+hac-h", size=check_size, key="-MS_NEG_ION_m+hac-h-"
                                , default=self.ms_settings["ions"]["negative"]["m+hac-h"]),
                    sg.Checkbox("m+br", size=check_size, key="-MS_NEG_ION_m+br-"
                                , default=self.ms_settings["ions"]["negative"]["m+br"]),
                    sg.Checkbox("m+tfa-h", size=check_size, key="-MS_NEG_ION_m+tfa-h-"
                                , default=self.ms_settings["ions"]["negative"]["m+tfa-h"]),
                    sg.Checkbox("2m-h", size=check_size, key="-MS_NEG_ION_2m-h-"
                                , default=self.ms_settings["ions"]["negative"]["2m-h"])],
                [sg.Checkbox("2m+fa-h", size=check_size, key="-MS_NEG_ION_2m+fa-h-"
                             , default=self.ms_settings["ions"]["negative"]["2m+fa-h"] ),
                    sg.Checkbox("2m+hac-h", size=check_size, key="-MS_NEG_ION_2m+hac-h-"
                                , default=self.ms_settings["ions"]["negative"]["2m+hac-h"]),
                    sg.Checkbox("3m-h", size=check_size, key="-MS_NEG_ION_3m-h-"
                                , default=self.ms_settings["ions"]["negative"]["3m-h"])]
            ])
        ]])

        layout = [sg.vtop([col_ion_pos, col_ion_neg])]

        return layout

    def plate_layout(self):

        col_colours = sg.Frame("Colours", [[
            sg.Column([
                [sg.ColorChooserButton("Sample", key="-PLATE_LAYOUT_COLOUR_SAMPLE-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["sample"]
                      , key="-PLATE_LAYOUT_COLOUR_SAMPLE_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_SAMPLE_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["sample"])],

                [sg.ColorChooserButton("Blank", key="-PLATE_LAYOUT_COLOUR_BLANK-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_BLANK_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["blank"]
                      , key="-PLATE_LAYOUT_COLOUR_BLANK_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_BLANK_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["blank"])],

                [sg.ColorChooserButton("Max", key="-PLATE_LAYOUT_COLOUR_MAX-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_MAX_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["max"]
                      , key="-PLATE_LAYOUT_COLOUR_MAX_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_MAX_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["max"])],

                [sg.ColorChooserButton("Minimum", key="-PLATE_LAYOUT_COLOUR_MINIMUM-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["minimum"]
                      , key="-PLATE_LAYOUT_COLOUR_MINIMUM_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_MINIMUM_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["minimum"])],

                [sg.ColorChooserButton("Positive Control", key="-PLATE_LAYOUT_COLOUR_POSITIVE-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["positive"]
                      , key="-PLATE_LAYOUT_COLOUR_POSITIVE_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_POSITIVE_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["positive"])],

                [sg.ColorChooserButton("Negative Control", key="-PLATE_LAYOUT_COLOUR_NEGATIVE-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["negative"]
                      , key="-PLATE_LAYOUT_COLOUR_NEGATIVE_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_NEGATIVE_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["negative"])],

                [sg.ColorChooserButton("Empty", key="-PLATE_LAYOUT_COLOUR_EMPTY-", size=(15, None),
                                       target="-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-"),
                 sg.T(background_color=self.config["plate_colouring"]["empty"]
                      , key="-PLATE_LAYOUT_COLOUR_EMPTY_BOX-", size=8),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_EMPTY_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text=self.config["plate_colouring"]["empty"])]
            ])
        ]])

        layout = [[col_colours]]
        return layout

    def tab_groups(self):
        """

        :return: The tab layout for the settings menu
        :rtype: list
        """
        sg.theme(self.config["GUI"]["theme"])

        sg.set_options(font=("Courier New", 10))
        # text_width = 50
        #
        headings = ["Bio Plate Report", "Bio Final Report", "MS Ions", "Plate Layout"]
        text_width = max(map(len, headings))
        tab_plate_report = sg.Tab("Bio Plate Report".center(text_width), self.settings_bio_plate_report(), expand_x=True, expand_y=True)
        tab_full_report = sg.Tab("Bio Final Report".center(text_width), self.settings_bio_final_report(), expand_x=True, expand_y=True)
        tab_ion = sg.Tab("MS Ions".center(text_width), self.purity_ions(), expand_x=True, expand_y=True)
        tab_plate_layout = sg.Tab("Plate Layout".center(text_width), self.plate_layout(), expand_x=True, expand_y=True)

        tab_group_tables = [tab_plate_report, tab_full_report, tab_ion, tab_plate_layout]

        buttons = [sg.B("Ok", key="-BIO_SETTINGS_OK-"), sg.B("Cancel", key="-CANCEL-"),
                   sg.B("set Default", key="-SETTINGS_DEFAULT-"),
                   sg.B("Load Default", key="-SETTINGS_LOAD_DEFAULT-", enable_events=True)]

        tab_layout = [[sg.TabGroup([tab_group_tables], tab_location="lefttop", selected_background_color="purple",
                                   enable_events=True, key="-TAB_GROUPS-")], buttons]

        return tab_layout

    def purity_tab_groups(self):
        ...

    def settings_window(self, final_setup, plate_setup, ms_settings):
        """

        :return: The window for the data
        :rtype: PySimpleGUI.PySimpleGUI.Window
        """

        self.final_setup = final_setup
        self.plate_setup = plate_setup
        self.ms_settings = ms_settings

        tab_layout = self.tab_groups()

        return sg.Window("Settings", tab_layout)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    sl = GUISettingsLayout(config)
    sl.test_window()

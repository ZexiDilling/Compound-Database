import PySimpleGUI as sg
import configparser


class GUISettingsLayout:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def settings_bio_final_report():
        calc_col = sg.Frame("Calculations", [[
            sg.Column([
                [sg.T("What well status to include calculations for (avg, stdiv...)")],
                [sg.HorizontalSeparator()],
                [sg.T("Original data", relief="groove"), sg.Checkbox("Include?", key="-FINAL_BIO_CAL_ORG-")],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_ORG_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_ORG_MIN-"),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_ORG_MAX-"),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_ORG_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_ORG_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_ORG_POS_C-"),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_ORG_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.T("Normalized data", relief="groove"), sg.Checkbox("Include?", key="-FINAL_BIO_CAL_NORM-")],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_NORM_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_NORM_MIN-", default=True),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_NORM_MAX-", default=True),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_NORM_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_NORM_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_NORM_POS_C-"),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_NORM_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.T("PORA data", relief="groove"), sg.Checkbox("Include?", key="-FINAL_BIO_CAL_PORA-")],
                [sg.Checkbox("Sample", key="-FINAL_BIO_CALC_PORA_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_CALC_PORA_MIN-"),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_CALC_PORA_MAX-"),
                 sg.Checkbox("Empty", key="-FINAL_BIO_CALC_PORA_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_CALC_PORA_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_CALC_PORA_POS_C-"),
                 sg.Checkbox("Blank", key="-FINAL_BIO_CALC_PORA_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Z-prime", key="-FINAL_BIO_Z_PRIME-")]

            ])
        ]])

        well_col = sg.Frame("Well report", [[
            sg.Column([
                [sg.T("What wells to include in the final report, depending on status and analysed method")],
                [sg.HorizontalSeparator()],
                [sg.T("What tables to include wells for:", relief="groove")],
                [sg.Checkbox("Original", key="-FINAL_BIO_ORG-"), sg.Checkbox("normalized", key="-FINAL_BIO_NORM-"),
                 sg.Checkbox("Pora", key="-FINAL_BIO_PORA-", default=True)],
                [sg.HorizontalSeparator()],
                [sg.T("What state to include wells for:", relief="groove")],
                [sg.Checkbox("Sample", key="-FINAL_BIO_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-FINAL_BIO_MIN-", default=True),
                 sg.Checkbox("Maximum", key="-FINAL_BIO_MAX-", default=True),
                 sg.Checkbox("Empty", key="-FINAL_BIO_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-FINAL_BIO_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-FINAL_BIO_POS_C-"),
                 sg.Checkbox("Blank", key="-FINAL_BIO_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
                [sg.T("Lower bound", size=10),
                 sg.InputText(key="-PORA_LOW_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PORA_LOW_MAX_HIT_THRESHOLD-", size=8)],
                [sg.T("Middle bound", size=10),
                 sg.InputText(key="-PORA_MID_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PORA_MID_MAX_HIT_THRESHOLD-", size=8)],
                [sg.T("Higher bound", size=10),
                 sg.InputText(key="-PORA_HIGH_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PORA_HIGH_MAX_HIT_THRESHOLD-", size=8)]
            ])
        ]])

        layout = [sg.vtop([calc_col, well_col])]

        return layout

    def settings_bio_plate_report(self):
        colours = [keys for keys in list(self.config["colours to hex"].keys())]
        col_report = sg.Frame("Report setup", [[
            sg.Column([
                [sg.T("Report setup per reading:", relief="groove")],
                [sg.HorizontalSeparator()],
                [sg.T("What well-state to include for the final report")],
                [sg.Checkbox("Sample", key="-BIO_SAMPLE-", default=True), sg.Checkbox("Minimum", key="-BIO_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_MAX-"), sg.Checkbox("Empty", key="-BIO_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_NEG_C-"), sg.Checkbox("Positive Control", key="-BIO_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.T("What analysed method to include wells from")],
                [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG-"),
                 sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM-"),
                 sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA-"),
                 sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL-")],
                [sg.HorizontalSeparator()],
                [sg.T("What calculation to include and for witch analysed method")],
                [sg.T("Will only take in samples and method that have been used")],
                [sg.Checkbox("Z prime", key="-BIO_Z_PRIME-", default=True)],
                [sg.Checkbox("Original", key="-BIO_PLATE_REPORT_ORG_CALC-"),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_ORG_AVG-"),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_ORG_STDEV-")],
                [sg.Checkbox("Sample", key="-BIO_CAL_ORG_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-BIO_CAL_ORG_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_CAL_ORG_MAX-"),
                 sg.Checkbox("Empty", key="-BIO_CAL_ORG_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_ORG_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_ORG_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_CAL_ORG_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Normalised", key="-BIO_PLATE_REPORT_NORM_CALC-"),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_NORM_AVG-"),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_NORM_STDEV-")],
                [sg.Checkbox("Sample", key="-BIO_CAL_NORM_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-BIO_CAL_NORM_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_CAL_NORM_MAX-"),
                 sg.Checkbox("Empty", key="-BIO_CAL_NORM_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_NORM_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_NORM_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_CAL_NORM_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Pora", key="-BIO_PLATE_REPORT_PORA_CAL-"),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_AVG-"),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_STDEV-")],
                [sg.Checkbox("Sample", key="-BIO_CAL_PORA_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-BIO_CAL_PORA_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_CAL_PORA_MAX-"),
                 sg.Checkbox("Empty", key="-BIO_CAL_PORA_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_CAL_PORA_BLANK-")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Pora Internal", key="-BIO_PLATE_REPORT_PORA_INTERNAL_CAL-"),
                 sg.Checkbox("avg", key="-BIO_PLATE_CAL_PORA_INT_AVG-"),
                 sg.Checkbox("stdev", key="-BIO_PLATE_CAL_PORA_INT_STDEV-")],
                [sg.Checkbox("Sample", key="-BIO_CAL_PORA_INT_SAMPLE-"),
                 sg.Checkbox("Minimum", key="-BIO_CAL_PORA_INT_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_CAL_PORA_INT_MAX-"),
                 sg.Checkbox("Empty", key="-BIO_CAL_PORA_INT_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_CAL_PORA_INT_NEG_C-"),
                 sg.Checkbox("Positive Control", key="-BIO_CAL_PORA_INT_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_CAL_PORA_INT_BLANK-")],
                [sg.HorizontalSeparator()],
            ])
        ]], expand_y=True)

        single_point = sg.Frame("Single point report setup", [[
            sg.Column([
                [sg.T("Original data", relief="groove"),
                 sg.Checkbox("use?", key="-SINGLE_ORG_USE-", default=True)],
                [sg.Radio("Colour Well State", group_id=1, key="-SINGLE_ORG_STATE-", default=True),
                 sg.Radio("Heatmap", group_id=1, key="-SINGLE_ORG_HEAT-"),
                 sg.Radio("None", group_id=1, key="-SINGLE_ORG_NONE-")],
                [sg.HorizontalSeparator()],
                [sg.T("normalised data", relief="groove"),
                 sg.Checkbox("use?", key="-SINGLE_NORM_USE-", default=True)],
                [sg.Radio("Colour Well State", group_id=2, key="-SINGLE_norm_STATE-"),
                 sg.Radio("Heatmap", group_id=2, key="-SINGLE_norm_HEAT-", default=True),
                 sg.Radio("None", group_id=2, key="-SINGLE_norm_NONE-")],
                [sg.HorizontalSeparator()],
                [sg.T("PORA data", relief="groove"),
                 sg.Checkbox("use?", key="-SINGLE_PORA_USE-", default=True)],
                [sg.Radio("Colour Well State", group_id=3, key="-SINGLE_PORA_STATE-"),
                 sg.Radio("Heatmap", group_id=3, key="-SINGLE_PORA_HEAT-"),
                 sg.Radio("Hit Mapping", group_id=3, key="-SINGLE_PORA_HIT-", default=True),
                 sg.Radio("None", group_id=3, key="-SINGLE_PORA_NONE-")],
                [sg.HorizontalSeparator()],
                [sg.T("PORA Internal data", relief="groove"),
                 sg.Checkbox("use?", key="-SINGLE_PORA_INTERNAL_USE-", default=True)],
                [sg.Radio("Colour Well State", group_id=4, key="-SINGLE_PORA_INTERNAL_STATE-"),
                 sg.Radio("Heatmap", group_id=4, key="-SINGLE_PORA_INTERNAL_HEAT-"),
                 sg.Radio("Hit Mapping", group_id=4, key="-SINGLE_PORA_INTERNAL_HIT-", default=True),
                 sg.Radio("None", group_id=4, key="-SINGLE_PORA_INTERNAL_NONE-")],
                [sg.HorizontalSeparator()],
                # This Could be the same as the full report...
                [sg.Text("Hit Threshold", relief="groove", size=10), sg.T("Minimum", size=7), sg.T("Maximum", size=8)],
                [sg.T("Lower bound", size=10),
                 sg.InputText(key="-PLATE_PORA_LOW_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PLATE_PORA_LOW_MAX_HIT_THRESHOLD-", size=8)],
                [sg.T("Middle bound", size=10),
                 sg.InputText(key="-PLATE_PORA_MID_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PLATE_PORA_MID_MAX_HIT_THRESHOLD-", size=8)],
                [sg.T("Higher bound", size=10),
                 sg.InputText(key="-PLATE_PORA_HIGH_MIN_HIT_THRESHOLD-", size=8),
                 sg.InputText(key="-PLATE_PORA_HIGH_MAX_HIT_THRESHOLD-", size=8)],
                [sg.HorizontalSeparator()],
                [sg.T("Heatmap settings")],
                [sg.Text("start Colour:", size=15), sg.Text("Mid Colour:", size=15), sg.Text("End Colour:", size=15)],
                [sg.DropDown(colours, key="-HEAT_START-", size=15, default_value=colours[0]),
                 sg.DropDown(colours, key="-HEAT_MID-", size=15, default_value=colours[13]),
                 sg.DropDown(colours, key="-HEAT_END-", size=15, default_value=colours[4])],

            ])
        ]])

        layout = [sg.vtop([col_report, single_point])]

        return layout

    def bio_tab_groups(self):
        sg.theme(self.config["GUI"]["theme"])
        tab_plate_report = sg.Tab("Plate Report", self.settings_bio_plate_report())
        tab_full_report = sg.Tab("Final Report", self.settings_bio_final_report())

        tab_group_tables = [tab_plate_report, tab_full_report]

        buttons = [sg.B("Ok", key="-BIO_SETTINGS_OK-"), sg.B("Cancel", key="-CANCEL-"),
                   sg.B("set default", key="-BIO_SETTINGS_DEFAULT-")]

        return [[sg.TabGroup([tab_group_tables], tab_location="left", selected_background_color="purple")],
                buttons]

    def bio_settings_window(self):
        layout = self.bio_tab_groups()

        return sg.Window("Settings", layout)

    def test_window(self):
        window = self.bio_settings_window()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "-CANCEL-":
                break


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    sl = GUISettingsLayout(config)
    sl.test_window()

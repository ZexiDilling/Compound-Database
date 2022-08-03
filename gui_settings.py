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
        col_report = sg.Frame("Report setup - NOT WORKING ATM, TAKES DATA FROM MAIN!", [[
            sg.Column([
                [sg.T("Data for each excel file:", relief="groove")],
                [sg.Checkbox("Sample", key="-BIO_SAMPLE-", default=True), sg.Checkbox("Minimum", key="-BIO_MIN-"),
                 sg.Checkbox("Maximum", key="-BIO_MAX-"), sg.Checkbox("Empty", key="-BIO_EMPTY-")],
                [sg.Checkbox("Negative Control", key="-BIO_NEG_C-"), sg.Checkbox("Positive Control", key="-BIO_POS_C-"),
                 sg.Checkbox("Blank", key="-BIO_BLANK-"), sg.Checkbox("Z prime", key="-BIO_Z-PRIME-")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("heatmap", key="-BIO_HEATMAP-")],
                [sg.Text("start Colour:", size=15),
                 sg.DropDown(colours, key="-HEAT_START-", size=15,
                             default_value=colours[0])],
                [sg.Text("Mid Colour:", size=15),
                 sg.DropDown(colours, key="-HEAT_MID-", size=15,
                             default_value=colours[13])],
                [sg.Text("End Colour:", size=15),
                 sg.DropDown(colours, key="-HEAT_END-", size=15,
                             default_value=colours[4])],
                [sg.HorizontalSeparator],
                [sg.Checkbox("State colours", key="-BIO_STATE-")],
            ])


        ]], expand_y=True)

        layout = [[col_report]]

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

    sl = SettingsLayout(config)
    sl.window()

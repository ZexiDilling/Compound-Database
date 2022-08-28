import PySimpleGUI as sg
from info import matrix_header


class GUILayout:
    def __init__(self, config, plate_list):
        self.config = config
        self.standard_size = 20
        self.button_height = 1
        self.plate_list = plate_list

    @staticmethod
    def menu_top():
        """
        :return: The layout for the top menu
        :rtype: list
        """
        menu_top_def = [
            ["&File", ["&Open    Ctrl-O", "&Save    Ctrl-S", "---", '&Properties',  "&Exit", ]],
            ["&Edit", ["Paste", ["Special", "Normal", ], "Undo"], ],
            ["&Help", ["Info", "About..."]],
            ]
        layout = [[sg.Menu(menu_top_def)]]
        return layout

    @staticmethod
    def menu_mouse():
        """

        :return: The mouse menu
        :rtype: list
        """
        menu_mouse_def = [['File', ['Open', 'Save', 'Exit', ]],
                    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                    ['Help', 'About...'], ]

        layout = [[sg.ButtonMenu("place_holder", menu_mouse_def, key="-RMB-")]]

        return layout, menu_mouse_def

    def setup_1_search(self):
        """

        :return: A layour for the search-module in the top box
        :rtype: list
        """
        ac = ["Academic", "Commercial"]
        # origin = [self.config["database_specific_commercial"][values] for values in self.config["database_specific_commercial"]]
        subs_search_methods = list(self.config["structure_search_methode"].keys())
        plate_production = ["Mother Plates", "Daughter Plates"]

        col_1 = sg.Frame("Search", [[
            sg.Column([
                [sg.T("Out put folder"),
                 sg.FolderBrowse(key="-SEARCH_OUTPUT_FOLDER-", target="-SEARCH_OUTPUT_FOLDER_TARGET-"
                                 , initial_folder="output_files")],
                [sg.Text(key="-SEARCH_OUTPUT_FOLDER_TARGET-", size=50)],
                [sg.Listbox(values=ac, key="-SEARCH_AC-", enable_events=True, size=(10, 5),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE),
                 sg.Listbox([], key="-SEARCH_ORIGIN-", size=(10, 5), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                [sg.Checkbox(text="Ignore plated compounds?", key="-SEARCH_IGNORE_PLATED_COMPOUNDS-")],
                [sg.Text("Amount of Plates", size=self.standard_size),
                 sg.InputText(key="-SEARCH_PLATE_AMOUNT-", size=10),
                 sg.Checkbox("All", key="-SEARCH_PLATE_AMOUNT_ALL-")],
                [sg.Text("Transferee vol:", size=self.standard_size),
                 sg.InputText(key="-SEARCH_TRANS_VOL-", size=10),
                 sg.Checkbox("Ignore volume", key="-SEARCH_IGNORE_VOLUME-")],
                [sg.Text("Plate Production"),
                 sg.DropDown(plate_production, key="-SEARCH_PLATE_PRODUCTION-", default_value=plate_production[0],
                             enable_events=True),
                 sg.DropDown(sorted(self.plate_list), key="-SEARCH_PLATE_LAYOUT-", disabled=True, enable_events=True),
                 sg.T("Samples per plate:"), sg.Input("384", key="-SEARCH_PLATE_LAYOUT_SAMPLE_AMOUNT-", size=5,
                                                      readonly=True, disabled_readonly_text_color="#FFFFFF",
                                                      disabled_readonly_background_color="#4D4D4D")]
            ])
        ]])

        col_sub_search = sg.Frame("Structure Search", [[
            sg.Column([
                [sg.Checkbox(text="Structure Search", key="-SUB_SEARCH-")],
                [sg.Text("Smiles", size=self.standard_size), sg.InputText(key="-SUB_SEARCH_SMILES-", size=self.standard_size),
                 sg.Button("Draw molecule", key="-SUB_SEARCH_DRAW_MOL-")],
                [sg.Text("Search Method", size=self.standard_size),
                 sg.DropDown(subs_search_methods, key="-SUB_SEARCH_METHOD-", default_value=subs_search_methods[0],
                             enable_events=True)],
                [sg.Text("Similarity Threshold", size=self.standard_size),
                 sg.InputText(key="-SUB_SEARCH_THRESHOLD-", default_text=0, size=self.standard_size)],
                [sg.HorizontalSeparator()],
                [sg.Text("Morgan specific options", key="-SUB_SEARCH_MORGAN_OPTIONS-", visible=False)],
                [sg.Checkbox(text="chirality", key="-SUB_SEARCH_MORGAN_CHIRALITY-", visible=False),
                 sg.Checkbox(text="Features", key="-SUB_SEARCH_MORGAN_FEATURES-", visible=False)],
                [sg.Text("n bits", key="-SUB_SEARCH_BITS_TEXT-", size=self.standard_size, visible=False),
                 sg.InputText(key="-SUB_SEARCH_MORGAN_BITS-", size=self.standard_size, visible=False)],
                [sg.Text("bound range", key="-SUB_SEARCH_BOUND_TEXT-", size=self.standard_size, visible=False),
                 sg.InputText(key="-SUB_SEARCH_MORGAN_RANGE-", size=self.standard_size, visible=False)],
            ])
        ]])

        layout = [sg.vtop([col_1,  col_sub_search]),
                  [sg.Checkbox("All compounds", key="-SEARCH_ALL_COMPOUNDS-", enable_events=True),
                   # sg.Checkbox("All Non-plated Compounds", key="-SEACH_ALL_NON_PLATED-", enable_events=True)
                   ]]

        return layout

    def setup_1_bio(self):
        """

        :return: A layour for the bio-module in the top box
        :rtype: list
        """

        # maybe make it a config file. and update the config file when new method are added ?
        analyse_type = ["single point"]
        responsible = [keys for keys in list(self.config["Responsible"].keys())]

        # Colours for the heatmap, if added back in
        # colours = [keys for keys in list(self.config["colours to hex"].keys())]

        sample_type = ["single point", "duplicate", "triplicate"]

        col_bio_analysis = sg.Frame("Analyse setup", [[
            sg.Column([
                [sg.FolderBrowse(button_text="Import Folder", key="-BIO_IMPORT_FOLDER-", target="-BIO_IMPORT_TARGET-")],
                [sg.Text(key="-BIO_IMPORT_TARGET-", size=self.standard_size*2)],
                [sg.FolderBrowse(button_text="Export Folder", key="-BIO_EXPORT_FOLDER-", target="-BIO_EXPORT_TARGET-")],
                [sg.Text(key="-BIO_EXPORT_TARGET-", size=self.standard_size*2)],
                [sg.Text("Plate Layout", size=self.standard_size),
                 sg.DropDown(sorted(self.plate_list), key="-BIO_PLATE_LAYOUT-", enable_events=True,
                             size=self.standard_size)],
                [sg.Text("Analyse Method", size=self.standard_size),
                 sg.DropDown(analyse_type, key="-BIO_ANALYSE_TYPE-", size=self.standard_size, enable_events=True,
                             default_value=analyse_type[0])],
                [sg.Text("Sample Type (Not working)", size=self.standard_size),
                 sg.DropDown(sample_type, key="-BIO_SAMPLE_TYPE-", default_value=sample_type[0],
                             size=self.standard_size, enable_events=True)],
                [sg.T("Sample Type:"),
                 sg.Radio("Use Layout", group_id="-BIO_INFO_SAMPLE_TYPE_RADIO-",
                          key="-BIO_INFO_SAMPLE_TYPE_RADIO_LAYOUT-"),
                 sg.Radio("Use Sample ID", group_id="-BIO_INFO_SAMPLE_TYPE_RADIO-",
                          key="-BIO_INFO_SAMPLE_TYPE_RADIO_ID-")],
                # [sg.Checkbox("heatmap", key="-BIO_HEATMAP-")],
                # [sg.Text("start Colour:", size=self.standard_size),
                #  sg.DropDown(colours, key="-HEAT_START-", size=self.standard_size,
                #              default_value=colours[0])],
                # [sg.Text("Mid Colour:", size=self.standard_size),
                #  sg.DropDown(colours, key="-HEAT_MID-", size=self.standard_size,
                #              default_value=colours[13])],
                # [sg.Text("End Colour:", size=self.standard_size),
                #  sg.DropDown(colours, key="-HEAT_END-", size=self.standard_size,
                #              default_value=colours[4])],
                # [sg.Checkbox("State colours", key="-BIO_STATE-")],
                [sg.Button("Export", key="-EXPORT_BIO-"), sg.Push(),
                 sg.Button("Send to Info", key="-BIO_SEND_TO_INFO-")]
            ])
        ]])

        col_extra = sg.Frame("Extra Settings", [[
            sg.Column([

                [sg.Checkbox("Combined Report ", key="-BIO_COMBINED_REPORT-", default=False, enable_events=True)
                 , sg.Push(), sg.B("Report Settings", key="-BIO_REPORT_SETTINGS-")],
                [sg.Checkbox("Compound Related Data", key="-BIO_COMPOUND_DATA-", enable_events=True),
                 sg.Checkbox("Add To Database", key="-BIO_EXPERIMENT_ADD_TO_DATABASE-", enable_events=True)],
                [sg.Checkbox("Add Compound Info To Final Report", key="-BIO_FINAL_REPORT_ADD_COMPOUNDS-")],
                [sg.T("Report Name", size=12), sg.T("Assay Name", size=14)],
                [sg.InputText(key="-FINAL_BIO_NAME-", size=14), sg.InputText(key="-BIO_ASSAY_NAME-", size=14)],
                [sg.T("Responsible:", size=12),
                 sg.DropDown(responsible, key="-BIO_RESPONSIBLE-", size=14)],
                [sg.FileBrowse("Import Sample List", key="-BIO_SAMPLE_LIST-", target="-BIO_SAMPLE_LIST_TARGET-")],
                [sg.T(key="-BIO_SAMPLE_LIST_TARGET-")]
            ])
        ]])

        col_graph = sg.Frame("Plate Layout", [[
            sg.Column([
                [sg.Graph(canvas_size=(250, 175), graph_bottom_left=(0, 0), graph_top_right=(250, 175),
                          background_color='grey', key="-BIO_CANVAS-", enable_events=False, drag_submits=False,
                          motion_events=False)],
                [sg.Text("Sample:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["sample"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_SAMPLE-", relief="groove")],
                [sg.Text("Blank:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["blank"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_BLANK-", relief="groove")],
                [sg.Text("Maximum:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["max"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_NAX-", relief="groove")],
                [sg.Text("Minimum:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["minimum"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_MINIMUM-", relief="groove")],
                [sg.Text("Positive Control:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["positive"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_POSITIVE-", relief="groove")],
                [sg.Text("Negative Control:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["negative"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_NEGATIVE-", relief="groove")],
                [sg.Text("Empty:", size=self.standard_size),
                 sg.T(background_color=self.config["plate_colouring"]["empty"], size=10,
                      key="-BIO_PLATE_LAYOUT_COLOUR_BOX_EMPTY-", relief="groove")],
            ])
        ]])


        layout = [sg.vtop([col_bio_analysis, col_extra, col_graph])]

        return layout

    def setup_1_purity(self):
        """

        :return: A layour for the purity-module in the top box
        :rtype: list
        """
        ms_mode = ["Positive", "Negative"]
        responsible = [keys for keys in list(self.config["Responsible"].keys())]

        col_ms_buttons = sg.Frame("bah", [[
            sg.Column([
                [sg.FolderBrowse(button_text="Import Folder", key="-PURITY_DATA_IMPORT_FOLDER-",
                                 target="-PURITY_DATA_IMPORT_TARGET-")],
                [sg.Text(key="-PURITY_DATA_IMPORT_TARGET-", size=self.standard_size * 2)],
                [sg.FolderBrowse(button_text="Export Folder", key="-PURITY_EXPORT_FOLDER-",
                                 target="-PURITY_DATA_EXPORT_TARGET-")],
                [sg.Text(key="-PURITY_DATA_EXPORT_TARGET-", size=self.standard_size * 2)],
                [sg.T("Responsible"), sg.DropDown(responsible, key="-PURITY_DATA_RESPONSIBLE-")],
                [sg.Checkbox("Compound data?", key="-PURITY_DATA_USE_COMPOUNDS-"),
                 sg.Checkbox("Add to Database", key="-PURITY_DATA_ADD_TO_DATABASE-")],
                [sg.B("Generate Report", key="-PURITY_DATA_REPORT-"),
                 sg.B("Import", key="-PURITY_DATA_IMPORT-"), sg.Push(),
                 sg.B("Send to Info", key="-PURITY_DATA_SEND_TO_INFO-")]
            ])
        ]])

        col_ms_settings = sg.Frame("MS setup", [[
            sg.Column([
                [sg.Push(), sg.B("Advanced setting", key="-PURITY_ADVANCED_SETTINGS-")],
                [sg.Checkbox("UV one", key="-UPDATE_UV-")],
                [sg.T("UV wavelength", size=self.standard_size),
                 sg.InputText(key="-PURITY_DATA_UV_WAVE-",
                              default_text=int(self.config["MS_default"]["uv_wavelength"]), size=10)],
                [sg.HorizontalSeparator()],
                [sg.Text("UV threshold", size=self.standard_size),
                 sg.InputText(key="-PURITY_DATA_UV_THRESHOLD-",
                              default_text=int(self.config["MS_default"]["uv_threshold"]), size=10)],
                [sg.Text("Solvent peak retention time", size=self.standard_size),
                 sg.InputText(key="-PURITY_DATA_RT_SOLVENT-",
                              default_text=float(self.config["MS_default"]["rt_solvent"]), size=10)],
                [sg.HorizontalSeparator()],
                [sg.DropDown(ms_mode, key="-PURITY_DATA_MS_MODE-", default_value=ms_mode[0])],
                [sg.Text("Delta MS", size=self.standard_size),
                 sg.InputText(key="-PURITY_DATA_MS_DELTA-",
                              default_text=float(self.config["MS_default"]["rt_solvent"]), size=10)],
                [sg.Text("MS threshold", size=self.standard_size),
                 sg.InputText(key="-PURITY_DATA_MS_THRESHOLD-",
                              default_text=int(self.config["MS_default"]["ms_threshold"]), size=10)]
            ])
        ]])

        layout = [sg.vtop([col_ms_buttons, col_ms_settings])]

        return layout

    def setup_1_plate_layout(self):
        """

        :return: A layour for the plate-module in the top box
        :rtype: list
        """
        color_select = {}
        for keys in list(self.config["plate_colouring"].keys()):
            color_select[keys] = self.config["plate_colouring"][keys]

        plate_type = ["plate_96", "plate_384", "plate_1536"]
        sample_type = ["single point", "duplicate", "triplicate"]


        col_graph = sg.Frame("Plate Layout", [[
            sg.Column([
                [sg.Graph(canvas_size=(500, 350), graph_bottom_left=(0, 0), graph_top_right=(500, 350),
                      background_color='grey', key="-CANVAS-", enable_events=True, drag_submits=True,
                      motion_events=True)],
                [sg.DropDown(values=plate_type, default_value=plate_type[1], key="-PLATE-"),
                 sg.B("Draw Plate", key="-DRAW-"),
                 sg.Checkbox("Active move+", key="-RECT_BIO_MOVE-", default=True, enable_events=True),
                 # sg.B("Add sample layout", key="-DRAW_SAMPLE_LAYOUT-"),
                 sg.Text(key="-INFO-")]
            ])
        ]])

        col_options = sg.Frame("Options", [[
            sg.Column([
                [sg.Text("Choose what clicking a figure does", enable_events=True)],
                [sg.Radio(f"Select Sample", 1, key="-RECT_SAMPLES-", size=15, enable_events=True,
                          default=True),
                 sg.T(background_color=self.config["plate_colouring"]["sample"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_SAMPLE-", relief="groove"),
                 sg.DropDown(sample_type, key="-RECT_SAMPLE_TYPE-", default_value=sample_type[0])],
                [sg.Radio(f"Select Blank", 1, key="-RECT_BLANK-", size=15, enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["blank"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_BLANK-", relief="groove")],
                [sg.Radio(f"Select Max Signal", 1, key="-RECT_MAX-", size=15, enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["max"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_NAX-", relief="groove")],
                [sg.Radio(f"Select Minimum Signal", 1, key="-RECT_MIN-", size=15,
                          enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["minimum"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_MINIMUM-", relief="groove")],
                [sg.Radio(f"Select Positive Control", 1, key="-RECT_POS-", size=15,
                          enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["positive"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_POSITIVE-", relief="groove")],
                [sg.Radio(f"Select Negative Control", 1, key="-RECT_NEG-", size=15,
                          enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["negative"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_NEGATIVE-", relief="groove")],
                [sg.Radio(f"Select Empty", 1, key="-RECT_EMPTY-", size=15, enable_events=True),
                 sg.T(background_color=self.config["plate_colouring"]["empty"], size=10,
                      key="-PLATE_LAYOUT_COLOUR_BOX_EMPTY-", relief="groove")],
                [sg.Radio(f"Colour", 1, key="-COLOUR-", enable_events=True, size=self.standard_size),
                 sg.ColorChooserButton("Colour", key="-PLATE_LAYOUT_COLOUR_CHOSE-",
                                       target="-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-"),
                 sg.Input(key="-PLATE_LAYOUT_COLOUR_CHOSE_TARGET-", visible=False, enable_events=True, disabled=True,
                          default_text="#ffffff")],
                # [sg.Radio('Erase', 1, key='-ERASE-', enable_events=True)],
                # [sg.Radio('Move Stuff', 1, key='-MOVE-', enable_events=True)],
                [sg.Checkbox("Use Archive", default=False, key="-ARCHIVE-", size=self.standard_size),
                 sg.DropDown(sorted(self.plate_list), key="-ARCHIVE_PLATES-", size=self.standard_size)],
                [sg.Button("Delete Layout", key="-DELETE_LAYOUT-"), sg.Button("Rename Layout", key="-RENAME_LAYOUT-"),
                 sg.Button("Export", key="-EXPORT_LAYOUT-")],
                [sg.Push(), sg.Button("Save Layout", key="-SAVE_LAYOUT-")],
            ])
        ]])

        layout = [[col_graph, col_options]]

        return layout

    def setup_1_update(self):
        """

        :return:A layour for the update-modul in the top box
        :rtype: list
        """

        col_buttons = sg.Frame("Update", [[
            sg.Column([
                [sg.T("Import folder:"),
                 sg.FolderBrowse(key="-UPDATE_FOLDER-", target="-FOLDER_PATH-",
                                 size=(self.standard_size, self.button_height))],
                [sg.Text("output_file", key="-FOLDER_PATH-", size=50)],
                [sg.Button("Add compounds", key="-UPDATE_COMPOUND-", size=(self.standard_size, self.button_height)),
                 sg.Button("Auto", key="-UPDATE_AUTO-", size=(self.standard_size, self.button_height))],
                [sg.Button("Add MotherPlates", key="-UPDATE_MP-", size=(self.standard_size, self.button_height)),
                 sg.Button("Add DaughterPlates", key="-UPDATE_DP-", size=(self.standard_size, self.button_height))],
            ])
        ]])

        layout = [sg.vtop([col_buttons])]

        return layout
        #return sg.Window("Update database", layout, size, finalize=True)

    def setup_1_simulator(self):
        """

        :return: A layour for the simulation-module in the top box
        :rtype: list
        """
        import_list = ["comPOUND", "MP Production", "DP production"]

        compound_col = sg.Frame("2D files (Compound -> 2D barcode)", [[
            sg.Column([
                [sg.Text("Input folder containing the compound txt file's"),
                 sg.FileBrowse(key="-SIM_INPUT_COMPOUND_FILE-", target="-SIM_COMPOUND_TARGET-")],
                [sg.T(key="-SIM_COMPOUND_TARGET-")],
            ])
        ]], visible=True, key="-SIM_COMPOUND_FRAME-")

        mp_production_col = sg.Frame("MP Production (2D barcode -> PB files)", [[
            sg.Column([
                [sg.Text("Input folder containing the 2D barcode txt file's (; separated)")],
                [sg.FolderBrowse(key="-SIM_INPUT_MP_FILE-", target="-SIM_MP_TARGET-")],
                [sg.T(key="-SIM_MP_TARGET-")],
                [sg.Text("MotherPlate initials", size=15),
                 sg.InputText(key="-SIM_MP_NAME-", size=10)],
                [sg.Text("Volume", size=15),
                 sg.InputText(key="-SIM_MP_VOL-", size=10)]
            ])
        ]], visible=False, key="-SIM_MP_FRAME-")

        dp_production = sg.Frame("DP production (PB files -> ECHO files)", [[
            sg.Column([
                [sg.Text("Input folder containing the MP CSV file's (; separated)"),
                 sg.FolderBrowse(key="-SIM_INPUT_DP_FILE-", target="-SIM_DP_TARGET-")],
                [sg.T(key="-SIM_DP_TARGET-")],
                [sg.Text("DP initials"),
                 sg.InputText(key="-SIM_DP_NAME-")]
            ])
        ]], visible=False, key="-SIM_DP_FRAME-")

        layout = [[sg.DropDown(import_list, size=self.standard_size, key="-SIM_INPUT_EQ-", enable_events=True,
                               default_value=import_list[0])],
                  sg.vtop([compound_col, mp_production_col, dp_production]),
                  [sg.Button("Simulate", key="-SIM_RUN-"),
                   sg.FolderBrowse("Output folder", key="-SIM_OUTPUT-", target="-SIM_OUTPUT_TArGET-"),
                   sg.T(key="-SIM_OUTPUT_TArGET-"), sg.Push(), sg.B("Start Up the Database", key="-START_UP_DB-")]]

        return layout

    def setup_2_compound(self):
        """

        :return: A layour for the info-module in the right box
        :rtype: list
        """

        col_picture = sg.Frame("picture", [[
            sg.Column([
                [sg.Image(key="-COMPOUND_INFO_PIC-", size=(500, 150))],
                [sg.Text(key="-COMPOUND_INFO_SMILES-", size=50)]
                ])
        ]])

        col_info = sg.Frame("Info", [[
            sg.Column([
                [sg.Input("", key="-COMPOUND_INFO_ID-", size=15), sg.Push(),
                 sg.Button("Search", key="-COMPOUND_INFO_SEARCH_COMPOUND_ID-")],
                [sg.Text("Academic/Commercial", size=self.standard_size),
                 sg.Text(key="-COMPOUND_INFO_AC-", size=self.standard_size)],
                [sg.Text("Origin", size=self.standard_size),
                 sg.Text(key="-COMPOUND_INFO_ORIGIN-", size=self.standard_size)],
                [sg.Text("Origin ID", size=self.standard_size),
                 sg.Text(key="-COMPOUND_INFO_ORIGIN_ID-", size=self.standard_size)],
                [sg.Text("Concentration", size=self.standard_size),
                 sg.Text(key="-COMPOUND_INFO_CONCENTRATION-", size=self.standard_size)],
                [sg.Text("volume left in MP", size=self.standard_size),
                 sg.Text(key="-COMPOUND_INFO_MP_VOLUME-", size=self.standard_size)]
                ]),
        ]])

        plate_headlines = ["name", "type", "well", "volume", "date"]
        row_plate_table = sg.Frame("Plate Table", [[
            sg.Column([
                [sg.Table(values=[], headings=plate_headlines, key="-COMPOUND_INFO_PLATE_TABLE-",
                          auto_size_columns=False)]
            ])
        ]], expand_x=True)

        tab_plates_table = sg.Tab("Plate info", [[sg.Frame("Plate Table", [[
            sg.Column([

            ])
        ]])
                               ]])

        tab_bio_exp_table = sg.Tab("Bio Info", [[sg.Frame("Bio Experimental", [[
            sg.Column([

            ])
        ]])
                                    ]])

        tab_purity_table = sg.Tab("Purity Info", [[sg.Frame("Purity", [[
            sg.Column([

            ])
        ]])
                                   ]])

        tab_groups = sg.TabGroup([[tab_plates_table, tab_bio_exp_table, tab_purity_table]],
                                 selected_background_color="purple", key="-COMPOUND_INFO_SUB_DATA-", enable_events=True,
                                 expand_x=True)

        layout = [sg.vtop([col_info, col_picture]), [sg.VPush()], [row_plate_table], [tab_groups]]

        return layout

    def setup_2_bio(self):
        # analyse_method = ["original", "normalised", "pora"]
        analyse_method = []
        mapping = ["State Mapping", "Heatmap", "Hit Map"]

        row_settings = sg.Frame("Bio Information", [[
            sg.Column([
                        [sg.Checkbox("Active Move+", key="-BIO_INFO_MOVE-", enable_events=True),
                         sg.Push(),
                         sg.Checkbox("Plate Report", key="-BIO_INFO_EXPORT_PLATE_REPORT-"),
                         sg.Checkbox("Final Report", key="-BIO_INFO_EXPORT_FINAL_REPORT-"),
                         sg.B("Export", key="-BIO_INFO_EXPORT-")],
                        [sg.HorizontalSeparator()],
                        [sg.T("Analyse method", size=14),
                         sg.DropDown(analyse_method, key="-BIO_INFO_ANALYSE_METHOD-", size=14, enable_events=True),
                         sg.T("Plate Mapping", size=14),
                         sg.DropDown(mapping, key="-BIO_INFO_MAPPING-", size=14, enable_events=True)],
                        [sg.T("Plate", size=14),
                         sg.InputCombo([], key="-BIO_INFO_PLATES-", size=14, enable_events=True),
                         sg.T("State", size=14),
                         sg.InputCombo([], key="-BIO_INFO_STATES-", size=14, enable_events=True)]
                    ])
        ]], expand_x=True)

        col_cal_info = sg.Column([
            [sg.T("avg", size=14), sg.T(key="-INFO_BIO_AVG-", size=14)],
            [sg.T("stdev", size=14), sg.T(key="-INFO_BIO_STDEV-", size=14)],
            [sg.T("Z-Prime", size=14), sg.T(key="-INFO_BIO_Z_PRIME-", size=14)]
        ])

        col_well_info = sg.Column([
            [sg.T("Well id", size=14), sg.T(key="-INFO_BIO_GRAPH_TARGET-", size=14)],
            [sg.T("Well value", size=14), sg.T(key="-INFO_BIO_WELL_VALUE-", size=14)],
            [sg.T("Compound name", size=14), sg.T(key="-INFO_BIO_GRAPH_COMPOUND_NAME-", size=14)]
        ])

        row_graph = sg.Frame("Plate Layout", [[
            sg.Column([
                [sg.Graph(canvas_size=(500, 350), graph_bottom_left=(0, 0), graph_top_right=(250, 175),
                          background_color='grey', key="-BIO_INFO_CANVAS-", enable_events=True, drag_submits=True,
                          motion_events=True)],
                [col_well_info, col_cal_info]
            ])
        ]], expand_x=True)

        col_hit_mapping = sg.Column([
            [sg.T("Hit-Map Settings", relief="groove")],
            [sg.HorizontalSeparator()],
            [sg.T("Lower bound", size=10),
             sg.InputText(key="-BIO_INFO_PORA_LOW_MIN_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_low_min")),
             sg.InputText(key="-BIO_INFO_PORA_LOW_MAX_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_low_max"))],
            [sg.T("Middle bound", size=10),
             sg.InputText(key="-BIO_INFO_PORA_MID_MIN_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_mid_min")),
             sg.InputText(key="-BIO_INFO_PORA_MID_MAX_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_mid_max"))],
            [sg.T("Higher bound", size=10),
             sg.InputText(key="-BIO_INFO_PORA_HIGH_MIN_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_high_min")),
             sg.InputText(key="-BIO_INFO_PORA_HIGH_MAX_HIT_THRESHOLD-", size=8, enable_events=True,
                          default_text=self.config["Settings_bio"].getfloat("final_report_pora_threshold_high_max"))],

            [sg.ColorChooserButton("Low Values Colour", key="-INFO_BIO_HIT_MAP_LOW_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_pora_threshold_colour_low"]
                  , key="-BIO_INFO_HIT_MAP_LOW_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HIT_MAP_LOW_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_low"])],

            [sg.ColorChooserButton("Mid Values Colour", key="-INFO_BIO_HIT_MAP_MID_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_pora_threshold_colour_mid"]
                  , key="-BIO_INFO_HIT_MAP_MID_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HIT_MAP_MID_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_mid"])],

            [sg.ColorChooserButton("High Values Colour", key="-INFO_BIO_HIT_MAP_HIGH_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_pora_threshold_colour_high"]
                  , key="-BIO_INFO_HIT_MAP_HIGH_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HIT_MAP_HIGH_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_pora_threshold_colour_high"])],
            # [sg.T("Low Colour", size=10), sg.DropDown(colours, key="-INFO_BIO_Hit_LOW-", enable_events=True,
            #                                           default_value=self.config["Settings_bio"]
            #                                           ["plate_report_pora_threshold_colour_low"], size=14)],
            # [sg.T("Mid Colour", size=10), sg.DropDown(colours, key="-INFO_BIO_Hit_MID-", enable_events=True,
            #                                           default_value=self.config["Settings_bio"]
            #                                           ["plate_report_pora_threshold_colour_mid"], size=14)],
            # [sg.T("High Colour", size=10), sg.DropDown(colours, key="-INFO_BIO_Hit_HIGH-", enable_events=True,
            #                                            default_value=self.config["Settings_bio"]
            #                                            ["plate_report_pora_threshold_colour_high"], size=14)],
        ], key="-INFO_BIO_ROW_HIT-"
            # , size=(0, 0)
        )

        col_heatmap = sg.Column([
            [sg.T("Heatmap Settings", relief="groove")],
            [sg.HorizontalSeparator()],
            [sg.ColorChooserButton("Low Values Colour", key="-INFO_BIO_HEATMAP_LOW_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_heatmap_colours_low"]
                      , key="-BIO_INFO_HEATMAP_LOW_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HEATMAP_LOW_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_low"])],
            [sg.ColorChooserButton("Mid Values Colour", key="-INFO_BIO_HEATMAP_MID_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_heatmap_colours_mid"]
                      , key="-BIO_INFO_HEATMAP_MID_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HEATMAP_MID_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_mid"])],
            [sg.ColorChooserButton("High Values Colour", key="-INFO_BIO_HEATMAP_HIGH_COLOUR-", size=(15, None),
                                   target="-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-"),
             sg.T(background_color=self.config["Settings_bio"]["plate_report_heatmap_colours_high"]
                      , key="-BIO_INFO_HEATMAP_HIGH_COLOUR_BOX-", size=8, relief="groove"),
             sg.Input(key="-BIO_INFO_HEATMAP_HIGH_COLOUR_TARGET-", visible=False, enable_events=True, disabled=True,
                      default_text=self.config["Settings_bio"]["plate_report_heatmap_colours_high"])],
            [sg.T("Low", size=10), sg.T("Mid", size=8), sg.T("High", size=8)],
            [sg.InputText(0, key="-BIO_INFO_HEAT_PERCENTILE_LOW-", size=10, enable_events=True),
             sg.InputText(50, key="-BIO_INFO_HEAT_PERCENTILE_MID-", size=10, enable_events=True),
             sg.InputText(100, key="-BIO_INFO_HEAT_PERCENTILE_HIGH-", size=10, enable_events=True)]

        ], key="-INFO_BIO_ROW_HEAT-"
            # , size=(0, 0)
        )

        col_list_box = sg.Column([
            [sg.T("States for Mapping")],
            [sg.Listbox([], key="-BIO_INFO_STATE_LIST_BOX-", size=(10, 10), enable_events=True,
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)]
        ])

        row_options = sg.Frame("Graph Settings", [
            # sg.vtop([col_heatmap, col_hit_mapping])  This does not work for some reason....
            [col_heatmap, sg.VerticalSeparator(), col_hit_mapping, sg.VerticalSeparator(), col_list_box],
            [sg.Push(), sg.Button("Re-Draw", key="-BIO_INFO_RE_DRAW-")]
            ])

        table_overview_headings = ["Method", "States", "calc", "value"]
        row_plate_overview = sg.Frame("Plate Overview", [[
            sg.Column([
                [sg.T("An overview over data per plate.")],
                [sg.Table([], headings=table_overview_headings, key="-BIO_INFO_OVERVIEW_TABLE-"),
                 sg.Listbox([], key="-BIO_INFO_PLATE_OVERVIEW_METHOD_LIST-", size=(10, 10),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True),
                 sg.Listbox([], key="-BIO_INFO_PLATE_OVERVIEW_STATE_LIST-", size=(10, 10),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True)],
                [sg.DropDown([], key="-BIO_INFO_PLATE_OVERVIEW_PLATE-", size=14, enable_events=True)]
            ])
        ]])

        table_overview_headings_avg = ["Barcode", "avg"]
        table_overview_headings_stdev = ["Barcode", "stdev"]
        table_overview_headings_z_prime = ["Barcode", "Z-Prime"]
        row_overview = sg.Frame("Overview", [[
            sg.Column([
                [sg.T("Overview of plates for the different calculations")],
                [sg.Table([], headings=table_overview_headings_avg, key="-BIO_INFO_OVERVIEW_AVG_TABLE-",
                          size=(10, 10), auto_size_columns=False),
                 sg.Table([], headings=table_overview_headings_stdev, key="-BIO_INFO_OVERVIEW_STDEV_TABLE-",
                          size=(10, 10), auto_size_columns=False),
                 sg.Table([], headings=table_overview_headings_z_prime, key="-BIO_INFO_OVERVIEW_Z_PRIME_TABLE-",
                          size=(10, 10), auto_size_columns=False)],
                [sg.DropDown([], key="-BIO_INFO_OVERVIEW_METHOD-", size=14, enable_events=True),
                 sg.DropDown([], key="-BIO_INFO_OVERVIEW_STATE-", size=14, enable_events=True)]
            ])
        ]])

        table_z_prime_list_headings = ["Barcode", "Z-Prime"]
        row_z_prime = sg.Frame("Z-Prime", [[
            sg.Column([
                [sg.T("Overview of Z-Prime values")],
                [sg.Table([], headings=table_z_prime_list_headings, key="-BIO_INFO_Z_PRIME_LIST_TABLE-",
                          auto_size_columns=False),
                 sg.Column([
                     [sg.T("Max:", size=5), sg.T("", key="-BIO_INFO_Z_PRIME_MAX_BARCODE-", size=10),
                      sg.T("", key="-BIO_INFO_Z_PRIME_MAX_VALUE-", size=10)],
                     [sg.T("Min:", size=5), sg.T("", key="-BIO_INFO_Z_PRIME_MIN_BARCODE-", size=10),
                      sg.T("", key="-BIO_INFO_Z_PRIME_MIN_VALUE-", size=10)]
                 ])],
                [sg.B("Matrix", key="-BIO_INFO_Z_PRIME_MATRIX_BUTTON-")]
            ])
        ]])

        table_hit_list_headings = ["well", "value", "compound"]
        row_hit_list = sg.Frame("Hit List", [[
            sg.Column([
                [sg.T("Tables with wells that are within the hit list boundaries")],
                [sg.Table([], headings=table_hit_list_headings, key="-BIO_INFO_HIT_LIST_LOW_TABLE-"),
                 sg.Table([], headings=table_hit_list_headings, key="-BIO_INFO_HIT_LIST_MID_TABLE-"),
                 sg.Table([], headings=table_hit_list_headings, key="-BIO_INFO_HIT_LIST_HIGH_TABLE-")],

                [sg.DropDown([], key="-BIO_INFO_HIT_LIST_PLATES-", size=14),
                 sg.DropDown([], key="-BIO_INFO_HIT_LIST_METHOD-", size=14),
                 sg.DropDown([], key="-BIO_INFO_HIT_LIST_STATE-", size=14)]
            ])
        ]])

        table_headings = matrix_header
        table_data = []
        col_matrix_tabl = sg.Column([
            [sg.Table(table_data, headings=table_headings, auto_size_columns=False,
                      key="-BIO_INFO_MATRIX_TABLE-", vertical_scroll_only=False, size=(7, 7))],
            [sg.T("", size=10)],
        ])

        row_matrix = sg.Frame("Matrix", [
            [sg.T("A matrix of calculations for the different plate compared to each other, in %")],
            [col_matrix_tabl],
            [sg.DropDown([], key="-BIO_INFO_MATRIX_METHOD-", size=14),
             sg.DropDown([], key="-BIO_INFO_MATRIX_STATE-", size=14),
             sg.DropDown([], key="-BIO_INFO_MATRIX_CALC-", size=14)],
            [sg.B("Generate Matrix", key="-BIO_INFO_MATRIX_BUTTON-"),
             sg.B("Pop out the Matrix", key="-BIO_INFO_MATRIX_POPUP-")]
        ])

        # This is covered by overview
        # table_list_headings = ["barcode", "calc"]
        # row_list = sg.Frame("List", [
        #     [sg.Column([
        #         [sg.T("Table with a list of calculation values for all the plates.")],
        #         [sg.Table([], headings=table_list_headings, key="-BIO_INFO_LIST_TABLE-", auto_size_columns=False)],
        #         [sg.T("Method", size=14), sg.T("State", size=14), sg.T("Calculation", size=14)],
        #         [sg.DropDown([], key="-BIO_INFO_LIST_METHOD-", size=14, enable_events=True),
        #          sg.DropDown([], key="-BIO_INFO_LIST_STATE-", size=14, enable_events=True),
        #          sg.DropDown([], key="-BIO_INFO_LIST_CALC-", size=14, enable_events=True)],
        #     ])]
        # ])

        tab_mapping = sg.Tab("Mapping", [[row_options]])
        tab_overview = sg.Tab("Overview", [[row_overview]])
        tab_plate_overview = sg.Tab("Plate Overview", [[row_plate_overview]])
        tab_z_prime = sg.Tab("Z-Prime", [[row_z_prime]])
        tab_hit_list = sg.Tab("Hit List", [[row_hit_list]])
        tab_matrix = sg.Tab("Matrix", [[row_matrix]])
        # tab_list = sg.Tab("List", [[row_list]])

        tab_bio_list = [tab_mapping, tab_overview, tab_plate_overview, tab_z_prime, tab_hit_list, tab_matrix]

        tab_groups = [sg.TabGroup([tab_bio_list], selected_background_color="purple",
                                  key="-BIO_INFO_SUB_SETTINGS_TABS-", enable_events=True)]

        top_row = [[row_settings], [row_graph]]

        layout = [[sg.Pane([sg.Column(top_row), sg.Column([tab_groups])])]]
        return layout

    def setup_2_purity(self):
        hey = self.config
        graph_showing = ["UV", "MS Positive", "MS Negative"]

        row_settings = sg.Frame("Purity settings", [[
            sg.Column([
                [sg.T("THIS IS THE COLUMN")],
                [sg.DropDown(graph_showing, key="-PURITY_INFO_GRAPH_SHOWING-")],
                [sg.Listbox("", key="-PURITY_INFO_SAMPLE_BOX-", enable_events=True, size=(10, 7),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            ])
        ]])

        row_canvas = sg.Frame("Canvas", [[
            sg.Column([
                [sg.Canvas(key="-PURITY_INFO_CANVAS-")]
            ])
        ]])

        purity_headings = ["row_id", "sample", "batch", "uv", "ms_pos", "ms_neg", "method", "file_name", "date"]
        row_elements = sg.Frame("Stuff", [[
            sg.Column([
                [sg.Table("", key="-PURITY_INFO_SAMPLE_TABLE-", headings=purity_headings)]
            ])
        ]])

        layout = [[row_settings], [row_canvas], [row_elements]]
        return layout

    def setup_compound_table(self):
        """

        :return: A layout for the compound table-module in the table box
        :rtype: list
        """
        headlines = ["compound_id", "smiles", "volume"]
        tables = ["Compound", "Mother Plates", "Assay Plates"]
        treedata = sg.TreeData()

        raw_table_col = sg.Column([
            [sg.Text("Raw data")],
            [sg.Tree(data=treedata, headings=headlines, row_height=100, auto_size_columns=False, num_rows=4,
                     col0_width=30, key="-TREE_DB-", show_expanded=True, expand_y=True, expand_x=True,
                     enable_events=True)]
        ])

        layout = [
            [raw_table_col],
            [sg.Button("Export", key="-C_TABLE_EXPORT-", size=self.standard_size),
             sg.Button("Refresh", key="-C_TABLE_REFRESH-", size=self.standard_size),
             # sg.DropDown(values=tables, default_value=tables[0], key="-C_TABLE_FILE_TYPE-"),
             sg.Text(text="Compounds: 0", key="-C_TABLE_COUNT-")]
        ]
        return layout
        #return sg.Window("batch and sample selection", layout, size, finalize=True)

    def setup_bio_experiment_table(self):
        """

        :return: A layout for the compound experiment-module in the table box
        :rtype: list
        """
        responsible = [keys for keys in list(self.config["Responsible"].keys())]

        table_data = []
        headings = ["exp_id", "assay_name", "raw_data", "plate_layout", "responsible", "date"]

        col_table = sg.Column([
            [sg.Text("Experimental data")],
            [sg.Table(values=table_data, headings=headings, key="-BIO_EXP_TABLE-",
                      auto_size_columns=False, col_widths=[10, 10, 10], enable_events=True)],
            [sg.B("Refresh", key="-BIO_EXP_TABLE_REFRESH-")]

        ])

        col_search = sg.Frame("Search Criteria", [[
            sg.Column([
                [sg.CalendarButton("Start date", key="-BIO_EXP_TABLE_DATE_START-", format="%Y-%m-%d", enable_events=True
                                   , target="-BIO_EXP_TABLE_DATE_START_TARGET-", size=(10, 1)),
                 sg.Input(key="-BIO_EXP_TABLE_DATE_START_TARGET-", size=10, enable_events=True)],
                [sg.CalendarButton("End date", key="-BIO_EXP_TABLE_DATE_END-", format="%Y-%m-%d", enable_events=True,
                                   target="-BIO_EXP_TABLE_DATE_END_TARGET-", size=(10, 1)),
                 sg.Input(key="-BIO_EXP_TABLE_DATE_END_TARGET-", size=10)],
                [sg.T("Responsible", size=10), sg.DropDown(responsible, key="-BIO_EXP_TABLE_RESPONSIBLE-", size=10)],
            ])
        ]])

        layout = [[col_table, col_search]]
        return layout

    def setup_lc_experiment_table(self):
        """

        :return: A layout for the compound experiment-module in the table box
        :rtype: list
        """

        table_data = []
        headings = ["exp_id", "assay_name", "raw_data", "plate_layout", "responsible", "date"]

        col_table = sg.Column([
            [sg.Text("LC Samples")],
            [sg.Table(values=table_data, headings=headings, key="-LC_MS_SAMPLE_TABLE-",
                      auto_size_columns=False, col_widths=[10, 10, 10], enable_events=True)],
            [sg.B("Refresh", key="-LC_MS_SAMPLE_TABLE_REFRESH-")]

        ])

        col_search = sg.Frame("Search Criteria", [[
            sg.Column([
                [sg.Listbox("", key="-LC_MS_TABLE_BATCH_LIST_BOX-", enable_events=True, size=(18, 10),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                [sg.CalendarButton("Start date", key="-LC_MS_TABLE_DATE_START-", format="%Y-%m-%d", enable_events=True
                                   , target="-LC_MS_TABLE_DATE_START_TARGET-", size=(10, 1)),
                 sg.Input(key="-LC_MS_TABLE_DATE_START_TARGET-", size=10, enable_events=True)],
                [sg.CalendarButton("End date", key="-LC_MS_TABLE_DATE_END-", format="%Y-%m-%d", enable_events=True,
                                   target="-LC_MS_TABLE_DATE_END_TARGET-", size=(10, 1)),
                 sg.Input(key="-LC_MS_TABLE_DATE_END_TARGET-", size=10)]

            ])
        ]])

        layout = [[col_table, col_search]]
        return layout

    def setup_plate_table(self):
        """

        :return: A layout for the plate table-module in the table box
        :rtype: list
        """
        headings = ["row_counter", "Barcode", "Compound", "Well", "Volume", "Date", "Source Barcode", "Source Well"]
        # headings = ["mp_barcode", "compound_id", "mp_well", "volume", "Date", "dp_barcode", "dp_well"]
        dd = ["Mother Plates", "Daughter Plates"]
        col_table = sg.Frame("Plate Table", [[
            sg.Column([
                [sg.Table([], headings=headings, key="-PLATE_TABLE_TABLE-", size=(20, 5))],
                [sg.Input("", key="-PLATE_TABLE_BARCODE_SEARCH-", size=10), sg.B("Search", key="-PLATE_TABLE_SEARCH-")]
            ]),
            sg.Column([
                [sg.Listbox("", key="-PLATE_TABLE_BARCODE_LIST_BOX-", enable_events=True, size=(10, 7),
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                [sg.DropDown(dd, key="-PLATE_TABLE_CHOOSER-", enable_events=True)],
                [sg.CalendarButton("Start Date", key="-PLATE_TABLE_START_DATE-", format="%Y-%m-%d", size=10,
                                   enable_events=True, target="-PLATE_TABLE_START_DATE_TARGET-"),
                 sg.Input(key="-PLATE_TABLE_START_DATE_TARGET-", size=10, enable_events=True)],
                [sg.CalendarButton("End Date", key="-PLATE_TABLE_END_DATE-", format="%Y-%m-%d", size=10,
                                   enable_events=True, target="-PLATE_TABLE_END_DATE_TARGET-"),
                 sg.Input(key="-PLATE_TABLE_END_DATE_TARGET-", size=10, enable_events=True)]
            ])
        ]], expand_x=True)

        layout = [[col_table]]
        return layout

    def layout_tab_group_1(self):
        """

        :return: the layout for the tab groups in the top box
        :rtype: list
        """
        tab_1_search = sg.Tab("search", self.setup_1_search())
        tab_1_bio_data = sg.Tab("bio data", self.setup_1_bio())
        tab_1_purity_data = sg.Tab("purity data", self.setup_1_purity())
        tab_1_plate_layout = sg.Tab("Plate layout", self.setup_1_plate_layout())
        tab_1_add = sg.Tab("Update", self.setup_1_update())
        tab_1_sim = sg.Tab("Sim", self.setup_1_simulator())

        tab_group_1_list = [tab_1_search, tab_1_bio_data, tab_1_purity_data, tab_1_plate_layout, tab_1_add, tab_1_sim]

        return [[sg.TabGroup([tab_group_1_list], selected_background_color="purple", key="-TAB_GROUP_ONE-",
                             enable_events=True)]]

    def layout_tab_group_2(self):
        """

        :return: the layout for the tab groups in the right box
        :rtype: list
        """

        tab_2_info = sg.Tab("Compound Info", self.setup_2_compound())
        tab_2_bio_bio = sg.Tab("bio info", self.setup_2_bio())
        tab_2_purity_purity = sg.Tab("purity info", self.setup_2_purity())

        tab_group_2_list = [tab_2_info, tab_2_bio_bio, tab_2_purity_purity]

        return [[sg.TabGroup([tab_group_2_list], selected_background_color="purple", key="-TAB_GROUP_TWO-",
                             enable_events=True)]]

    def layout_tab_group_tables(self):
        """

        :return: the layout for the tab groups in the table box
        :rtype: list
        """

        tab_table_compound = sg.Tab("Compound table", self.setup_compound_table())
        tab_bio_experiment_table = sg.Tab("Bio Experiment table", self.setup_bio_experiment_table())
        tab_lc_experiment_table = sg.Tab("LC Experiment table", self.setup_lc_experiment_table())
        tab_plate_table = sg.Tab("Plate tables", self.setup_plate_table())

        tab_group_tables = [tab_table_compound, tab_bio_experiment_table, tab_lc_experiment_table, tab_plate_table]
        return [[sg.TabGroup([tab_group_tables], key="-TABLE_TAB_GRP-", enable_events=True,
                             selected_background_color="purple")]]

    def full_layout(self):
        """

        :return: The final layout
        :rtype: PySimpleGUI.PySimpleGUI.Window
        """
        sg.theme(self.config["GUI"]["theme"])
        window_size = (int(self.config["GUI"]["size_x"]), int(self.config["GUI"]["size_y"]))
        x_size = window_size[0]/3
        y_size = window_size[1]/3

        tab_group_1 = self.layout_tab_group_1()
        tab_group_2 = self.layout_tab_group_2()
        table_block = self.layout_tab_group_tables()
        menu = self.menu_top()
        mouse_right_click, right_click_options = self.menu_mouse()
        # col_1_1 = [[sg.Frame(layout=tab_group_1, title="X-1", size=(x_size*2, y_size))]]
        # col_1_2 = [[sg.Frame(layout=table_block, title="Table", size=(x_size*2, y_size*2))]]
        # col_2 = [[sg.Frame(layout=tab_group_2, title="X-2", size=(x_size, window_size[1]))]]

        layout_complete = [[
            menu,
            sg.Pane([
                sg.Column(
                    [[sg.Pane([sg.Column(tab_group_1), sg.Column(table_block)], orientation="v")]]
                ),
                sg.Column(tab_group_2)
                ], orientation="h")
        ]]

        return sg.Window("SCore", layout_complete, finalize=True, resizable=True, right_click_menu=right_click_options)

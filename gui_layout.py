import PySimpleGUI as sg


class GUILayout:
    def __init__(self, config, plate_list):
        self.config = config
        self.standard_size = 20
        self.button_height = 1
        self.plate_list = plate_list
    @staticmethod
    def menu_top():
        menu_top_def = [['File', ['Open', 'Save', 'Exit', ]],
                        ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                        ['Help', 'About...'], ]
        layout = [[sg.Menu(menu_top_def)]]
        return layout

    @staticmethod
    def menu_mouse():
        menu_mouse_def = [['File', ['Open', 'Save', 'Exit', ]],
                    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                    ['Help', 'About...'], ]

        layout = [[sg.ButtonMenu("place_holder", menu_mouse_def, key="-RMB-")]]

        return layout, menu_mouse_def

    def setup_1_search(self):
        origin = ["company", "research"]
        company = list(self.config["company"].keys())

        subs_search_methods = list(self.config["structure_search_methode"].keys())
        plate_production = ["Mother Plates", "Assay Plates"]

        col_1 = sg.Frame("Search", [[
            sg.Column([
                [sg.DropDown(values=origin, default_value=origin[0], key="-SEARCH_ORIGIN-", enable_events=True),
                 sg.DropDown(values=company, default_value=company[0], key="-SEARCH_WHO-")],
                [sg.T("Out put folder"),
                 sg.FolderBrowse(key="-OUTPUT_FILE-", target="-OUTPUT_FOLDER-", initial_folder="output_files")],
                [sg.Text(key="-OUTPUT_FOLDER-", size=75)],
                [sg.Checkbox(text="Ignore plated compounds?", key="-IGNORE_ACTIVE-")],
                [sg.Text("Amount of Plates", size=self.standard_size),
                 sg.InputText(key="-MP_AMOUNT-", size=self.standard_size)],
                [sg.Text("Transferee vol:", size=self.standard_size),
                 sg.InputText(key="-TRANS_VOL-", size=self.standard_size)],
                [sg.Text("Plate Production"), sg.DropDown(plate_production, key="-PP-",
                                                          default_value=plate_production[0])]
            ])
        ]])

        col_sub_search = sg.Frame("Sub Search", [[
            sg.Column([
                [sg.Checkbox(text="Sub Search?", key="-SUB_SEARCH-")],
                [sg.Text("smiles", size=self.standard_size), sg.InputText(key="-SMILES-", size=self.standard_size),
                 sg.Button("Draw molecule", key="-DRAW_MOL-")],
                [sg.Text("method?", size=self.standard_size),
                 sg.DropDown(subs_search_methods, key="-SS_METHOD-", default_value=subs_search_methods[0],
                             enable_events=True)],
                [sg.Text("Similarity Threshold", size=self.standard_size),
                 sg.InputText(key="-THRESHOLD-", default_text=0, size=self.standard_size)],
                [sg.HorizontalSeparator()],
                [sg.Text("Morgan specific options", key="-MORGAN_OPTIONS-", visible=False)],
                [sg.Checkbox(text="chirality", key="-MORGAN_CHIRALITY-", visible=False),
                 sg.Checkbox(text="Features", key="-MORGAN_FEATURES-", visible=False)],
                [sg.Text("n bits", key="-BITS_TEXT-", size=self.standard_size, visible=False),
                 sg.InputText(key="-MORGAN_BITS-", size=self.standard_size, visible=False)],
                [sg.Text("bound range", key="-BOUND_TEXT-", size=self.standard_size, visible=False),
                 sg.InputText(key="-MORGAN_RANGE-", size=self.standard_size, visible=False)],
            ])
        ]])

        layout = [sg.vtop([col_1,  col_sub_search]),
                  [sg.Checkbox("All compounds", key="-ALL_COMPOUNDS-", enable_events=False)]]

        return layout

    def setup_1_bio(self):

        # maybe make it a config file. and update the config file when new method are added ?
        analyse_type = ["single point"]
        colours = [keys for keys in list(self.config["colours to hex"].keys())]

        sample_type = ["single point", "duplicate", "triplicate"]

        col_bio_analysis = sg.Frame("Analyse setup", [[
            sg.Column([
                [sg.FolderBrowse(button_text="Import Folder", key="-BIO_IMPORT_FOLDER-", target="-BIO_IMPORT_TARGET-")],
                [sg.Text(key="-BIO_IMPORT_TARGET-", size=self.standard_size*2)],
                [sg.FolderBrowse(button_text="Export Folder", key="-BIO_EXPORT_FOLDER-", target="-BIO_EXPORT_TARGET-")],
                [sg.Text(key="-BIO_EXPORT_TARGET-", size=self.standard_size*2)],
                [sg.Text("Plate layout", size=self.standard_size),
                 sg.DropDown(sorted(self.plate_list), key="-BIO_PLATE_LAYOUT-", enable_events=True,
                             size=self.standard_size)],
                [sg.Text("Analyse method", size=self.standard_size),
                 sg.DropDown(analyse_type, key="-BIO_ANALYSE_TYPE-", size=self.standard_size, enable_events=True)],
                [sg.Text("sample type (Not working)", size=self.standard_size),
                 sg.DropDown(sample_type, key="-BIO_SAMPLE_TYPE-", default_value=sample_type[0],
                             size=self.standard_size, enable_events=True)],
                [sg.Checkbox("combined report? ", key="-BIO_COMBINED_REPORT-", default=False, enable_events=True),
                 sg.B("Report setting", key="-BIO_REPORT_SETTINGS-")],
                [sg.InputText(key="-FINAL_BIO_NAME-")],
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
                [sg.Button("Export", key="-EXPORT_BIO-"),
                 sg.Checkbox("Compound related data?", key="-BIO_COMPOUND_DATA-")]
            ])
        ]])

        # col_report = sg.Frame("Report setup", [[
        #     sg.Column([
        #         [sg.T("Data for each excel file:")],
        #         [sg.Checkbox("Sample", key="-BIO_SAMPLE-", default=True), sg.Checkbox("Minimum", key="-BIO_MIN-"),
        #          sg.Checkbox("Max", key="-BIO_MAX-"), sg.Checkbox("Empty", key="-BIO_EMPTY-")],
        #         [sg.Checkbox("Negative Control", key="-BIO_NEG_C-"), sg.Checkbox("Positive Control", key="-BIO_POS_C-"),
        #          sg.Checkbox("Blank", key="-BIO_BLANK-"), sg.Checkbox("Z prime", key="-BIO_Z-PRIME-")],
        #         [sg.T("Data for combined report")],
        #         [sg.Checkbox("combined report? ", key="-BIO_COMBINED_REPORT-", default=False, enable_events=True)],
        #         [sg.InputText(key="-FINAL_BIO_NAME-")],
        #         [sg.B("Report setting", key="-BIO_REPORT_SETTINGS-")]
        #     ])
        # ]])

        col_graph = sg.Frame("Plate Layout", [[
            sg.Column([
                [sg.Graph(canvas_size=(250, 175), graph_bottom_left=(0, 0), graph_top_right=(250, 175),
                          background_color='grey', key="-BIO_CANVAS-", enable_events=False, drag_submits=False,
                          motion_events=False)],
                [sg.Text("Sample:", size=self.standard_size),
                 sg.Text(f'{self.config["plate_colouring"]["sample"]}/yellow')],
                [sg.Text("Blank:", size=self.standard_size), sg.Text(self.config["plate_colouring"]["blank"])],
                [sg.Text("Maximum:", size=self.standard_size), sg.Text(self.config["plate_colouring"]["max"])],
                [sg.Text("Minimum:", size=self.standard_size), sg.Text(self.config["plate_colouring"]["minimum"])],
                [sg.Text("Positive Control:", size=self.standard_size),
                 sg.Text(self.config["plate_colouring"]["positive"])],
                [sg.Text("Negative Control:", size=self.standard_size),
                 sg.Text(self.config["plate_colouring"]["negative"])],
                [sg.Text("Empty:", size=self.standard_size), sg.Text(self.config["plate_colouring"]["empty"])],
            ])
        ]])

        # layout = [sg.vtop([col_bio_analysis, col_report, col_graph])]
        layout = [sg.vtop([col_bio_analysis, col_graph])]

        return layout

    @staticmethod
    def setup_1_purity():
        layout = [
            [sg.Text("this is tab group 3 in tab layout 1")]
        ]

        return layout

    def setup_1_update(self):
        ms_mode = ["Positive", "Negative"]

        col_buttons = sg.Frame("buttons", [[
            sg.Column([
                [sg.FolderBrowse(key="-UPDATE_FOLDER-", target="-FOLDER_PATH-",
                                 size=(self.standard_size, self.button_height))],
                [sg.Text("output_file", key="-FOLDER_PATH-", size=50)],
                [sg.Button("Add compounds", key="-UPDATE_COMPOUND-", size=(self.standard_size, self.button_height)),
                 sg.Button("Auto", key="-UPDATE_AUTO-", size=(self.standard_size, self.button_height))],
                [sg.Button("Add MotherPlates", key="-UPDATE_MP-", size=(self.standard_size, self.button_height)),
                 sg.Button("Add DaughterPlates", key="-UPDATE_DP-", size=(self.standard_size, self.button_height))],
                [sg.Button("Add purity data", key="-UPDATE_PURITY-", size=(self.standard_size, self.button_height)),
                 sg.Button("Add bio data", key="-UPDATE_BIO-", size=(self.standard_size, self.button_height))],

            ])
        ]])

        col_ms = sg.Frame("MS setup", [[
            sg.Column([
                [sg.Text("UV wavelength - If using one wavelength", size=self.standard_size)],
                [sg.Checkbox("UV one", key="-UPDATE_UV-"),
                 sg.InputText(key="-UPDATE_UV_WAVE-", default_text=int(self.config["MS_default"]["uv_wavelength"]),
                              size=self.standard_size)],
                [sg.Text("UV threshold", size=self.standard_size),
                 sg.InputText(key="-UPDATE_UV_THRESHOLD-", default_text=int(self.config["MS_default"]["uv_threshold"]),
                              size=self.standard_size)],
                [sg.Text("Solvent peak retention time", size=self.standard_size),
                 sg.InputText(key="-UPDATE_RT_SOLVENT-", default_text=float(self.config["MS_default"]["rt_solvent"]),
                              size=self.standard_size)],
                [sg.DropDown(ms_mode, key="-UPDATE_MS_MODE-", default_value=ms_mode[0])],
                [sg.Text("Delta MS", size=self.standard_size),
                 sg.InputText(key="-UPDATE_MS_DELTA-", default_text=float(self.config["MS_default"]["rt_solvent"]),
                              size=self.standard_size)],
                [sg.Text("MS threshold", size=self.standard_size),
                 sg.InputText(key="-UPDATE_MS_THRESHOLD-", default_text=int(self.config["MS_default"]["ms_threshold"]),
                              size=self.standard_size)]
            ])
        ]])

        layout = [sg.vtop([col_buttons, col_ms])]

        return layout
        #return sg.Window("Update database", layout, size, finalize=True)

    def setup_1_plate_layout(self):
        """
        Layout for plate formatting
        """
        color_select = {}
        for keys in list(self.config["plate_colouring"].keys()):
            color_select[keys] = self.config["plate_colouring"][keys]

        plate_type = ["plate_96", "plate_384", "plate_1536"]
        sample_type = ["single point", "duplicate", "triplicate"]
        colours = ['snow', 'slate gray', 'blue', 'deep sky blue', 'cyan', 'dark green', 'lime green', 'forest green',
                   'yellow', 'gold', 'saddle brown', 'orange', 'orange red', 'red', 'hot pink', 'deep pink', 'maroon',
                   'purple', 'ivory2', 'blue2', 'DeepSkyBlue3', 'turquoise1', 'DarkSlategray1', 'SeaGreen1', 'green2',
                   'chartreuse2', 'yellow2', 'gold2', 'burlywood2', 'chocolate1', 'OrangeRed2', 'red3', 'DeepPink2',
                   'magenta3', 'purple4', 'grey59']

        col_graph = sg.Column([
            [sg.Graph(canvas_size=(500, 350), graph_bottom_left=(0, 0), graph_top_right=(500, 350),
                      background_color='grey', key="-CANVAS-", enable_events=True, drag_submits=True,
                      motion_events=True)],
            [sg.DropDown(values=plate_type, default_value=plate_type[1], key="-PLATE-"),
             sg.B("Draw plate", key="-DRAW-"),
             # sg.B("Add sample layout", key="-DRAW_SAMPLE_LAYOUT-"),
             sg.Text(key="-INFO-")]
        ])

        col_options = sg.Frame("Options", [[
            sg.Column([
                [sg.Text("Choose what clicking a figure does", enable_events=True)],
                [sg.Radio(f"Select Sample - {color_select['sample']}", 1, key="-RECT_SAMPLES-", enable_events=True,
                          default=True),
                 sg.DropDown(sample_type, key="-RECT_SAMPLE_TYPE-", default_value=sample_type[0])],
                [sg.Radio(f"Select Blank - {color_select['blank']}", 1, key="-RECT_BLANK-", enable_events=True)],
                [sg.Radio(f"Select Max Signal - {color_select['max']}", 1, key="-RECT_MAX-", enable_events=True)],
                [sg.Radio(f"Select Minimum Signal - {color_select['minimum']}", 1, key="-RECT_MIN-",
                          enable_events=True)],
                [sg.Radio(f"Select Positive Control - {color_select['positive']}", 1, key="-RECT_POS-",
                          enable_events=True)],
                [sg.Radio(f"Select Negative Control - {color_select['negative']}", 1, key="-RECT_NEG-",
                          enable_events=True)],
                [sg.Radio(f"Select Empty - {color_select['empty']}", 1, key="-RECT_EMPTY-", enable_events=True)],
                [sg.Radio(f"colour", 1, key="-COLOUR-", enable_events=True, size=self.standard_size),
                 sg.DropDown(colours, key="-COLOUR_CHOICE-", size=self.standard_size)],
                # [sg.Radio('Erase', 1, key='-ERASE-', enable_events=True)],
                # [sg.Radio('Move Stuff', 1, key='-MOVE-', enable_events=True)],
                [sg.Checkbox("use archive?", default=False, key="-ARCHIVE-", size=self.standard_size),
                 sg.DropDown(sorted(self.plate_list), key="-ARCHIVE_PLATES-", size=self.standard_size)],
                [sg.Button("Delete Layout", key="-DELETE_LAYOUT-"), sg.Button("Rename Layout", key="-RENAME_LAYOUT-")],
                [sg.Button("Export", key="-EXPORT_LAYOUT-"), sg.Button("Save Layout", key="-SAVE_LAYOUT-")]
            ])
        ]])

        layout = [[col_graph, col_options]]

        return layout
        # return sg.Window("Plate test", layout, finalize=True)

    def setup_1_simulator(self):
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
                [sg.Text("Input folder containing the 2D barcode txt file's (; separated)"),
                 sg.FolderBrowse(key="-SIM_INPUT_MP_FILE-", target="-SIM_MP_TARGET-")],
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
                   sg.T(key="-SIM_OUTPUT_TArGET-")]]

        return layout

    def setup_2_info(self):

        col_picture = sg.Frame("picture", [[
            sg.Column([
                [sg.Image(key="-INFO_PIC-", size=(500, 150))],
                [sg.Text(key="-INFO_SMILES-", size=50)]
                ])
        ]])

        col_info = sg.Column([
            [sg.Text("name_placeholder", size=self.standard_size),
             sg.Text(key="-INFO_NAME-", size=self.standard_size)],
            [sg.Text("company/research", size=self.standard_size),
             sg.Text(key="-INFO_origin_1", size=self.standard_size)],
            [sg.Text("what/who", size=self.standard_size),
             sg.Text(key="-INFO_origin_2", size=self.standard_size)],
            [sg.Text("volume left", size=self.standard_size),
             sg.Text(key="-INFO_MP_VOLUME-", size=self.standard_size)]
            ])

        layout = [[col_info, col_picture]]

        return layout

    def setup_table(self):
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

    def layout_tab_group_1(self):
        tab_1_search = sg.Tab("search", self.setup_1_search())
        tab_1_bio_data = sg.Tab("bio data", self.setup_1_bio())
        tab_1_purity_data = sg.Tab("purity data", self.setup_1_purity())
        tab_1_plate_layout = sg.Tab("Plate layout", self.setup_1_plate_layout())
        tab_1_add = sg.Tab("Update", self.setup_1_update())
        tab_1_sim = sg.Tab("Sim", self.setup_1_simulator())

        tab_group_1_list = [tab_1_search, tab_1_bio_data, tab_1_purity_data, tab_1_plate_layout, tab_1_add, tab_1_sim]

        return [[sg.TabGroup([tab_group_1_list], selected_background_color="purple")]]

    def layout_tab_group_2(self):
        layout_2_info = self.setup_2_info()
        layout_2_bio = [
            [sg.Text("this is tab group bio in tab layout 2")]
        ]
        layout_2_purity = [
            [sg.Text("this is tab group purity in tab layout 2")]
        ]

        tab_2_info = sg.Tab("Info", layout_2_info)
        tab_2_bio_bio = sg.Tab("bio data", layout_2_bio)
        tab_2_purity_purity = sg.Tab("purity data", layout_2_purity)

        tab_group_2_list = [tab_2_info, tab_2_bio_bio, tab_2_purity_purity]

        return [[sg.TabGroup([tab_group_2_list], selected_background_color="purple")]]

    def setup_experiment_table(self):

        layout = [[sg.Text("experiment table")]]
        return layout

    def setup_plate_table(self):

        layout = [[sg.Text("plate table")]]
        return layout

    def layout_tab_group_tables(self):
        layout_compound_table = self.setup_table()
        layout_experiment_table = self.setup_experiment_table()
        layout_plate_table = self.setup_plate_table()

        tab_table_compound = sg.Tab("Compound table", layout_compound_table)
        tab_experiment_table = sg.Tab("Experiment table", layout_experiment_table)
        tab_plate_table = sg.Tab("Plate tables", layout_plate_table)

        tab_group_tables = [tab_table_compound, tab_experiment_table, tab_plate_table]
        return [[sg.TabGroup([tab_group_tables], key="-TABLE_TAB_GRP-", enable_events=True, selected_background_color="purple")]]

    def full_layout(self):
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

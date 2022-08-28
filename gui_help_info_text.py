
class TextForInfo:
    def __init__(self, window, config):
        self.window = window
        self.headline_colour = "purple"
        self.sub_headline_colour = "blue"
        self.main_text_colour = "black"

        self.config = config

    def window_1_search_text(self):
        self.window["-INFO_HELP_SEARCH-"].update("Search\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "     Set up the search for compounds.\n"
            "     Either for checking out compounds, or for producing Mother/Daughter Plates.\n"
            "     This module is linked with the Compound Table.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nVendor/Reasearch DropDown\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Chooce between vendor or reasearch for the compound origian\n",
                                                 text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nSource DropDown\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Chooce the source for the compound.\n"
            "    Either a specific vendore, or a specific university\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nOutput folder\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Chooce the output folder for the export file.\n"
            "    The export button is located on the Compound Table tab\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nIgnore plated compounds?\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    If this is True, the result of the search will show all compounds\n"
            "    If this is False, it will not show compounds that are located in MotherPlates, "
            "that are set to active.\n"
            "    Active compounds are compounds with more liquid amount higher than deadvolume.\n"
            "    If Daughter Plates are choosen, this will ignore compounds in Daugther Plates\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nAmount of plates\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    How many plated is needed to be filled. \n"
            "    The base amount of compounds is set to be 384 times to plate amount.\n"
            "    If Daugther plates are choosen, then the amount of compounds per plate, "
            "will be depended on the plate layout choosen.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nTransferee Volume\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    How much volume is needed for the transferee. \n"
            "    The search result will only include compounds with enough liquid + "
            "deadvolume for the transferee to complete.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nPlate Production\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Choose what kinda of plate is being produced.\n"
            f"    Mother Plates are Plates {self.config['INFO']['MotherPlates']}.\n"
            f"    Daughter Plates are plates {self.config['INFO']['DaughterPlates']}",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\n\nStructure Search\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "     Set up the structur search for compounds.\n"
            "     This module is linked with the Compound Table.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nStructure Search\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Choose if structure search is used when searching for compounds\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nSmiles\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    The string representing the compound, that the results should be compared to.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nDraw Molecule\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Open ups a module for drawing the structure of the molecule.\n"
            "    This is not working yet :(",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nMethod\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    Choose what Sturcute search method to use.\n"
            f"    Finger: {self.config['INFO']['structure_search_finger']}\n"
            f"    Morgan: {self.config['INFO']['structure_search_morgan']}\n"
            f"    Dice: {self.config['INFO']['structure_search_dice']}\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nSimilarity Threshold\n",
                                                 text_color_for_value=self.sub_headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    How similar the resulting compounds should be to the Smiles-code.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SEARCH-"].update("\nAll Compounds\n",
                                                 text_color_for_value=self.headline_colour,
                                                 append=True)
        self.window["-INFO_HELP_SEARCH-"].update(
            "    If this is true. The search function will ignore all search parameters and "
            "get all the compounds from the main table.\n",
            text_color_for_value=self.main_text_colour, append=True)

    def window_1_bio_data_text(self):
        self.window["-INFO_HELP_BIO_DATA-"].update("Analyse setup\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "     Set up the import and export for bio experimental data. \n"
            "     The data is based on reading data from a TECAN plate reader.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nImport Folder\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Choose the folder where all the data is located.\n"
            "    Always needs a folder. Even for single files",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nExport Folder\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Choose the folder Where the final Report is saved to, and where all the imported files are moved to\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nPlate Layout\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Choose the layout used for the plates.\n"
            "    The layouts are created in the Plate Layout Tab. and it is showed in the Plate Layout Frame",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nAnalyse Method\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Choose what method to analyse the data with.\n"
            f"    Single Point:  {self.config['INFO']['bio_data_analyse_method_single_point']}\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nSample Type\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If 'Use Sample ID' is chosen:\n"
            "    It will use the Sample ID's or Compounds ID's depending on the state of 'Compound related data'\n"
            "    If 'Use layout' is chosen:\n"
            "    Choose the sample type for the analyse\n"
            f"    Single Point:  {self.config['INFO']['bio_data_analyse_method_single_point']}\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nExport\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Will analyse the imported files, add calculations and plate manipulations to the raw data file\n"
            "    If 'Combined Report' is True. It will also produce a Final report, "
            "with data from all the imported files\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nSend To Info\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Will analyse the data and send it to Bio Info, for closer examination.\n"
            "    After looking at the data, it is possible to export the data from Bio Info with chosen values.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\n\nExtra Settings\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "     Settings for Exporting data'. \n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nCombined Report\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If True, then the Export, will make a Final Report, with combined data from all the imported files\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nReport Settings\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Settings for how the reports should look like, what data to include and so on.\n"
            "    Both settings for the Finale Report and for the single plate reports",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nCompound Related Data\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If True, then the database will add the data to the specific compounds\n"
            "    This data will always be added to the database... \n"
            "    THIS HAVE NOT BEEN SETUP YET... AS I DO NOT KNOW HOW IT WILL WORK :D \n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nAdd To Database\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If True. The Data will be added to the Bio Experimental table.\n"
            "    The data will be saved, and can be looked at later.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nReport Name\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Name of the Final Report.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nAssay Name\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If the data will be added to the database, "
            "then this is the name of that assay to save the data under\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nResponsible\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    The person that have run the experiment\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nAdd Compound Info To The Final Report\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    If True. The Final Report will have the Compound ID/Sample ID in the well info column.\n"
            "    If it is compound related data, it will pull the Compound ID's from the database. \n"
            "    If it not compound related data, it will need to import a sample list.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\nImport Sample List\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "    Only needed if 'Add Compound info to Final Report' is True.\n"
            "    Takes an Excel sheet with a list of well_ID and a list of Sample_ID's\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_DATA-"].update("\n\nPlate Layout\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_DATA-"].update(
            "     Shows the plate layout chosen under 'Plate Layout'. \n"
            "     The Info below, Shows what well state corresponds to witch colour.\n"
            "     It is possible to draw plates with all colours. So any colour not found on the List below, will not "
            "have a corresponds state, and can't be used for the analyse.\n",
            text_color_for_value=self.main_text_colour, append=True)

    def window_1_purity_data_text(self):
        ...

    def window_1_plate_layout_text(self):
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Plate Layout\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     The Plate Layout drawing module.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("\nPlate Size\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "    Sets the size of the plate\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("\nDraw Plate\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "    Draws the plate on the Canvas, depending on chosen values\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("\nActive Move+\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "    If True, will print out coordinates and wells below the Plate Layout\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("\n\nOptions\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     Sets the Drawing tools for the Plate Layout\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("\nRadio Buttons\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "    Choose the 'state' that is the draw with.\n"
            "    This will be saved for used with the analysing tool\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Colour\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     If chosen, make it possible to colour the plate in different colours.\n"
            "     If this is used, the plates can't be used for analysing data. Should only be used for Export\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Use Archive\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     If True: When 'Draw Plate' it will draw the plate chosen in the dropdown menu.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Delete Layout\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     Will delete the layout chosen in the Archive dropdown\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Rename Layout\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     Will rename the layout chosen in the Archive dropdown\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Save Layout\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     Will Save the layout drawn on the Plate Layout canvas.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_PLATE_LAYOUT-"].update("Export\n",
                                                 text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_PLATE_LAYOUT-"].update(
            "     Will export the layout to an excel file\n",
            text_color_for_value=self.main_text_colour, append=True)

    def window_1_update_text(self):
        self.window["-INFO_HELP_UPDATE-"].update("Update\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            "     Uploading files to the database or updating the database.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_UPDATE-"].update("\nBrowse\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            "    Chose the folder with the data that needs to be imported\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_UPDATE-"].update("\nAdd Compounds\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            "    Add compounds to the database\n"
            "    Takes sdf-files with compounds information from vendors.\n"
            "    or excel files with compound information - This is not setup yet.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_UPDATE-"].update("\nAuto\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            f"    Will go through the folder: {self.config['folders']['main_import_folder']}\n"
            "    Then for each sub-folder, will add data that corresponds to the sub-folder.\n"
            f"    Will move the all the data to {self.config['folders']['main_output_folder']} after import.\n"
            "     This is not working yet",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_UPDATE-"].update("\nAdd Mother Plates\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            "    Will add Mother Plates to the database\n"
            "    Takes Plate Butler files\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_UPDATE-"].update("\nAdd Daughter Plates\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_UPDATE-"].update(
            "    Will add Daughter Plates to the database\n"
            "    Takes Echo files\n",
            text_color_for_value=self.main_text_colour, append=True)

    def window_1_sim_text(self):
        self.window["-INFO_HELP_SIM-"].update("Simulate\n", text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_SIM-"].update(
            "     Simulate data generated by different systems.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_SIM-"].update("\nDropDown\n",
                                                 text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_SIM-"].update(
            "    comPOUND: Simulate data generated after Tubes have been taken from the comPOUND freezer and scanned"
            "on a 2-D QR-code plate scanner.\n"
            "    Takes a list of compounds. \n"
            "    MP Production: Simulate the output files from the Plate Butler, after a Mother Plate Production. \n"
            "    Take 2-D QR-codes txt-files and MP initials.\n"
            "    DP Production: Simulate DP production\n"
            "    Takes PB files and initials",
            text_color_for_value=self.main_text_colour, append=True)

    def window_2_info_text(self):
        ...

    def window_2_bio_info_text(self):
        self.window["-INFO_HELP_BIO_INFO-"].update("Bio Information\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows information for a assay.\n"
            "     The data is either pulled from the Bio Experimental table or from the Bio Data tab.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nActive Move+\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    If True, will print well information, below the plate layout, when hovering over wells,\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nExport\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    Will Generate a report file over current data\n"
            "    THIS HAVE NOT BEEN SET UP YET... \n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nAnalyse Method\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    Shows data in Plate Layout, depending on what analysis have been done on the data\n"
            f"    Original: {self.config['INFO']['bio_data_analyse_method_original']}\n"
            f"    Normalised: {self.config['INFO']['bio_data_analyse_method_normalised']}\n"
            f"    Pora: {self.config['INFO']['bio_data_analyse_method_pora']}\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nPlate Mapping\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    Colours the plate layout depending on the choose\n"
            f"    State Mapping: {self.config['INFO']['bio_info_plate_mapping_state_map']}\n"
            f"    Heatmap: {self.config['INFO']['bio_info_plate_mapping_heatmap']}\n"
            f"    Hit Map: {self.config['INFO']['bio_info_plate_mapping_hit_map']}\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nPlate\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    A list of plates in the assay\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nState\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "    Choose witch state to show basic information for, that is just below the plate layout\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nPlate Layout\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows the layout for the Chosen analysis.\n"
            "     With the data from the specified analyse method and state.\n"
            "     All information below the Plate Layout is depending on the options chosen above plate layout\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nTab Group\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Different tabs to show different data for the analysis and plates..\n"
            "     Values used through out the menus:\n"
            "     Barcode: Is the Barcode for the different plates\n"
            "     avg: Average over all wells included in the calculation.\n"
            "     stdev: Standard deviation for all wells included in the calculation.\n"
            "     Z-Prime: Z-Prime calculation for the plate.",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nMapping\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Settings for map colours on the plate layout\n"
            "     These settings will be used if the data is exported for all reports\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHeatmap Settings\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Setting for the Heatmap\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHeatmap Colours\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Set the colours for the heatmap.\n"
            "     It will go from low value-colour to mid value-colour, "
            "and from mid value-colour to high value-colour\n"
            "     It will go in a linear gradient\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHeatmap Values\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Sets the values range in percentage for when a well will get a specific colour.\n"
            "     The low and high bound, will go from 0-low and from high-100. \n"
            "     All values within that percentile will have the low or high colour.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHit Map Settings\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Setting for the hit map\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHit Map Values\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Sets the boundaries for when to colour wells.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nHit Map Colours\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Set the colours for the plate layout.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nStates For Mapping\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Chose with well-state will be included in the mapping.\n"
            "     Any well-state not included or value not within bounds, will be white\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nOverview\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows calculations for all plates depending on analyse method and state\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nPlate Overview\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows calculations for all plates depending on analyse method and state\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nZ-Prime\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows Z-Prime for all plates in different ways.\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\n\nMatrix\n",
                                                   text_color_for_value=self.headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Shows a Matrix over Values from each plate compared with each other. The values in percentage\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nGenerate Matrix\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Will generate Matrix depending on the values chosen\n",
            text_color_for_value=self.main_text_colour, append=True)

        self.window["-INFO_HELP_BIO_INFO-"].update("\nPop Out The Matrix\n",
                                                   text_color_for_value=self.sub_headline_colour, append=True)
        self.window["-INFO_HELP_BIO_INFO-"].update(
            "     Will call a popup window to get a bigger window to look at the Matrix for.\n",
            text_color_for_value=self.main_text_colour, append=True)



    def window_2_purity_info_text(self):
        ...

    def window_3_compound_table_text(self):
        ...

    def window_3_bio_exp_table_text(self):
        ...

    def window_3_plate_table_text(self):
        ...

    def glossary(self):
        ...

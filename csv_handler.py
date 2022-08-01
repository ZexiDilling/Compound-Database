import csv
from datetime import date
from math import ceil
import os

import info
from info import *
from plate_formatting import mother_plate_generator as mpg


class CSVWriter:
    def __str__(self):
        """
        Writes CSV files
        :return: CSV files, in different formate.
        """

    @staticmethod
    def compound_freezer_writer(path, compound_list):
        """
        Writes the tube file for the comPOUND freezer
        :param path: main output folder
        :param compound_list: list of compounds
        :return: CSV for the comPOUND freezer, to fetch tubes
        """
        try:
            os.mkdir(f"{path}/comPOUND")
        except OSError:
            print("directory exist")

        path = f"{path}/comPOUND"

        file_name = f"comPOUND_'{date.today()}'.txt"
        complete_file_name = os.path.join(path, file_name)
        with open(complete_file_name, "w+", newline="\n") as f:
            csv_writer = csv.writer(f)
            for compound in compound_list:
                csv_writer.writerow([compound])

    @staticmethod
    def mp_workflow_handler(path, compound_list, plate_layout, tube_rack_list, samples_per_plate=96):
        """
        Generate a dict of tubes and their placement in a plate
        :param path: Main output folder
        :param compound_list: List of compounds
        :param plate_layout: Layout for the plate to get well information. is pulled from INFO!
        :param tube_rack_list: Barcode for the tube-racks
        :param samples_per_plate: How many samples there are per plate. Should always be 96.
        :return: A dict of tubes with what rack they are in, and what well/spot in that rack.
        and A CSV file for PlateButler to run the MotherPlate protocol.
        """
        tube_dict = {}
        try:
            os.mkdir(f"{path}/mp_files_{date.today()}")
        except OSError:
            print("directory exist")

        path = f"{path}/mp_files_{date.today()}"

        counter_compounds = 0
        if not tube_rack_list:
            plate_amount = len(compound_list)/samples_per_plate
            plate_amount = ceil(plate_amount)
            tube_rack_list = []
            for i in range(plate_amount):
                tube_rack_list.append(i+1)
        for plate in tube_rack_list:
            tube_dict[plate] = {}
            file_name = f"{path}/{plate}.txt"
            with open(file_name, "w", newline="\n") as f:
                csv_writer = csv.writer(f, delimiter=";")
                csv_writer.writerow(["RowCol", "tubeBarcode"])
                for index, _ in enumerate(compound_list):
                    if counter_compounds <= len(compound_list):
                        if index < samples_per_plate:
                            tube_dict[plate][plate_layout[index]] = compound_list[counter_compounds]
                            csv_writer.writerow([plate_layout[index], compound_list[counter_compounds]])
                            counter_compounds += 1

        return tube_dict

    @staticmethod
    def mp_to_pb_writer(path, mp_plates):
        """
        Writes the output file from the PlateButler to double check if things looks fine.
        CAN BE DELEDET!
        :param path: Main Output folder
        :param mp_plates: Dict with information about what tubes goes into witch well. from 4 x 96 to 384.
        :return: CSV file, to compare with PlateButler output file
        """

        try:
            os.mkdir(f"{path}/pb_output")
        except OSError:
            print("directory exist")

        path = f"{path}/pb_output"
        file_name = f"{path}/pb_mp_generated_output_{date.today()}.csv"
        with open(file_name, "w", newline="\n") as f:
            csv_writer = csv.writer(f, delimiter=";")
            for mp_barcode in mp_plates:
                for values in mp_plates[mp_barcode]:
                    csv_writer.writerow([mp_barcode, *values])

    def compound_freezer_handler(self, path, compound_list, mp_name, tube_rack_list=None, plate_layout=None):
        """
        Generate CSV files for the comPOUND freezer and PlateButler for producing MotherPlates
        :param path: Main Output folder
        :param compound_list: List of compounds
        :param mp_name: Main name for MotherPlates.
        :param tube_rack_list: List of barcodes for racks
        :param plate_layout: Layout for the plate to get well information. is pulled from INFO!
        :return: 3 CSV files. One for the comPOUND freezer to fetch tubes, one for PlateButler to run the protocol,
        1 for comparing output files from PlateButler with Theoretical output
        """
        if not plate_layout:
            plate_layout = info.plate_96
        self.compound_freezer_writer(path, compound_list)

        # tube_dict = self.mp_workflow_handler(path, compound_list, plate_layout, tube_rack_list)
        # _, pb_mp_output = mpg(tube_dict, mp_name)
        # self.mp_to_pb_writer(path, pb_mp_output)

    @staticmethod
    def dp_writer(dp_dict, path):
        """
        Writes CSV file for PlateButler protocol for producing DaughterPlates
        :param dp_dict: Dict over compounds. Source and Destination info and volume to transferee
        :param path: Main output folder
        :return: CSV file for PlateButler to run Assay production Protocol.
        """
        path = f"{path}/pb_output"
        file_name = f"{path}/pb_db_generated_output_{date.today()}.csv"

        with open(file_name, "w", newline="\n") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            csv_writer.writerow(["DestinationBarcode", "DestinationWell", "Volume", "SourceWell", "SourceBarcode", "CompoundID"])

            for destination_plate in dp_dict:
                for destination_well, vol, source_well, source_sample, plate in dp_dict[destination_plate]:
                    csv_writer.writerow([destination_plate, destination_well, vol, source_well, plate, source_sample])


class CSVReader:
    def __str__(self):
        """
        Reads CSV files
        :return: Dict's with information.
        """

    @staticmethod
    def _pb_mp_output_files(file):
        """
        Reads the output file from PlateButler. When running MotherPlates Production
        :param file: PlateButler output file
        :return: 2 dict. 1 for the data and 1 for the plates
        """
        headline = ["DestinationBarcode", "DestinationWell", "compoundID", "Volume"]
        dict_data = {}
        destination_plates = {}
        with open(file) as f:
            for row_index, line in enumerate(f):
                values = line.split(";")
                dict_data[f"Transferee_{row_index}"] = {}
                for clm_index, value in enumerate(values):
                    dict_data[f"Transferee_{row_index}"][headline[clm_index]] = value.strip("\n")
                    if headline[clm_index] == "DestinationBarcode":
                        destination_plates[value] = {}
                        destination_plates[value]["DestinationBarcode"] = value
                        destination_plates[value]["date"] = date.today()

        return dict_data, destination_plates

    @staticmethod
    def pb_tube_files_ind(file, tube_dict):
        """
        Reads Tube files from 2D-scanner
        :param file: Tube files
        :param tube_dict: Dict for the tubes
        :return: The tube dict, updated with information
        """
        plate = file.split("/")
        plate = plate[-1]
        plate = plate.removesuffix(".txt")
        tube_dict[plate] = {}
        with open(file) as f:
            for line in f:
                values = line.split(";")
                if values != ['RowCol', 'tubeBarcode\n']:
                    tube_dict[plate][values[0]] = values[1].strip("\n")

    @staticmethod
    def _tab_file_reader(file):
        """
        Reads CSV file with tab format that PlateButler prefer to read.
        :param file: CSV file that needs to be read
        :return: 2 dict. 1 for data, 1 for plates
        """
        counter = -1
        headline = []
        dict_data = {}
        destination_plates = {}
        with open(file) as f:

            for line in f:
                counter += 1
                values = line.split("\t")
                if counter > 0:
                    dict_data[f"Transferee_{counter}"] = {}
                for index, value in enumerate(values):
                    if value != "\n":
                        if counter == 0:

                            headline.append(value.strip("\n"))

                        else:
                            dict_data[f"Transferee_{counter}"][headline[index]] = value.strip("\n")

                            if headline[index] == "DestinationBarcode":
                                destination_plates[value] = {}
                                destination_plates[value]["DestinationBarcode"] = value.strip("\n")
                                destination_plates[value]["date"] = date.today()
                                #destination_plates[clm_info]["location"] = "Freezer-1"

        return dict_data, destination_plates

    def csv_r_controller(self, csv_file, file_type):
        """
        Handles the CSV reader to get files where they needs to go. Could be deleted.
        :param csv_file: The CSV file that needs  to be read
        :param file_type: What kind of CSV file it is
        :return: 2 dict. 1 for data, 1 for plates
        """
        if file_type == "tab":
            dict_data, destination_plates = self._tab_file_reader(csv_file)
        elif file_type == "pb_mp_output":
            dict_data, destination_plates = self._pb_mp_output_files(csv_file)
        return dict_data, destination_plates


class CSVConverter:

    def __str__(self):
        """Convert CSV files to other formate"""

    @staticmethod
    def mp_in_to_out(path, barcodes_2d_files, mp_name, trans_vol):
        """
        Convert Tube files from MotherPlate Files to a CSV file for PlateButler, incase some files are missing.
        :param path: Main Output folder
        :type path: str
        :param barcodes_2d_files: list of 2d barcode files
        :type barcodes_2d_files: list
        :param mp_name: MotherPlate main name.
        :type mp_name: str
        :return: None
        """
        tube_dict = {}
        for files in barcodes_2d_files:
            CSVReader.pb_tube_files_ind(files, tube_dict)

        _, pb_mp_output = mpg(tube_dict, mp_name, trans_vol)
        print(pb_mp_output)

        CSVWriter.mp_to_pb_writer(path, pb_mp_output)


if __name__ == "__main__":
    file_input_1 = "tube_test_file - Copy.txt"
    file_input_2 = "20220609_114040 - Copy.txt"

    file_type_2 = "pb_mp"
    file_type_1 = "tab"

    csv = CSVReader()
    print(csv.controller(file_input_1, file_type_1))
    print(csv.controller(file_input_2, file_type_2))


    # csvw = CSVWriter()
    # csvw.compound_handler(com_list)



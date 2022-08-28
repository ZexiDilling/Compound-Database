from openpyxl import Workbook
import numpy as np
from openpyxl.styles import Font

from openpyxl_fix_functions import *


def _cal_writer_final_report(barcode, ws, all_data, init_row, init_col, report_output):
    """
    Writes the calculations in the combined report for all the plates

    :param barcode: The barcode for the plate
    :type barcode: str
    :param ws: The worksheet for the excel filere where the data is added
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param all_data: A dict over all plate date. all the analysed data will be added to this dict
    :type all_data: dict
    :param init_row: The first row to write to in the excel file
    :type init_row: int
    :param init_col: The first row to write to in the excel file
    :type init_col: int
    :param report_output: Gate dict for what information to write. is set in the settings
    :type report_output: dict
    :return: The overview report page in the final report.
    row_counter: The last row writen in
    :rtype: int
    """

    row_counter = init_row

    merge_cells_single_row(barcode, ws, row_counter, init_col, init_col + 2)
    ws.cell(column=init_col, row=row_counter, value=barcode).font = Font(b=True, underline="single")
    row_counter += 1
    for plate_analysed in all_data["calculations"]:
        # Removing other calculations than avg and stdev
        if plate_analysed != "other":
            # Checks to see if the overview of avg and stv should be included
            if report_output[plate_analysed]["overview"]:
                # Writes the analysed method in, if the overview is set to true
                merge_cells_single_row(plate_analysed, ws, row_counter, init_col, init_col + 2, True, "red_line")
                row_counter += 1
                for state in all_data["calculations"][plate_analysed]:
                    if report_output[plate_analysed][state]:
                        ws.cell(column=init_col, row=row_counter, value=state).font = Font(b=True)
                        for calc in all_data["calculations"][plate_analysed][state]:
                            # Writes avg and stdev including values
                            ws.cell(column=init_col + 1, row=row_counter, value=calc)
                            ws.cell(column=init_col + 2, row=row_counter,
                                    value=all_data["calculations"][plate_analysed][state][calc])
                            row_counter += 1
        else:
            if report_output["z_prime"]:
                ws.cell(column=init_col, row=row_counter, value="z-Prime").font = Font(b=True)
                try:
                    ws.cell(column=init_col + 2, row=row_counter,
                            value=all_data["calculations"][plate_analysed]["z_prime"])
                except KeyError:
                    ws.cell(column=init_col + 2, row=row_counter,
                            value="Z-Prime is not calculated for the plates")
                row_counter += 1
            row_counter += 1
    return row_counter


def _well_writer_final_report(ws, hits, final_report_setup, init_row):
    """
    Writes all the wells in a list, in the excel file, for the values that are within the predetermined values.

    :param ws: The worksheet for the excel filere where the data is added
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param hits: A dict over all the values that are "hits" and needs to be added
    :type hits: dict
    :param final_report_setup: Gate for what data is added to the report. Is setting in the settings
    :type final_report_setup: dict
    :param init_row: The first row to write to.
    :type init_row: int
    :return: A list of wells in the excel sheet.
    """
    indent_col = 1
    row_counter = init_row

    for barcode in hits:
        # Writes headline for data inserts to see where the data is coming from
        ws.cell(column=indent_col, row=row_counter, value=barcode).font = Font(b=True, underline="single")
        row_counter += 1

        for method in hits[barcode]:
            if final_report_setup["methods"][method]:
                # writes method
                ws.cell(column=indent_col, row=row_counter, value=method).font = Font(b=True)
                row_counter += 1
                for split in hits[barcode][method]:
                    ws.cell(column=indent_col, row=row_counter, value=split).font = Font(b=True)
                    ws.cell(column=indent_col+1, row=row_counter,
                                   value=final_report_setup["pora_threshold"][split]["min"]).font = \
                        Font(underline="single")
                    ws.cell(column=indent_col+2, row=row_counter,
                                   value=final_report_setup["pora_threshold"][split]["max"]).font = \
                        Font(underline="single")
                    row_counter += 1
                    for well in hits[barcode][method][split]:
                        ws.cell(column=indent_col + 1, row=row_counter, value=well)
                        ws.cell(column=indent_col + 2, row=row_counter,
                                       value=hits[barcode][method][split][well])
                        row_counter += 1
        indent_col += 4
        row_counter = init_row


def _get_data(all_plate_data, final_report_setup):
    """
    Grabs data that are needed for the different output sheets in the excel file.

    :param all_plate_data: The data for all the plates.
    :type all_plate_data: dict
    :param final_report_setup: The settings for the final report. is set in the settings.
    :type final_report_setup: dict
    :return:
        - temp_hits: All the hits that are within the values
        - data_calc_dict: A dicts over all the calculations and the values
        - plate_counter: The amount of plates that are being analysed
        - all_states: The states that are being used for the analysis
        - all_methods: The methods that are being used for the analysis
    :rtype:
        - dict
        - dict
        - int
        - dict
        - dict
    """
    data_calc_dict = {}
    temp_hits = {}
    plate_counter = 0
    all_states = []
    all_methods = []

    for barcode in all_plate_data:
        plate_counter += 1
        temp_hits[barcode] = {}
        data_calc_dict[barcode] = {}
        for method in all_plate_data[barcode]["plates"]:
            if method != "other":
                if method not in all_methods:
                    all_methods.append(method)
            if final_report_setup["methods"][method]:
                temp_hits[barcode][method] = {"low": {}, "mid": {}, "high": {}}
                for well in all_plate_data[barcode]["plates"][method]["wells"]:
                    if well in all_plate_data[barcode]["plates"][method]["sample"]:
                        for split in final_report_setup["pora_threshold"]:
                            temp_well_value = all_plate_data[barcode]["plates"][method]["wells"][well]
                            if float(final_report_setup["pora_threshold"][split]["min"]) < float(temp_well_value) < \
                                    float(final_report_setup["pora_threshold"][split]["max"]):
                                temp_hits[barcode][method][split][well] = temp_well_value

        for method in all_plate_data[barcode]["calculations"]:
            data_calc_dict[barcode][method] = {}
            if method != "other":
                for state in all_plate_data[barcode]["calculations"][method]:
                    if state not in all_states:
                        all_states.append(state)

                    data_calc_dict[barcode][method][state] = {}
                    for calc in all_plate_data[barcode]["calculations"][method][state]:
                        data_calc_dict[barcode][method][state][calc] = \
                            all_plate_data[barcode]["calculations"][method][state][calc]

            else:
                for other_calc in all_plate_data[barcode]["calculations"][method]:
                    data_calc_dict[barcode][method][other_calc] = \
                        all_plate_data[barcode]["calculations"][method][other_calc]

    return temp_hits, data_calc_dict, plate_counter, all_states, all_methods


def _data_writer(ws_matrix, ws_list, data_calc_dict, state, plate_counter, all_methods, use_list, use_max_min):
    """
    Writes all the data, and handles the flow of the data to witch sheet different things are writen in.

    :param ws_matrix: The Worksheet for the data that goes in Matrix formate for calculations
    :type ws_matrix: openpyxl.worksheet.worksheet.Worksheet
    :param ws_list: The worksheet that list calculations and the min/max values for the different once
    :type ws_list: openpyxl.worksheet.worksheet.Worksheet
    :param data_calc_dict: All the data in a dict formate
    :type data_calc_dict: dict
    :param state: What state the data is for (samples, minimum, maximum, blank...)
    :type state: str
    :param plate_counter: The amount of plates that are being analysed
    :type plate_counter: int
    :param all_methods: A list of all the methods
    :type all_methods: list
    :param use_list: If the list data should be added to the report. Is set in the settings.
    :type use_list: bool
    :param use_max_min: If the min_max data should be added to the report. Is set in the settings.
    :type use_max_min: bool
    :return: Values written into the excel sheet for the Matrix, and the list and or min_max depending on settings
    """
    init_row = 4
    init_col = 3
    spacer = 4
    list_spacer_clm = 6

    col_stdev = init_col + plate_counter + spacer
    col_counter = init_col + 1
    row_counter = init_row + 1
    col_stdev_counter = col_stdev + 1
    row_offset = init_row

    list_clm = init_col - 1
    list_row = init_row

    list_row_minmax = init_row

    for index_m, method in enumerate(all_methods):
        temp_avg_dict = {}
        temp_stdev_dict = {}
        mw_col = col_counter
        mw_row = row_counter
        mw_col_stdev = col_stdev_counter

        for barcodes in data_calc_dict:
            # Writes Plate names in row and clm for avg
            ws_matrix.cell(column=init_col - 1, row=row_counter, value=barcodes).font = Font(b=True)
            ws_matrix.cell(column=col_counter, row=row_offset - 1, value=barcodes).font = Font(b=True)

            # Writes Plate names in row and clm for stdev
            ws_matrix.cell(column=col_stdev - 1, row=row_counter, value=barcodes).font = Font(b=True)
            ws_matrix.cell(column=col_stdev_counter, row=row_offset - 1, value=barcodes).font = Font(b=True)

            for index_method, _ in enumerate(data_calc_dict[barcodes]):

                if index_method == 0:
                    # Writes method for avg
                    ws_matrix.cell(column=init_col, row=row_offset - 1, value=method).font = Font(b=True)
                    # Writes method for stdev
                    ws_matrix.cell(column=col_stdev, row=row_offset - 1, value=method).font = Font(b=True)
                    if method != "other":
                        for calc in data_calc_dict[barcodes][method][state]:
                            temp_value = data_calc_dict[barcodes][method][state][calc]
                            # gets avg values
                            if calc == "avg":
                                ws_matrix.cell(column=init_col, row=row_offset, value=calc).font = Font(b=True)
                                ws_matrix.cell(column=init_col, row=row_counter, value=temp_value)
                                ws_matrix.cell(column=col_counter, row=row_offset, value=temp_value)
                                temp_avg_dict[barcodes] = temp_value
                            elif calc == "stdev":
                                ws_matrix.cell(column=col_stdev, row=row_offset, value=calc).font = Font(b=True)
                                ws_matrix.cell(column=col_stdev, row=row_counter, value=temp_value)
                                ws_matrix.cell(column=col_stdev_counter, row=row_offset, value=temp_value)
                                temp_stdev_dict[barcodes] = temp_value
            # Sets offset for next loop, for writing headlines the right place
            col_counter += 1
            row_counter += 1
            col_stdev_counter += 1

        # calculate the % difference between avg for each plate
        _matrix_calculator(ws_matrix, mw_row, mw_col, temp_avg_dict)
        # calculate the % difference between stdev for each plate
        _matrix_calculator(ws_matrix, mw_row, mw_col_stdev, temp_stdev_dict)

        # sortes the dict by size
        temp_avg_dict = _sort_dict(temp_avg_dict)
        temp_stdev_dict = _sort_dict(temp_stdev_dict)

        # writes list of all avg for the different methods
        if use_list:
            _writes_list_of_values(ws_list, list_row, list_clm, temp_avg_dict, "avg", method)
            _writes_list_of_values(ws_list, list_row, list_clm + 3, temp_stdev_dict, "stdev", method)

        # Calculate how much space the list takes
        list_clm = (list_spacer_clm * (len(all_methods))) + 2

        # writes list of all avg for the different methods
        if use_max_min:
            _write_min_max_values(ws_list, list_row_minmax, list_clm, temp_avg_dict, "avg", method)
            _write_min_max_values(ws_list, list_row_minmax, list_clm + 4, temp_stdev_dict, "stdev", method)


        # makes sure that next loop is writen below the first method. One method per row, with avg and stdev for each.
        col_stdev = init_col + plate_counter + spacer
        col_counter = init_col + 1
        row_counter += spacer
        col_stdev_counter = col_stdev + 1
        row_offset += (plate_counter + spacer)
        list_row_minmax += 5
        list_clm = init_col - 1 + (list_spacer_clm * (index_m + 1))


def _matrix_calculator(ws, row, col, temp_data_dict):
    """
    Calculates and writes the values for the Matrix

    :param ws: The Worksheet for the data that goes in Matrix formate for calculations
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param row: The row for the locations of the matrix
    :type row: int
    :param col: The col for the locations of the matrix
    :type col: int
    :param temp_data_dict: The data for the matrix
    :type temp_data_dict: dict
    :return: Written a matrix in the final report for the excel file
    """

    for index_x, value_x in enumerate(temp_data_dict):
        for index_y, value_y in enumerate(temp_data_dict):
            try:
                temp_value = (float(temp_data_dict[value_x]) / float(temp_data_dict[value_y])) * 100
            except (ZeroDivisionError, TypeError):
                temp_value = None
            ws.cell(column=col + index_x, row=row + index_y, value=temp_value)


def _sort_dict(temp_data_dict):
    """
    This sorts the dict from lowest values to highest

    :param temp_data_dict: The data for the hit wells.
    :type temp_data_dict: dict
    :return: a sorted dict
    :rtype: dict
    """
    try:
        return {key: value for key, value in sorted(temp_data_dict.items(), key=lambda item: item[1])}
    except TypeError:
        return temp_data_dict


def _writes_list_of_values(ws, row, col, temp_data_dict, item_name, method=None):
    """
    Writes the hit values in a list.
    NEEDS TO ADD COMPOUND DATA TO THIS AT SOME POINT!!!

    :param ws: The Worksheet for the data, for the excel file
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param row: The row where the data is start being written
    :type row: int
    :param col: The col where the data is start being written
    :type col: int
    :param temp_data_dict: The data that needs to be writen. A dict of wells and their values
    :type temp_data_dict: dict
    :param item_name: The name for the data type. avg or stdev
    :type item_name: str
    :param method: What methods the data is from
    :type method: str
    :return: Data written in the excel file.
    """

    # writes method
    if method:
        merge_cells_single_row(method, ws, row - 2, col, col + 1, True, "red_line")

    # writes headline for the list
    ws.cell(column=col, row=row - 1, value="Barcode").font = Font(b=True)
    ws.cell(column=col + 1, row=row - 1, value=item_name).font = Font(b=True)
    # writes list of values and barcode / plate name
    row_counter = 0
    for index, values in enumerate(temp_data_dict):

        ws.cell(column=col, row=row + index, value=values)
        ws.cell(column=col + 1, row=row + index, value=temp_data_dict[values])
        row_counter += 1

    table_name = f"{item_name}_{method}"
    start_row = row - 1
    end_row = start_row + row_counter
    ws.add_table(table_purple(ws, table_name, start_row, col, end_row, col + 1))


def _write_min_max_values(ws, row, col, data_dict, item_name, method=None):
    """
    Writes the min and max values in the list sheet

    :param ws: The Worksheet for the data, for the excel file
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param row: The row where the data is start being written
    :type row: int
    :param col: The col where the data is start being written
    :type col: int
    :param item_name: The name for the data type. avg or stdev
    :type item_name: str
    :param method: What methods the data is from
    :type method: str
    :return: Data written in the excel file.
    """

    # writes method
    if method:
        merge_cells_single_row(method, ws, row - 2, col, col + 2, True, "red_line")

    # writes headlines
    ws.cell(column=col + 1, row=row - 1, value="Barcode").font = Font(b=True)
    ws.cell(column=col + 2, row=row - 1, value=item_name).font = Font(b=True)
    ws.cell(column=col, row=row, value="Maximum").font = Font(b=True)
    ws.cell(column=col, row=row + 1, value="Minimum").font = Font(b=True)

    # removes None values:
    temp_data_dict = {}
    for keys in data_dict:
        if data_dict[keys]:
            temp_data_dict[keys] = data_dict[keys]

    # writes max and barcode / plate name
    temp_dict_max = max(temp_data_dict, key=temp_data_dict.get)

    ws.cell(column=col + 1, row=row, value=temp_dict_max)
    ws.cell(column=col + 2, row=row, value=temp_data_dict[temp_dict_max])

    # writes max and barcode / plate name
    temp_dict_min = min(temp_data_dict, key=temp_data_dict.get)
    ws.cell(column=col + 1, row=row + 1, value=temp_dict_min)
    ws.cell(column=col + 2, row=row + 1, value=temp_data_dict[temp_dict_min])


def _z_prime(ws, data_calc_dict, use_list, use_max_min):
    """
    Writes the Z-Prime report page in the final report

    :param ws: The Worksheet for the data, for the excel file
    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :param data_calc_dict: A dict over all the Z-Prime values
    :type data_calc_dict: dict
    :param use_list: If the list data should be added to the report. Is set in the settings.
    :type use_list: bool
    :param use_max_min: If the min_max data should be added to the report. Is set in the settings.
    :type use_max_min: bool
    :return: All the data for the Z-Prime in its own sheet in the final report excel file.
    """

    init_row = 2
    init_col = 2
    spacer = 1

    matrix_col = init_col + 8
    matrix_row = init_row + spacer

    col_counter = matrix_col + spacer
    row_counter = matrix_row + spacer

    z_prime_dict = {}

    for barcodes in data_calc_dict:
        # Writes Plate names
        ws.cell(column=matrix_col-1, row=row_counter, value=barcodes).font = Font(b=True)
        ws.cell(column=col_counter, row=matrix_row-1, value=barcodes).font = Font(b=True)
        # Writes values for Z-Prime
        z_prime = data_calc_dict[barcodes]["other_data"]["z_prime"]
        ws.cell(column=matrix_col, row=row_counter, value=z_prime)
        ws.cell(column=col_counter, row=matrix_row, value=z_prime)
        col_counter += 1
        row_counter += 1
        # z_prime_list.append(z_prime)
        z_prime_dict[barcodes] = z_prime

    col_counter = init_col + 1
    row_counter = init_row + 1

    # _matrix_calculator(ws, row_counter, col_counter, z_prime_list)
    _matrix_calculator(ws, matrix_row + 1, matrix_col + 1, z_prime_dict)

    z_prime_dict = _sort_dict(z_prime_dict)
    if use_list:
        _writes_list_of_values(ws, row_counter, init_col, z_prime_dict, "z_prime")
    if use_max_min:
        _write_min_max_values(ws, row_counter, col_counter + 2, z_prime_dict, "z_prime")


def bio_final_report_controller(analyse_method, all_plate_data, output_file, final_report_setup):
    """
    The controller for the flow of data, that writes the final report in an excel file.

    :param analyse_method: What analyse method is being used.
    :type analyse_method: str
    :param all_plate_data: All the data for all the plates, including calculations and well states
    :type all_plate_data: dict
    :param output_file: The name and path for the final report
    :type output_file: str
    :param final_report_setup: The settings for the final report.
    :type final_report_setup: dict
    :return: An excel file ready to be presented... or something..
    """
    wb = Workbook()
    ws_report = wb.active
    ws_report.title = "Full report"
    ws_well_info = wb.create_sheet("Well Info")
    ws_z_prime = wb.create_sheet("Z-Prime")

    init_row = 2
    init_col = 2
    row = init_row
    col = init_col
    # calc overview:

    for index, barcode in enumerate(all_plate_data):
        row_counter = _cal_writer_final_report(barcode, ws_report, all_plate_data[barcode], row, col,
                                               final_report_setup["calc"])
        # Writes 5 plates horizontal, before changing rows.
        col += 4

        if index % 5 == 0 and index > 0:
            row += row_counter
            col = init_col

    # gets data:
    temp_hits, data_calc_dict, plate_counter, all_states, all_methods = _get_data(all_plate_data, final_report_setup)

    # write well data
    _well_writer_final_report(ws_well_info, temp_hits, final_report_setup, init_row)

    # writes Matrix of data:

    for states in all_states:
        if final_report_setup["data"][states]["matrix"]:

            _data_writer(ws_creator(wb, states, "Matrix"), ws_creator(wb, states, "Lists"), data_calc_dict, states,
                         plate_counter, all_methods, final_report_setup["data"][states]["list"],
                         final_report_setup["data"][states]["max_min"])

    # writes Z-prime
    if final_report_setup["data"]["z_prime"]["matrix"]:
        _z_prime(ws_z_prime, data_calc_dict, final_report_setup["data"]["z_prime"]["list"],
                 final_report_setup["data"]["z_prime"]["max_min"])

    wb.save(output_file)

import PySimpleGUI
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl import load_workbook
import pandas as pd
import re

from info import numb2alpha


def ex_cell(row, col):
    """
    takes row value and column value and translate it to a cell value  ex from (1,1) = (A1)
    :param row: value for the row
    :param col: value for the column
    :return: cell value
    """
    return f"{numb2alpha[col]}{row}"


def org(all_data, well):
    """
    original data
    :param all_data: all the data
    :param well: witch well is being calculated
    :return: the original data in the same formate as the rest of the data will be in
    """
    return all_data["plates"]["original"]["wells"][well]


def norm(all_data, well):
    """
    normalises the data based on the avg of the minimum
    :param all_data: all the data
    :param well: witch well is being calculated
    :return: the results of the normalise calculation
    """
    return all_data["plates"]["original"]["wells"][well] - all_data["calculations"]["original"]["minimum"]["avg"]


def pora(all_data, well):
    """
    percentage of remaining activity calculation based on the avg of the max of normalised data
    :param all_data: all the data
    :param well: witch well is being calculated
    :return: the result of the PORA (percentage of remaining activity)
    """
    print(well)
    print(all_data["calculations"]["normalised"]["max"]["avg"])
    return ((100 * all_data["plates"]["normalised"]["wells"][well]) /
                all_data["calculations"]["normalised"]["max"]["avg"])


def z_prime(all_data, method):
    return 1 - ((3 * (all_data["calculations"][method]["max"]["stdev"] +
                (all_data["calculations"][method]["minimum"]["stdev"]))) /
                abs(all_data["calculations"][method]["max"]["avg"] +
                (all_data["calculations"][method]["minimum"]["avg"])))


def heatmap(config, ws, pw_dict, translate_wells_to_cells, heatmap_colours):
    """
    colour code samples based on values.
    :param ws: worksheet
    :param pw_dict: dict for each well and what state it is (sample, blank, empty....
    :param translate_wells_to_cells: dict for each well cells value
    :return: None
    """
    temp_list = []
    for well in pw_dict:
        if pw_dict[well] == "sample":
            temp_list.append(well)

    # 3 colours heat mao
    ws.conditional_formatting.add(f"{translate_wells_to_cells[temp_list[0]]}:"
                                  f"{translate_wells_to_cells[temp_list[-1]]}",
                                  ColorScaleRule(start_type='percentile', start_value=10,
                                                 start_color=config["colours to hex"][heatmap_colours["start"]],
                                                 mid_type='percentile', mid_value=50,
                                                 mid_color=config["colours to hex"][heatmap_colours["mid"]],
                                                 end_type='percentile',  end_value=90,
                                                 end_color=config["colours to hex"][heatmap_colours["end"]])
                                  )
    # 2 colours heat mao
    # ws.conditional_formatting.add(f"{translate_wells_to_cells[temp_list[0]]}:"
    #                               f"{translate_wells_to_cells[temp_list[-1]]}",
    #                               ColorScaleRule(start_type="min",
    #                                              start_color=config["colours to hex"][heatmap_colours["start"]],
    #                                              end_type="max",
    #                                              end_color=config["colours to hex"][heatmap_colours["end"]]))


def well_row_col_type(plate_layout):
    well_type = {}
    well_col_row = {"well_col": [], "well_row": []}
    print(plate_layout)
    for counter in plate_layout["well_layout"]:
        for keys in plate_layout["well_layout"][counter]:
            if keys == "well_id":
                temp_well_row = re.sub(r"\d+", "", plate_layout["well_layout"][counter][keys])
                temp_well_col = re.sub(r"\D+", "", plate_layout["well_layout"][counter][keys])
                if temp_well_row not in well_col_row["well_row"]:
                    well_col_row["well_row"].append(temp_well_row)
                if temp_well_col not in well_col_row["well_col"]:
                    well_col_row["well_col"].append(temp_well_col)

            if keys == "state":
                well_type.setdefault(plate_layout["well_layout"][counter]["state"], []).append(
                    plate_layout["well_layout"][counter]["well_id"])

    return well_col_row, well_type


def original_data_dict(file, plate_layout):
    well_col_row, well_type = well_row_col_type(plate_layout)
    wb = load_workbook(file)
    sheet = wb.sheetnames[0]
    ws = wb[sheet]
    plate_type_384 = False
    plate_type_1536 = False

    all_data = {"plates": {}, "calculations": {}}
    n_rows = len(well_col_row["well_row"])
    for row_index, row in enumerate(ws.values):
        for index_row, value in enumerate(row):
            if value == "<>":
                skipped_rows = row_index
            if value == "I":
                plate_type_384 = True
            if value == "AA":
                plate_type_1536 = True

    df_plate = pd.read_excel(file, sheet_name=sheet, skiprows=skipped_rows, nrows=n_rows)

    df_plate_dict = df_plate.to_dict()
    if n_rows == 8 and plate_type_384:
        PySimpleGUI.PopupError("Wrong plate size, data is larger than 96-wells")
        return None, None, None
    elif n_rows == 16 and not plate_type_384:
        PySimpleGUI.PopupError("Wrong plate size, data is 96-wells")
        return None, None, None
    elif n_rows == 16 and plate_type_1536:
        PySimpleGUI.PopupError("wrong plate size, data is 1536-wells")
        return None, None, None
    elif n_rows == 32 and not plate_type_1536:
        PySimpleGUI.PopupError("wrong plate size, data is larger smaller than 1536-wells")
        return None, None, None

    temp_reading_dict = {}
    for counter, heading in enumerate(df_plate_dict):
        for index, values in enumerate(df_plate_dict[heading]):
            temp_reading_dict[f"{well_col_row['well_row'][index]}{counter}"] = df_plate_dict[heading][values]

    all_data["plates"]["original"] = {}
    all_data["plates"]["original"]["wells"] = {}
    for state in well_type:
        for well in well_type[state]:
            try:
                all_data["plates"]["original"]["wells"][well] = temp_reading_dict[well]

            # Incase blanked wells are skipped for the reading
            except KeyError:
                all_data["plates"]["original"]["wells"][well] = 1

    return all_data, well_col_row, well_type

if __name__ == "__main__":
    ...
    # 6plate_layout = {"well_layout": {"1": {"well_id": "A1", "state": "empty", "colour": "blue"}, "2": {"well_id": "B1", "state": "empty", "colour": "blue"}, "3": {"well_id": "C1", "state": "empty", "colour": "blue"}, "4": {"well_id": "D1", "state": "empty", "colour": "blue"}, "5": {"well_id": "E1", "state": "empty", "colour": "blue"}, "6": {"well_id": "F1", "state": "empty", "colour": "blue"}, "7": {"well_id": "G1", "state": "empty", "colour": "blue"}, "8": {"well_id": "H1", "state": "empty", "colour": "blue"}, "9": {"well_id": "I1", "state": "empty", "colour": "blue"}, "10": {"well_id": "J1", "state": "empty", "colour": "blue"}, "11": {"well_id": "K1", "state": "empty", "colour": "blue"}, "12": {"well_id": "L1", "state": "empty", "colour": "blue"}, "13": {"well_id": "M1", "state": "empty", "colour": "blue"}, "14": {"well_id": "N1", "state": "empty", "colour": "blue"}, "15": {"well_id": "O1", "state": "empty", "colour": "blue"}, "16": {"well_id": "P1", "state": "empty", "colour": "blue"}, "17": {"well_id": "A2", "state": "empty", "colour": "blue"}, "18": {"well_id": "B2", "state": "max", "colour": "purple"}, "19": {"well_id": "C2", "state": "max", "colour": "purple"}, "20": {"well_id": "D2", "state": "max", "colour": "purple"}, "21": {"well_id": "E2", "state": "max", "colour": "purple"}, "22": {"well_id": "F2", "state": "max", "colour": "purple"}, "23": {"well_id": "G2", "state": "max", "colour": "purple"}, "24": {"well_id": "H2", "state": "max", "colour": "purple"}, "25": {"well_id": "I2", "state": "max", "colour": "purple"}, "26": {"well_id": "J2", "state": "max", "colour": "purple"}, "27": {"well_id": "K2", "state": "max", "colour": "purple"}, "28": {"well_id": "L2", "state": "max", "colour": "purple"}, "29": {"well_id": "M2", "state": "max", "colour": "purple"}, "30": {"well_id": "N2", "state": "max", "colour": "purple"}, "31": {"well_id": "O2", "state": "empty", "colour": "blue"}, "32": {"well_id": "P2", "state": "empty", "colour": "blue"}, "33": {"well_id": "A3", "state": "empty", "colour": "blue"}, "34": {"well_id": "B3", "state": "sample", "colour": "orange"}, "35": {"well_id": "C3", "state": "sample", "colour": "orange"}, "36": {"well_id": "D3", "state": "sample", "colour": "orange"}, "37": {"well_id": "E3", "state": "sample", "colour": "orange"}, "38": {"well_id": "F3", "state": "sample", "colour": "orange"}, "39": {"well_id": "G3", "state": "sample", "colour": "orange"}, "40": {"well_id": "H3", "state": "sample", "colour": "orange"}, "41": {"well_id": "I3", "state": "sample", "colour": "orange"}, "42": {"well_id": "J3", "state": "sample", "colour": "orange"}, "43": {"well_id": "K3", "state": "sample", "colour": "orange"}, "44": {"well_id": "L3", "state": "sample", "colour": "orange"}, "45": {"well_id": "M3", "state": "sample", "colour": "orange"}, "46": {"well_id": "N3", "state": "sample", "colour": "orange"}, "47": {"well_id": "O3", "state": "empty", "colour": "blue"}, "48": {"well_id": "P3", "state": "empty", "colour": "blue"}, "49": {"well_id": "A4", "state": "empty", "colour": "blue"}, "50": {"well_id": "B4", "state": "sample", "colour": "orange"}, "51": {"well_id": "C4", "state": "sample", "colour": "orange"}, "52": {"well_id": "D4", "state": "sample", "colour": "orange"}, "53": {"well_id": "E4", "state": "sample", "colour": "orange"}, "54": {"well_id": "F4", "state": "sample", "colour": "orange"}, "55": {"well_id": "G4", "state": "sample", "colour": "orange"}, "56": {"well_id": "H4", "state": "sample", "colour": "orange"}, "57": {"well_id": "I4", "state": "sample", "colour": "orange"}, "58": {"well_id": "J4", "state": "sample", "colour": "orange"}, "59": {"well_id": "K4", "state": "sample", "colour": "orange"}, "60": {"well_id": "L4", "state": "sample", "colour": "orange"}, "61": {"well_id": "M4", "state": "sample", "colour": "orange"}, "62": {"well_id": "N4", "state": "sample", "colour": "orange"}, "63": {"well_id": "O4", "state": "empty", "colour": "blue"}, "64": {"well_id": "P4", "state": "empty", "colour": "blue"}, "65": {"well_id": "A5", "state": "empty", "colour": "blue"}, "66": {"well_id": "B5", "state": "sample", "colour": "orange"}, "67": {"well_id": "C5", "state": "sample", "colour": "orange"}, "68": {"well_id": "D5", "state": "sample", "colour": "orange"}, "69": {"well_id": "E5", "state": "sample", "colour": "orange"}, "70": {"well_id": "F5", "state": "sample", "colour": "orange"}, "71": {"well_id": "G5", "state": "sample", "colour": "orange"}, "72": {"well_id": "H5", "state": "sample", "colour": "orange"}, "73": {"well_id": "I5", "state": "sample", "colour": "orange"}, "74": {"well_id": "J5", "state": "sample", "colour": "orange"}, "75": {"well_id": "K5", "state": "sample", "colour": "orange"}, "76": {"well_id": "L5", "state": "sample", "colour": "orange"}, "77": {"well_id": "M5", "state": "sample", "colour": "orange"}, "78": {"well_id": "N5", "state": "sample", "colour": "orange"}, "79": {"well_id": "O5", "state": "empty", "colour": "blue"}, "80": {"well_id": "P5", "state": "empty", "colour": "blue"}, "81": {"well_id": "A6", "state": "empty", "colour": "blue"}, "82": {"well_id": "B6", "state": "sample", "colour": "orange"}, "83": {"well_id": "C6", "state": "sample", "colour": "orange"}, "84": {"well_id": "D6", "state": "sample", "colour": "orange"}, "85": {"well_id": "E6", "state": "sample", "colour": "orange"}, "86": {"well_id": "F6", "state": "sample", "colour": "orange"}, "87": {"well_id": "G6", "state": "sample", "colour": "orange"}, "88": {"well_id": "H6", "state": "sample", "colour": "orange"}, "89": {"well_id": "I6", "state": "sample", "colour": "orange"}, "90": {"well_id": "J6", "state": "sample", "colour": "orange"}, "91": {"well_id": "K6", "state": "sample", "colour": "orange"}, "92": {"well_id": "L6", "state": "sample", "colour": "orange"}, "93": {"well_id": "M6", "state": "sample", "colour": "orange"}, "94": {"well_id": "N6", "state": "sample", "colour": "orange"}, "95": {"well_id": "O6", "state": "empty", "colour": "blue"}, "96": {"well_id": "P6", "state": "empty", "colour": "blue"}, "97": {"well_id": "A7", "state": "empty", "colour": "blue"}, "98": {"well_id": "B7", "state": "sample", "colour": "orange"}, "99": {"well_id": "C7", "state": "sample", "colour": "orange"}, "100": {"well_id": "D7", "state": "sample", "colour": "orange"}, "101": {"well_id": "E7", "state": "sample", "colour": "orange"}, "102": {"well_id": "F7", "state": "sample", "colour": "orange"}, "103": {"well_id": "G7", "state": "sample", "colour": "orange"}, "104": {"well_id": "H7", "state": "sample", "colour": "orange"}, "105": {"well_id": "I7", "state": "sample", "colour": "orange"}, "106": {"well_id": "J7", "state": "sample", "colour": "orange"}, "107": {"well_id": "K7", "state": "sample", "colour": "orange"}, "108": {"well_id": "L7", "state": "sample", "colour": "orange"}, "109": {"well_id": "M7", "state": "sample", "colour": "orange"}, "110": {"well_id": "N7", "state": "sample", "colour": "orange"}, "111": {"well_id": "O7", "state": "empty", "colour": "blue"}, "112": {"well_id": "P7", "state": "empty", "colour": "blue"}, "113": {"well_id": "A8", "state": "empty", "colour": "blue"}, "114": {"well_id": "B8", "state": "sample", "colour": "orange"}, "115": {"well_id": "C8", "state": "sample", "colour": "orange"}, "116": {"well_id": "D8", "state": "sample", "colour": "orange"}, "117": {"well_id": "E8", "state": "sample", "colour": "orange"}, "118": {"well_id": "F8", "state": "sample", "colour": "orange"}, "119": {"well_id": "G8", "state": "sample", "colour": "orange"}, "120": {"well_id": "H8", "state": "sample", "colour": "orange"}, "121": {"well_id": "I8", "state": "sample", "colour": "orange"}, "122": {"well_id": "J8", "state": "sample", "colour": "orange"}, "123": {"well_id": "K8", "state": "sample", "colour": "orange"}, "124": {"well_id": "L8", "state": "sample", "colour": "orange"}, "125": {"well_id": "M8", "state": "sample", "colour": "orange"}, "126": {"well_id": "N8", "state": "sample", "colour": "orange"}, "127": {"well_id": "O8", "state": "empty", "colour": "blue"}, "128": {"well_id": "P8", "state": "empty", "colour": "blue"}, "129": {"well_id": "A9", "state": "empty", "colour": "blue"}, "130": {"well_id": "B9", "state": "sample", "colour": "orange"}, "131": {"well_id": "C9", "state": "sample", "colour": "orange"}, "132": {"well_id": "D9", "state": "sample", "colour": "orange"}, "133": {"well_id": "E9", "state": "sample", "colour": "orange"}, "134": {"well_id": "F9", "state": "sample", "colour": "orange"}, "135": {"well_id": "G9", "state": "sample", "colour": "orange"}, "136": {"well_id": "H9", "state": "sample", "colour": "orange"}, "137": {"well_id": "I9", "state": "sample", "colour": "orange"}, "138": {"well_id": "J9", "state": "sample", "colour": "orange"}, "139": {"well_id": "K9", "state": "sample", "colour": "orange"}, "140": {"well_id": "L9", "state": "sample", "colour": "orange"}, "141": {"well_id": "M9", "state": "sample", "colour": "orange"}, "142": {"well_id": "N9", "state": "sample", "colour": "orange"}, "143": {"well_id": "O9", "state": "empty", "colour": "blue"}, "144": {"well_id": "P9", "state": "empty", "colour": "blue"}, "145": {"well_id": "A10", "state": "empty", "colour": "blue"}, "146": {"well_id": "B10", "state": "sample", "colour": "orange"}, "147": {"well_id": "C10", "state": "sample", "colour": "orange"}, "148": {"well_id": "D10", "state": "sample", "colour": "orange"}, "149": {"well_id": "E10", "state": "sample", "colour": "orange"}, "150": {"well_id": "F10", "state": "sample", "colour": "orange"}, "151": {"well_id": "G10", "state": "sample", "colour": "orange"}, "152": {"well_id": "H10", "state": "sample", "colour": "orange"}, "153": {"well_id": "I10", "state": "sample", "colour": "orange"}, "154": {"well_id": "J10", "state": "sample", "colour": "orange"}, "155": {"well_id": "K10", "state": "sample", "colour": "orange"}, "156": {"well_id": "L10", "state": "sample", "colour": "orange"}, "157": {"well_id": "M10", "state": "sample", "colour": "orange"}, "158": {"well_id": "N10", "state": "sample", "colour": "orange"}, "159": {"well_id": "O10", "state": "empty", "colour": "blue"}, "160": {"well_id": "P10", "state": "empty", "colour": "blue"}, "161": {"well_id": "A11", "state": "empty", "colour": "blue"}, "162": {"well_id": "B11", "state": "sample", "colour": "orange"}, "163": {"well_id": "C11", "state": "sample", "colour": "orange"}, "164": {"well_id": "D11", "state": "sample", "colour": "orange"}, "165": {"well_id": "E11", "state": "sample", "colour": "orange"}, "166": {"well_id": "F11", "state": "sample", "colour": "orange"}, "167": {"well_id": "G11", "state": "sample", "colour": "orange"}, "168": {"well_id": "H11", "state": "sample", "colour": "orange"}, "169": {"well_id": "I11", "state": "sample", "colour": "orange"}, "170": {"well_id": "J11", "state": "sample", "colour": "orange"}, "171": {"well_id": "K11", "state": "sample", "colour": "orange"}, "172": {"well_id": "L11", "state": "sample", "colour": "orange"}, "173": {"well_id": "M11", "state": "sample", "colour": "orange"}, "174": {"well_id": "N11", "state": "sample", "colour": "orange"}, "175": {"well_id": "O11", "state": "empty", "colour": "blue"}, "176": {"well_id": "P11", "state": "empty", "colour": "blue"}, "177": {"well_id": "A12", "state": "empty", "colour": "blue"}, "178": {"well_id": "B12", "state": "sample", "colour": "orange"}, "179": {"well_id": "C12", "state": "sample", "colour": "orange"}, "180": {"well_id": "D12", "state": "sample", "colour": "orange"}, "181": {"well_id": "E12", "state": "sample", "colour": "orange"}, "182": {"well_id": "F12", "state": "sample", "colour": "orange"}, "183": {"well_id": "G12", "state": "sample", "colour": "orange"}, "184": {"well_id": "H12", "state": "sample", "colour": "orange"}, "185": {"well_id": "I12", "state": "sample", "colour": "orange"}, "186": {"well_id": "J12", "state": "sample", "colour": "orange"}, "187": {"well_id": "K12", "state": "sample", "colour": "orange"}, "188": {"well_id": "L12", "state": "sample", "colour": "orange"}, "189": {"well_id": "M12", "state": "sample", "colour": "orange"}, "190": {"well_id": "N12", "state": "sample", "colour": "orange"}, "191": {"well_id": "O12", "state": "empty", "colour": "blue"}, "192": {"well_id": "P12", "state": "empty", "colour": "blue"}, "193": {"well_id": "A13", "state": "empty", "colour": "blue"}, "194": {"well_id": "B13", "state": "sample", "colour": "orange"}, "195": {"well_id": "C13", "state": "sample", "colour": "orange"}, "196": {"well_id": "D13", "state": "sample", "colour": "orange"}, "197": {"well_id": "E13", "state": "sample", "colour": "orange"}, "198": {"well_id": "F13", "state": "sample", "colour": "orange"}, "199": {"well_id": "G13", "state": "sample", "colour": "orange"}, "200": {"well_id": "H13", "state": "sample", "colour": "orange"}, "201": {"well_id": "I13", "state": "sample", "colour": "orange"}, "202": {"well_id": "J13", "state": "sample", "colour": "orange"}, "203": {"well_id": "K13", "state": "sample", "colour": "orange"}, "204": {"well_id": "L13", "state": "sample", "colour": "orange"}, "205": {"well_id": "M13", "state": "sample", "colour": "orange"}, "206": {"well_id": "N13", "state": "sample", "colour": "orange"}, "207": {"well_id": "O13", "state": "empty", "colour": "blue"}, "208": {"well_id": "P13", "state": "empty", "colour": "blue"}, "209": {"well_id": "A14", "state": "empty", "colour": "blue"}, "210": {"well_id": "B14", "state": "sample", "colour": "orange"}, "211": {"well_id": "C14", "state": "sample", "colour": "orange"}, "212": {"well_id": "D14", "state": "sample", "colour": "orange"}, "213": {"well_id": "E14", "state": "sample", "colour": "orange"}, "214": {"well_id": "F14", "state": "sample", "colour": "orange"}, "215": {"well_id": "G14", "state": "sample", "colour": "orange"}, "216": {"well_id": "H14", "state": "sample", "colour": "orange"}, "217": {"well_id": "I14", "state": "sample", "colour": "orange"}, "218": {"well_id": "J14", "state": "sample", "colour": "orange"}, "219": {"well_id": "K14", "state": "sample", "colour": "orange"}, "220": {"well_id": "L14", "state": "sample", "colour": "orange"}, "221": {"well_id": "M14", "state": "sample", "colour": "orange"}, "222": {"well_id": "N14", "state": "sample", "colour": "orange"}, "223": {"well_id": "O14", "state": "empty", "colour": "blue"}, "224": {"well_id": "P14", "state": "empty", "colour": "blue"}, "225": {"well_id": "A15", "state": "empty", "colour": "blue"}, "226": {"well_id": "B15", "state": "sample", "colour": "orange"}, "227": {"well_id": "C15", "state": "sample", "colour": "orange"}, "228": {"well_id": "D15", "state": "sample", "colour": "orange"}, "229": {"well_id": "E15", "state": "sample", "colour": "orange"}, "230": {"well_id": "F15", "state": "sample", "colour": "orange"}, "231": {"well_id": "G15", "state": "sample", "colour": "orange"}, "232": {"well_id": "H15", "state": "sample", "colour": "orange"}, "233": {"well_id": "I15", "state": "sample", "colour": "orange"}, "234": {"well_id": "J15", "state": "sample", "colour": "orange"}, "235": {"well_id": "K15", "state": "sample", "colour": "orange"}, "236": {"well_id": "L15", "state": "sample", "colour": "orange"}, "237": {"well_id": "M15", "state": "sample", "colour": "orange"}, "238": {"well_id": "N15", "state": "sample", "colour": "orange"}, "239": {"well_id": "O15", "state": "empty", "colour": "blue"}, "240": {"well_id": "P15", "state": "empty", "colour": "blue"}, "241": {"well_id": "A16", "state": "empty", "colour": "blue"}, "242": {"well_id": "B16", "state": "sample", "colour": "orange"}, "243": {"well_id": "C16", "state": "sample", "colour": "orange"}, "244": {"well_id": "D16", "state": "sample", "colour": "orange"}, "245": {"well_id": "E16", "state": "sample", "colour": "orange"}, "246": {"well_id": "F16", "state": "sample", "colour": "orange"}, "247": {"well_id": "G16", "state": "sample", "colour": "orange"}, "248": {"well_id": "H16", "state": "sample", "colour": "orange"}, "249": {"well_id": "I16", "state": "sample", "colour": "orange"}, "250": {"well_id": "J16", "state": "sample", "colour": "orange"}, "251": {"well_id": "K16", "state": "sample", "colour": "orange"}, "252": {"well_id": "L16", "state": "sample", "colour": "orange"}, "253": {"well_id": "M16", "state": "sample", "colour": "orange"}, "254": {"well_id": "N16", "state": "sample", "colour": "orange"}, "255": {"well_id": "O16", "state": "empty", "colour": "blue"}, "256": {"well_id": "P16", "state": "empty", "colour": "blue"}, "257": {"well_id": "A17", "state": "empty", "colour": "blue"}, "258": {"well_id": "B17", "state": "sample", "colour": "orange"}, "259": {"well_id": "C17", "state": "sample", "colour": "orange"}, "260": {"well_id": "D17", "state": "sample", "colour": "orange"}, "261": {"well_id": "E17", "state": "sample", "colour": "orange"}, "262": {"well_id": "F17", "state": "sample", "colour": "orange"}, "263": {"well_id": "G17", "state": "sample", "colour": "orange"}, "264": {"well_id": "H17", "state": "sample", "colour": "orange"}, "265": {"well_id": "I17", "state": "sample", "colour": "orange"}, "266": {"well_id": "J17", "state": "sample", "colour": "orange"}, "267": {"well_id": "K17", "state": "sample", "colour": "orange"}, "268": {"well_id": "L17", "state": "sample", "colour": "orange"}, "269": {"well_id": "M17", "state": "sample", "colour": "orange"}, "270": {"well_id": "N17", "state": "sample", "colour": "orange"}, "271": {"well_id": "O17", "state": "empty", "colour": "blue"}, "272": {"well_id": "P17", "state": "empty", "colour": "blue"}, "273": {"well_id": "A18", "state": "empty", "colour": "blue"}, "274": {"well_id": "B18", "state": "sample", "colour": "orange"}, "275": {"well_id": "C18", "state": "sample", "colour": "orange"}, "276": {"well_id": "D18", "state": "sample", "colour": "orange"}, "277": {"well_id": "E18", "state": "sample", "colour": "orange"}, "278": {"well_id": "F18", "state": "sample", "colour": "orange"}, "279": {"well_id": "G18", "state": "sample", "colour": "orange"}, "280": {"well_id": "H18", "state": "sample", "colour": "orange"}, "281": {"well_id": "I18", "state": "sample", "colour": "orange"}, "282": {"well_id": "J18", "state": "sample", "colour": "orange"}, "283": {"well_id": "K18", "state": "sample", "colour": "orange"}, "284": {"well_id": "L18", "state": "sample", "colour": "orange"}, "285": {"well_id": "M18", "state": "sample", "colour": "orange"}, "286": {"well_id": "N18", "state": "sample", "colour": "orange"}, "287": {"well_id": "O18", "state": "empty", "colour": "blue"}, "288": {"well_id": "P18", "state": "empty", "colour": "blue"}, "289": {"well_id": "A19", "state": "empty", "colour": "blue"}, "290": {"well_id": "B19", "state": "sample", "colour": "orange"}, "291": {"well_id": "C19", "state": "sample", "colour": "orange"}, "292": {"well_id": "D19", "state": "sample", "colour": "orange"}, "293": {"well_id": "E19", "state": "sample", "colour": "orange"}, "294": {"well_id": "F19", "state": "sample", "colour": "orange"}, "295": {"well_id": "G19", "state": "sample", "colour": "orange"}, "296": {"well_id": "H19", "state": "sample", "colour": "orange"}, "297": {"well_id": "I19", "state": "sample", "colour": "orange"}, "298": {"well_id": "J19", "state": "sample", "colour": "orange"}, "299": {"well_id": "K19", "state": "sample", "colour": "orange"}, "300": {"well_id": "L19", "state": "sample", "colour": "orange"}, "301": {"well_id": "M19", "state": "sample", "colour": "orange"}, "302": {"well_id": "N19", "state": "sample", "colour": "orange"}, "303": {"well_id": "O19", "state": "empty", "colour": "blue"}, "304": {"well_id": "P19", "state": "empty", "colour": "blue"}, "305": {"well_id": "A20", "state": "empty", "colour": "blue"}, "306": {"well_id": "B20", "state": "sample", "colour": "orange"}, "307": {"well_id": "C20", "state": "sample", "colour": "orange"}, "308": {"well_id": "D20", "state": "sample", "colour": "orange"}, "309": {"well_id": "E20", "state": "sample", "colour": "orange"}, "310": {"well_id": "F20", "state": "sample", "colour": "orange"}, "311": {"well_id": "G20", "state": "sample", "colour": "orange"}, "312": {"well_id": "H20", "state": "sample", "colour": "orange"}, "313": {"well_id": "I20", "state": "sample", "colour": "orange"}, "314": {"well_id": "J20", "state": "sample", "colour": "orange"}, "315": {"well_id": "K20", "state": "sample", "colour": "orange"}, "316": {"well_id": "L20", "state": "sample", "colour": "orange"}, "317": {"well_id": "M20", "state": "sample", "colour": "orange"}, "318": {"well_id": "N20", "state": "sample", "colour": "orange"}, "319": {"well_id": "O20", "state": "empty", "colour": "blue"}, "320": {"well_id": "P20", "state": "empty", "colour": "blue"}, "321": {"well_id": "A21", "state": "empty", "colour": "blue"}, "322": {"well_id": "B21", "state": "sample", "colour": "orange"}, "323": {"well_id": "C21", "state": "sample", "colour": "orange"}, "324": {"well_id": "D21", "state": "sample", "colour": "orange"}, "325": {"well_id": "E21", "state": "sample", "colour": "orange"}, "326": {"well_id": "F21", "state": "sample", "colour": "orange"}, "327": {"well_id": "G21", "state": "sample", "colour": "orange"}, "328": {"well_id": "H21", "state": "sample", "colour": "orange"}, "329": {"well_id": "I21", "state": "sample", "colour": "orange"}, "330": {"well_id": "J21", "state": "sample", "colour": "orange"}, "331": {"well_id": "K21", "state": "sample", "colour": "orange"}, "332": {"well_id": "L21", "state": "sample", "colour": "orange"}, "333": {"well_id": "M21", "state": "sample", "colour": "orange"}, "334": {"well_id": "N21", "state": "sample", "colour": "orange"}, "335": {"well_id": "O21", "state": "empty", "colour": "blue"}, "336": {"well_id": "P21", "state": "empty", "colour": "blue"}, "337": {"well_id": "A22", "state": "empty", "colour": "blue"}, "338": {"well_id": "B22", "state": "sample", "colour": "orange"}, "339": {"well_id": "C22", "state": "sample", "colour": "orange"}, "340": {"well_id": "D22", "state": "sample", "colour": "orange"}, "341": {"well_id": "E22", "state": "sample", "colour": "orange"}, "342": {"well_id": "F22", "state": "sample", "colour": "orange"}, "343": {"well_id": "G22", "state": "sample", "colour": "orange"}, "344": {"well_id": "H22", "state": "sample", "colour": "orange"}, "345": {"well_id": "I22", "state": "sample", "colour": "orange"}, "346": {"well_id": "J22", "state": "sample", "colour": "orange"}, "347": {"well_id": "K22", "state": "sample", "colour": "orange"}, "348": {"well_id": "L22", "state": "sample", "colour": "orange"}, "349": {"well_id": "M22", "state": "sample", "colour": "orange"}, "350": {"well_id": "N22", "state": "sample", "colour": "orange"}, "351": {"well_id": "O22", "state": "empty", "colour": "blue"}, "352": {"well_id": "P22", "state": "empty", "colour": "blue"}, "353": {"well_id": "A23", "state": "empty", "colour": "blue"}, "354": {"well_id": "B23", "state": "minimum", "colour": "yellow"}, "355": {"well_id": "C23", "state": "minimum", "colour": "yellow"}, "356": {"well_id": "D23", "state": "minimum", "colour": "yellow"}, "357": {"well_id": "E23", "state": "minimum", "colour": "yellow"}, "358": {"well_id": "F23", "state": "minimum", "colour": "yellow"}, "359": {"well_id": "G23", "state": "minimum", "colour": "yellow"}, "360": {"well_id": "H23", "state": "minimum", "colour": "yellow"}, "361": {"well_id": "I23", "state": "minimum", "colour": "yellow"}, "362": {"well_id": "J23", "state": "minimum", "colour": "yellow"}, "363": {"well_id": "K23", "state": "minimum", "colour": "yellow"}, "364": {"well_id": "L23", "state": "minimum", "colour": "yellow"}, "365": {"well_id": "M23", "state": "minimum", "colour": "yellow"}, "366": {"well_id": "N23", "state": "minimum", "colour": "yellow"}, "367": {"well_id": "O23", "state": "empty", "colour": "blue"}, "368": {"well_id": "P23", "state": "empty", "colour": "blue"}, "369": {"well_id": "A24", "state": "empty", "colour": "blue"}, "370": {"well_id": "B24", "state": "empty", "colour": "blue"}, "371": {"well_id": "C24", "state": "empty", "colour": "blue"}, "372": {"well_id": "D24", "state": "empty", "colour": "blue"}, "373": {"well_id": "E24", "state": "empty", "colour": "blue"}, "374": {"well_id": "F24", "state": "empty", "colour": "blue"}, "375": {"well_id": "G24", "state": "empty", "colour": "blue"}, "376": {"well_id": "H24", "state": "empty", "colour": "blue"}, "377": {"well_id": "I24", "state": "empty", "colour": "blue"}, "378": {"well_id": "J24", "state": "empty", "colour": "blue"}, "379": {"well_id": "K24", "state": "empty", "colour": "blue"}, "380": {"well_id": "L24", "state": "empty", "colour": "blue"}, "381": {"well_id": "M24", "state": "empty", "colour": "blue"}, "382": {"well_id": "N24", "state": "empty", "colour": "blue"}, "383": {"well_id": "O24", "state": "empty", "colour": "blue"}, "384": {"well_id": "P24", "state": "empty", "colour": "blue"}}, "plate_type": "plate_384"}, "New_layout":
    # folder =" C:/Users/Charlie/PycharmProjects/structure_search/Bio Data/raw data"
    # file = "Data_analysis-MTase1-Epigenetic_library_HYCPK5449.xlsx"
    # full_file = f"{folder}/{file}"
    # original_data_dict(full_file, plate_layout)
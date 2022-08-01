"""
Layout of different plates with well placement and names.
"""

plate_96 = [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12",
           ]


mother_plate_layout = {"T1": [["A1"], ["A3"], ["A5"], ["A7"], ["A9"], ["A11"], ["A13"], ["A15"], ["A17"], ["A19"],
                              ["A21"], ["A23"], ["C1"], ["C3"], ["C5"], ["C7"], ["C9"], ["C11"], ["C13"], ["C15"],
                              ["C17"], ["C19"], ["C21"], ["C23"], ["E1"], ["E3"], ["E5"], ["E7"], ["E9"], ["E11"],
                              ["E13"], ["E15"], ["E17"], ["E19"], ["E21"], ["E23"], ["G1"], ["G3"], ["G5"], ["G7"],
                              ["G9"], ["G11"], ["G13"], ["G15"], ["G17"], ["G19"], ["G21"], ["G23"], ["I1"], ["I3"],
                              ["I5"], ["I7"], ["I9"], ["I11"], ["I13"], ["I15"], ["I17"], ["I19"], ["I21"], ["I23"],
                              ["K1"], ["K3"], ["K5"], ["K7"], ["K9"], ["K11"], ["K13"], ["K15"], ["K17"], ["K19"],
                              ["K21"], ["K23"], ["M1"], ["M3"], ["M5"], ["M7"], ["M9"], ["M11"], ["M13"], ["M15"],
                              ["M17"], ["M19"], ["M21"], ["M23"], ["O1"], ["O3"], ["O5"], ["O7"], ["O9"], ["O11"],
                              ["O13"], ["O15"], ["O17"], ["O19"], ["O21"], ["O23"]],
                       "T2": [["A2"], ["A4"], ["A6"], ["A8"], ["A10"], ["A12"], ["A14"], ["A16"], ["A18"], ["A20"],
                              ["A22"], ["A24"], ["C2"], ["C4"], ["C6"], ["C8"], ["C10"], ["C12"], ["C14"], ["C16"],
                              ["C18"], ["C20"], ["C22"], ["C24"], ["E2"], ["E4"], ["E6"], ["E8"], ["E10"], ["E12"],
                              ["E14"], ["E16"], ["E18"], ["E20"], ["E22"], ["E24"], ["G2"], ["G4"], ["G6"], ["G8"],
                              ["G10"], ["G12"], ["G14"], ["G16"], ["G18"], ["G20"], ["G22"], ["G24"], ["I2"], ["I4"],
                              ["I6"], ["I8"], ["I10"], ["I12"], ["I14"], ["I16"], ["I18"], ["I20"], ["I22"], ["I24"],
                              ["K2"], ["K4"], ["K6"], ["K8"], ["K10"], ["K12"], ["K14"], ["K16"], ["K18"], ["K20"],
                              ["K22"], ["K24"], ["M2"], ["M4"], ["M6"], ["M8"], ["M10"], ["M12"], ["M14"], ["M16"],
                              ["M18"], ["M20"], ["M22"], ["M24"], ["O2"], ["O4"], ["O6"], ["O8"], ["O10"], ["O12"],
                              ["O14"], ["O16"], ["O18"], ["O20"], ["O22"], ["O24"]],
                       "T3": [["B1"], ["B3"], ["B5"], ["B7"], ["B9"], ["B11"], ["B13"], ["B15"], ["B17"], ["B19"],
                              ["B21"], ["B23"], ["D1"], ["D3"], ["D5"], ["D7"], ["D9"], ["D11"], ["D13"], ["D15"],
                              ["D17"], ["D19"], ["D21"], ["D23"], ["F1"], ["F3"], ["F5"], ["F7"], ["F9"], ["F11"],
                              ["F13"], ["F15"], ["F17"], ["F19"], ["F21"], ["F23"], ["H1"], ["H3"], ["H5"], ["H7"],
                              ["H9"], ["H11"], ["H13"], ["H15"], ["H17"], ["H19"], ["H21"], ["H23"], ["J1"], ["J3"],
                              ["J5"], ["J7"], ["J9"], ["J11"], ["J13"], ["J15"], ["J17"], ["J19"], ["J21"], ["J23"],
                              ["L1"], ["L3"], ["L5"], ["L7"], ["L9"], ["L11"], ["L13"], ["L15"], ["L17"], ["L19"],
                              ["L21"], ["L23"], ["N1"], ["N3"], ["N5"], ["N7"], ["N9"], ["N11"], ["N13"], ["N15"],
                              ["N17"], ["N19"], ["N21"], ["N23"], ["P1"], ["P3"], ["P5"], ["P7"], ["P9"], ["P11"],
                              ["P13"], ["P15"], ["P17"], ["P19"], ["P21"], ["P23"]],
                       "T4": [["B2"], ["B4"], ["B6"], ["B8"], ["B10"], ["B12"], ["B14"], ["B16"], ["B18"], ["B20"],
                              ["B22"], ["B24"], ["D2"], ["D4"], ["D6"], ["D8"], ["D10"], ["D12"], ["D14"], ["D16"],
                              ["D18"], ["D20"], ["D22"], ["D24"], ["F2"], ["F4"], ["F6"], ["F8"], ["F10"], ["F12"],
                              ["F14"], ["F16"], ["F18"], ["F20"], ["F22"], ["F24"], ["H2"], ["H4"], ["H6"], ["H8"],
                              ["H10"], ["H12"], ["H14"], ["H16"], ["H18"], ["H20"], ["H22"], ["H24"], ["J2"], ["J4"],
                              ["J6"], ["J8"], ["J10"], ["J12"], ["J14"], ["J16"], ["J18"], ["J20"], ["J22"], ["J24"],
                              ["L2"], ["L4"], ["L6"], ["L8"], ["L10"], ["L12"], ["L14"], ["L16"], ["L18"], ["L20"],
                              ["L22"], ["L24"], ["N2"], ["N4"], ["N6"], ["N8"], ["N10"], ["N12"], ["N14"], ["N16"],
                              ["N18"], ["N20"], ["N22"], ["N24"], ["P2"], ["P4"], ["P6"], ["P8"], ["P10"], ["P12"],
                              ["P14"], ["P16"], ["P18"], ["P20"], ["P22"], ["P24"]]
                       }

numb2alpha = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z", 27: "AA", 28: "AB", 29: "AC", 30: "AD", 31: "AE", 32: "AF", 33: "AG", 34: "AH", 35: "AI", 36: "AJ", 37: "AK", 38: "AL", 39: "AM", 40: "AN", 41: "AO", 42: "AP", 43: "AQ", 44: "AR", 45: "AS", 46: "AT", 47: "AU", 48: "AV", 49: "AW", 50: "AX", 51: "AY", 52: "AZ"}
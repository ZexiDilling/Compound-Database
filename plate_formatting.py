from info import mother_plate_layout as mpl


def mother_plate_generator(tube_dict, mp_name, volume=9):
    """
    Generates mother_plates from tube_list and mother_plate layout (from 4 x 96 well plate to one 384 well plate).

    :param tube_dict: Dict of all the tubes
    :type tube_dict: dict
    :param mp_name: Name used for MotherPlates
    :type mp_name: str
    :param volume: How much volume is needed for the transferee
    :type volume: float
    :return:
        - mp_plate: A dict of Motherplates
        - pb_mp_output: A dict for PlateButler, for the MotherPlate protocol
    :rtype:
        - dict
        - dict
    """
    transferee = 0
    mp_name_counter = 1
    mp_plate = {}
    pb_mp_output = {}
    for rack_id in tube_dict:
        for index, samples in enumerate(tube_dict[rack_id]):

            if index == 0:
                transferee += 1
                if transferee > 4:
                    transferee = 1
                    if transferee == 1:
                        mp_name_counter += 1

            mp_name_temp = f"{mp_name}_{mp_name_counter}"
            destination_well = mpl[f"{'T'}{transferee}"][index][0]
            mp_plate.setdefault(mp_name_temp, []).append([destination_well, tube_dict[rack_id][samples]])

            pb_mp_output.setdefault(mp_name_temp, []).append([destination_well, tube_dict[rack_id][samples], volume])

    return mp_plate, pb_mp_output


def daughter_plate_generator(mp_data, sample_amount, dp_name, dp_layout, volume):
    """
    Writes source plate information to destination plate. for well's and compound id, and how much to transferee

    :param mp_data: Data for the MotherPlate
    :type mp_data: dict
    :param sample_amount: Amount of samples
    :type sample_amount: int
    :param dp_name: Name for the DaughterPlates
    :type dp_name: str
    :param dp_layout: The Layout of the DaughterPlates
    :type dp_layout: dict
    :param volume: How much volume is needed
    :type volume: float
    :return: A dict with source and destination information.
    :rtype: dict
    """
    dp_dict = {}
    name_counter = 1
    counter = 0

    for plate in mp_data:
        for source_well, source_sample in mp_data[plate]:
            if counter == sample_amount:
                name_counter += 1
                counter = 0

            barcode = f"{dp_name}{name_counter}"
            destination_well = dp_layout["sample"][counter]

            dp_dict.setdefault(barcode, []).append(
                [destination_well, volume, source_well, source_sample, plate])
            counter += 1
    return dp_dict


def plate_layout_re_formate(plate_layout):
    """
    Reformate the platlayout from having a counter, to using the well-ID instead

    :param plate_layout: The layout for the plates, with well_id, colour and state
    :type plate_layout: dict
    :return: Reformate the platlayout from having a counter, to using the well-ID instead
    :rtype: dict
    """
    plate_layout_re = {}

    for counter in plate_layout:
        plate_layout_re[plate_layout[counter]["well_id"]] = {}

        if "group" in plate_layout[counter]:
            plate_layout_re[plate_layout[counter]["well_id"]]["group"] = plate_layout[counter]["group"]
        plate_layout_re[plate_layout[counter]["well_id"]]["state"] = plate_layout[counter]["state"]
        plate_layout_re[plate_layout[counter]["well_id"]]["colour"] = plate_layout[counter]["colour"]

    return plate_layout_re


def plate_layout_to_well_ditc(plate_layout):
    """
    turning the panda-datafrom into a dict.

    :param plate_layout: Plate_layout for the Daughter plate
    :type plate_layout: ditch
    :return: A dict with what is in each well. blank, sample or ref
    :rtype: dict
    """
    well_dict = {"sample": [], "blank": [], "max": [], "minimum": [],
                 "positive": [], "negative": [], "empty": []}
    for counter in plate_layout["well_layout"]:
        well_dict[plate_layout["well_layout"][counter]["state"]].append(plate_layout["well_layout"][counter]["well_id"])

    return well_dict
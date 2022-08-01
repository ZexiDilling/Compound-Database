from info import mother_plate_layout as mpl


def mother_plate_generator(tube_dict, mp_name, volume=9):
    """
    Generates mother_plates from tube_list and mother_plate layout (from 4 x 96 well plate to one 384 well plate).
    :param tube_dict: Dict of all the tubes
    :param mp_name: Name used for MotherPlates
    :param volume: How much volume is needed for the transferee
    :return: 2 dicts
    A dict for MotherPlates
    A Dict for PlateButler, for the MotherPlate protocol
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
    :param sample_amount: Amount of samples
    :param dp_name: Name for the DaughterPlates
    :param dp_layout: The Layout of the DaughterPlates
    :param volume: How much volume is needed
    :return: A dict with source and destination information.
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

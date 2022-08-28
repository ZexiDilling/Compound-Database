import json


def dict_writer(file_name, data_dict):
    """
    Writes plate-formates to a CSV file

    :param file_name: The name of the txt file, where the data is saved
    :type file_name: str
    :param data_dict: A dict with data that needs to be saved
    :type data_dict: dict
    :return: A CSV file with information
    """
    with open(file_name, "w") as f:
        f.write(json.dumps(data_dict))


def dict_reader(file_name):
    try:
        with open(file_name) as f:
            data = f.read()
    except TypeError:
        return {}

    js = json.loads(data)

    return js


def plate_dict_reader(plate_file):
    """
    Gets data from a CSV file and turns it into a dict that can be used to draw a plate-layout

    :param plate_file: The file name
    :type plate_file: str
    :return:
        - plate_list: A list of all the layouts
        - archive_plates: A dict for the well state in each layout
    :rtype:
        - list
        - dict
    """

    try:
        with open(plate_file) as f:
            data = f.read()
    except TypeError:
        return [], {}

    if data:
        js = json.loads(data)
        plate_list = []
        archive_plates = {}
        for plate in js:
            plate_list.append(plate)
            archive_plates[plate] = {}
            for headlines in js[plate]:
                if headlines == "well_layout":
                    archive_plates[plate][headlines] = {}
                    for keys in js[plate][headlines]:
                        temp_key = int(keys)
                        archive_plates[plate][headlines][temp_key] = js[plate][headlines][keys]
                elif headlines == "plate_type":
                    archive_plates[plate][headlines] = js[plate][headlines]

        return plate_list, archive_plates




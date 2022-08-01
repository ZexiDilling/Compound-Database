import json


def dict_writer(plate_file, plate_dictionary):

    with open(plate_file, "w") as f:
        f.write(json.dumps(plate_dictionary))


def dict_reader(plate_file):

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

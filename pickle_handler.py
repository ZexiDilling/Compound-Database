import pickle


def df_writer(file_path, data):

    if guard(file_path, data):
        with open(file_path, "ab") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def guard(file_path, data):
    """
    Checks if the data is already in the file
    Not sure if this is needed... or if the check should be here...
    :param file_path:
    :param data:
    :return:
    """
    for samples in data:
        sample = samples

    if df_reader(file_path, sample):
        return False

    else:
        return True


def df_reader(file_path, samples):
    with open(file_path, "rb") as handle:


        temp_dict = {}
        while 1:
            try:
                # objs.append(pickle.load(handle))
                temp_data = pickle.load(handle)
                for sample in temp_data:

                    if sample in samples:

                        temp_dict[sample] = {}
                        data = temp_data[sample]
                        temp_dict[sample] = data

            except EOFError:
                break
        return temp_dict

if __name__ == "__main__":
    file_path = "output/purity_data_08_2022"

    sample = ["B1P9_009_130722", "B1P1_001_130722"]

    temp_data_ditc = {"row_id": "row_id",
                      "compound_id": "compound_id",
                      "sample": sample,
                      "batch": "batch",
                      "method": "method",
                      "file_name": file_path,
                      "date": "file_name"}

    print(guard(file_path, temp_data_ditc))

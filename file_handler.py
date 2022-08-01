import os
import shutil


def get_file_list(path):
    """
    Generate a list of files in a folder
    :param path: The path to the folder where data is located.
    :return: A list of files in the folder
    """
    return [f"{path}/{files}" for files in os.listdir(path)]


def move_files(file_list):

    for file in file_list:
        if not os.path.isdir(file):
            temp_destination = ""
            file_split = []
            init_split = file.split("/")
            for split in init_split:
                temp_split = split.split("\\")
                for temp in temp_split:
                    file_split.append(temp)
            for index, value in enumerate(file_split):

                if value == "pending":
                    temp_destination += "Transferred"
                else:
                    temp_destination += value
                if index == len(file_split)-2 and "Transferred" in temp_destination:
                    try:
                        os.mkdir(temp_destination)
                    except OSError:
                        pass
                if index < len(file_split)-1:
                    temp_destination += "/"

            shutil.move(file, temp_destination)


def _folder_scan(folder):
    all_files = {}
    for files in os.listdir(folder):
        all_files[files] = [folder]

    main_folder = [f.path for f in os.scandir(folder) if f.is_dir()]

    for folder in main_folder:
        for file in os.listdir(folder):
            all_files[file] = [folder]
        all_files = _sub_folder_digger(folder, all_files)

    path_list = _create_folder_paths(all_files)

    return(path_list)


def _create_folder_paths(all_files):
    path_list = []

    for file in all_files:
        for folder in all_files[file]:
            path_list.append("/".join((folder, file)))

    return path_list


def _sub_folder_digger(sub_folder, all_files):
    temp_file = []
    sub_folder = [f.path for f in os.scandir(sub_folder) if f.is_dir()]
    for folders in sub_folder:
        for file in os.listdir(folders):
            temp_file.append(file)
            all_files[file] = [folders]
        if temp_file:
            _sub_folder_digger(folders, all_files)

    return all_files


def file_list_distributor(folder):
    file_list = _folder_scan(folder)
    compound_list = []
    mp_list = []
    dp_list = []
    purity_list = []
    bio_list = []

    for file in file_list:
        if "Compounds" in file:
            if file.endswith("sdf"):
                compound_list.append(file)
        elif "MotherPlate_production" in file:
            if file.endswith("txt"):
                mp_list.append(file)
        elif "DaughterPlate_production" in file:
            if file.endswith("xml"):
                dp_list.append(file)
        elif "Purity Data" in file:
            purity_list.append(file)

        if "Bio Data" in file:
            bio_list.append(file)

    return compound_list, mp_list, dp_list, purity_list, bio_list, file_list


if __name__ == "__main__":
    folder = "C:/Users/phch/PycharmProjects/structure_search/output_files/pending"
    #folder_scan(folder)
    # file_list = get_file_list(folder)
    z, x, c, a, s, file_list = file_list_distributor(folder)
    move_files(file_list)

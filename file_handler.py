import os
import shutil


def get_file_list(path):
    """
    Generate a list of files in a folder

    :param path: The path to the folder where data is located.
    :type path: str
    :return: A list of files in the folder
    :rtype: list
    """
    return [f"{path}/{files}" for files in os.listdir(path)]


def move_files(file_list):
    """
    Moves files from one folder to another
    THIS IS NOT WORKING ATM!!!

    :param file_list: The list of files that needs to be moved
    :type file_list: list
    :return: The file moved to a different folder
    """

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
    """
    Scans the folder for files and folders

    :param folder: The main starting folder
    :type folder: str
    :return: a list of all the different folders and sub folders and files in thoes folders
    :rtype: list
    """
    all_files = {}
    for files in os.listdir(folder):
        all_files[files] = [folder]

    main_folder = [f.path for f in os.scandir(folder) if f.is_dir()]

    for folder in main_folder:
        for file in os.listdir(folder):
            all_files[file] = [folder]
        all_files = _sub_folder_digger(folder, all_files)

    path_list = _create_folder_paths(all_files)

    return path_list


def _create_folder_paths(all_files):
    """
    Creates a list of path to the different files in the file list

    :param all_files: A list of all the files and folders
    :type all_files: list
    :return: a list of fill paths to the files
    :rtype: list
    """
    path_list = []

    for file in all_files:
        for folder in all_files[file]:
            path_list.append("/".join((folder, file)))

    return path_list


def _sub_folder_digger(sub_folder, all_files):
    """
    Digs through the sub folder of the main folder, to find more files and folders

    :param sub_folder: The sub folders under the main folder
    :type sub_folder: str
    :param all_files: A list of all the files and folders
    :type all_files: list
    :return: All the files and the sub folders in one list
    :rtype: list
    """
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
    """
    Sends the main folder to different modules to get all the files and folders in the main folder, for different
    file types to send to the right analyst module

    :param folder: The main folder
    :type folder: str
    :return:
        - compound_list: A list of compounds
        - mp_list: A list of MotherPlates
        - dp_list: A list of DP's
        - purity_list: A list of purity data
        - bio_list: A list of Bio data
        - file_list: A list of all the files
    :rtype:
        - list
        - list
        - list
        - list
        - list
        - list
    """
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

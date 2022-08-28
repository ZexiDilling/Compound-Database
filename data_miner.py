import os
import numpy as np
import pandas as pd
import re
import datetime


def _uv_date(file, all_data, row_id):
    """
    grabs UV data based on files ending with ".txt"
    It also uses data in the UV-files for batch name, and sample name for the complete DataFrame.
    Uses the UV-file name for ID-ing what MS-files belongs to witch batch/sample to make sure  that the right data
    are combined in the final DataFrame.

    :param file: raw data file for UV data
    :type file: str
    :param temp_file_name: List of file names of the data, to match it against MS data
    :type temp_file_name: list
    :param sample_id: List of compound id per sample
    :type sample_id: list
    :param batch_id: list of batch_id / plate_id
    :type batch_id: list
    :param batch_dic: a dictionary keys for batch/plate and values a list of samples/compounds
    :type batch_dic: dict
    :param uv_files: A list of the UV data
    :type uv_files: list
    :return:
        - temp_file_name: name of the file for comparing with ms data
        - sample_id: sample/compound id
        - batch_id: batch/plate id
        - batch_dic: a dictionary keys for batch/plate and values a list of samples/compounds
        - uv_files: the UV data
        - sample_date: date and time for the sample
    :rtype:
        - list
        - list
        - dict
        - file
        - str
    """

    with open(file) as f:
        uv_txt = f.read()
    uv_txt = uv_txt.split('\n\n')

    # Loop over strings in UV_file
    K = np.arange(0, len(uv_txt), 1)

    for k in K:

        x = uv_txt[k]
        # Split x (string) at '/n', returns a list of strings
        x = x.split('\n')

        # get date and time
        if x[0] == "[File Information]":
            temp_date = x[2].split()[1].split(" ")[0]
            # Change to date formate
            temp_date = datetime.datetime.strptime(temp_date, "%d/%m/%Y").strftime("%Y-%m-%d")

        # get batch information
        if x[0] == "[Original Files]":
            temp_sample = os.path.basename(x[1]).split(".")[0]
            temp_method = os.path.basename(x[2]).split(".")[0]
            temp_batch = os.path.basename(x[3]).split(".")[0]

        # Find relevant UV data where x[0]=='[PDA 3D]'
        if x[0] == '[PDA 3D]':
            UV_data_index_sample = x
            del UV_data_index_sample[0:10]

    # Extract wavelengths for column labels
    wavelengths = UV_data_index_sample[0]
    wavelengths = wavelengths.split('\t')
    del wavelengths[0]
    wavelengths = np.asarray(wavelengths)
    wavelengths = wavelengths.astype(float)
    UV_wavelengths = wavelengths / 100

    # Extract retention times doe row labels
    UV_data1 = UV_data_index_sample[1:]
    L = np.arange(0, len(UV_data1), 1)
    UV_retention_times = []
    for l in L:
        x = UV_data1[l]
        x = x.split('\t')
        UV_retention_times.append(float(x[0].replace(',', '.')))

    # Extract UV intensities
    UV = []
    for l in L:
        x = UV_data1[l]
        x = x.split('\t')
        x = x[1:]
        x = np.asarray(x)
        x = x.astype(float)
        UV.append(x)
    # Combine UV intensities, wavelengths (columns) and retention times (rows) in one dataframe
    temp_uv_data = pd.DataFrame(UV, columns=UV_wavelengths, index=UV_retention_times)

    # Setting up the data ditch for each sample for later use
    all_data[temp_sample] = {"row_id": "", "compound_id": "", "sample": "", "batch": "", "uv": "", "ms_pos": "",
                             "ms_neg": "", "method": "", "file_name": "", "date": ""}
    all_data[temp_sample]["row_id"] = row_id
    all_data[temp_sample]["sample"] = temp_sample
    all_data[temp_sample]["method"] = temp_method
    all_data[temp_sample]["batch"] = temp_batch
    all_data[temp_sample]["uv"] = temp_uv_data
    all_data[temp_sample]["date"] = temp_date

    return all_data


def _ms_neg(file, all_data):
    """
    Grabs negative MS data from "_Seg1Ev2.JDX"
    compares the name with UV-file name to make sure that it is the right data.

    :param file: raw data file for MS data (Negative mode)
    :type file:str
    :param temp_file_name: list of file names, to compare with UV, to make sure that the same data is added to the
        same sample/compound
    :type temp_file_name: str
    :param ms_neg_files: the MS data
    :type ms_neg_files: list
    :return: temp_ms_neg(infomation for ms_positive to make sure the two type matches), ms_neg_files (MS Data)
    :rtype: str, list
    """

    with open(file) as f:
        jdx_file = f.read()
    # Split MS_file at '##SCAN_NUMBER'
    ms_file = jdx_file.split('##SCAN_NUMBER')
    # Delete first string in MS_file
    del ms_file[0]

    # Generate the m/z-values (ranges from 100 to 1000, with 0.05 intervals)
    # OBS: Change the m/z range here if needed
    mz_range = np.arange(100, 1000.05, 0.05)
    mz_range = mz_range.round(2)
    # Generate array with length of the total number of scans
    array = np.arange(0, len(ms_file), 1)
    # Generate zero matrix
    zero_matrix = np.zeros((len(array), len(mz_range)))
    # Empty retention time array
    ms_retention_times = []
    for m in array:
        x = ms_file[m]
        # Split MS_file at '/n'
        x = x.split('\n')
        # Extract retention times
        rt = re.findall('\d*\.?\d+', x[1].replace(",", "."))  # Extract retion time
        rt = float(np.asarray(rt))
        ms_retention_times.append(rt)
        # Extract MS- data
        del x[0:5]
        del x[-1]
        # Delete '##END' in the end of the file
        if m == array[-1]:
            del x[-1]
        # Replace 0's in zero_matrix with detected m/z-values
        N = np.arange(0, len(x), 1)
        for n in N:
            x[n] = x[n].replace(",", ".", 1)
            x_mz = (float(re.findall('\d*\.?\d+', x[n])[0]))
            ind = np.where(mz_range == x_mz)[0][0]
            zero_matrix[m][ind] = float(re.findall('\d*\.?\d+', x[n])[1])
    # Combine MS- intensities, m/z-values (columns) and retention times (rows) in one dataframe
    df_ms_neg = pd.DataFrame(zero_matrix)
    df_ms_neg.columns = mz_range
    df_ms_neg.index = ms_retention_times
    all_data["ms_neg"] = df_ms_neg

    return all_data


def _ms_post(file, all_data):
    """
    Grabs positive MS data from "_Seg1Ev1.JDX"
    compares the name with UV-file name to make sure that it is the rigth data.

    :param file: raw data file for MS data (Positive mode)
    :type file: str
    :param temp_file_name: list of file names to make
    :type temp_file_name: list
    :param temp_ms_neg: list of file names, to compare with UV, to make sure that the same data is added to the
        same sample/compound
    :type temp_ms_neg: list
    :param ms_pos_files: The Data
    :type ms_pos_files: list
    :return: ms_pos_files (MS data)
    :rtype: list
    """

    with open(file) as f:
        JDXfile = f.read()

    MS_file = JDXfile.split('##SCAN_NUMBER')
    # Delete first string in MS_file
    # self.ms_pos_file_name.append(MS_file[0].removeprefix("##TITLE= "))
    del MS_file[0]

    # MS+ measurements does not always include the first reading (scan number 1)
    # If the first reading is present it is deleted, to make sure all MS+
    # readings have the same dimensions

    if len(MS_file) == len(all_data["ms_neg"]):
        del MS_file[0]

    # Generate the m/z-values (ranges from 100 to 1000, with 0.05 intervals)
    # OBS: Change the m/z range here if needed
    mz_range = np.arange(100, 1000.05, 0.05)
    mz_range = mz_range.round(2)
    # Generate array with length of the total number of scans
    M = np.arange(0, len(MS_file), 1)
    # Generate zero matrix
    zero_matrix = np.zeros((len(M), len(mz_range)))
    # Empty retention time array
    MS_retention_times = []
    for m in M:
        x = MS_file[m]
        # Split MS_file at '/n'
        x = x.split('\n')
        # Extract retention times
        RT = re.findall('\d*\.?\d+', x[1].replace(",", "."))  # Extract retion time
        RT = float(np.asarray(RT))
        MS_retention_times.append(RT)
        # Extract MS+ data
        del x[0:5]
        del x[-1]
        # Delete '##END' in the end of the file
        if m == M[-1]:
            del x[-1]
        # Replace 0's in zero_matrix with detected m/z-values
        N = np.arange(0, len(x), 1)
        for n in N:
            x[n] = x[n].replace(",", ".", 1)
            x_mz = (float(re.findall('\d*\.?\d+', x[n])[0]))
            ind = np.where(mz_range == x_mz)[0][0]
            zero_matrix[m][ind] = float(re.findall('\d*\.?\d+', x[n])[1])
    # Combine MS+ intensities, m/z-values (columns) and retention times (rows) in one dataframe
    df_MS_pos = pd.DataFrame(zero_matrix)
    df_MS_pos.columns = mz_range
    df_MS_pos.index = MS_retention_times
    all_data["ms_pos"] = df_MS_pos
    return all_data

def _file_handler(file_list):
    """
    Goes through the full list of files and folders, and sends the right files to the right data handlers

    :param file_list: List of all files in a specific folder
    :type file_list: list
    :return: sample_id, batch_id, batch_dic, temp_file_name, uv_files, ms_neg_files, ms_pos_files, sample_date
    :rtype: list, list, dict, str, list, list, list, dict
    """

    # running each file type seperated, as their names are being checked against each other, to make sure that
    # there are files for each type of data. This could be changed for Threading, But then a different check needs
    # to be put in place

    row_id = 0
    all_data = {}

    for file in file_list:
        # uv files
        if file.endswith('.txt'):
            row_id += 1
            all_data = _uv_date(file, all_data, row_id)

    for file in file_list:
        # ms negativ files
        if file.endswith('Ev2.JDX'):

            sample = os.path.basename(file).removesuffix("_Seg1Ev2.JDX")
            all_data[sample] = _ms_neg(file, all_data[sample])

    for file in file_list:
        # ms positive files
        if file.endswith('Ev1.JDX'):
            sample = os.path.basename(file).removesuffix("_Seg1Ev1.JDX")
            all_data[sample] = _ms_post(file, all_data[sample])

    return all_data


def dm_controller(file_list):
    """
    access point for transforming raw data into a usefull formate

    :param file_list: list of all the UV and MS data files
    :type file_list: list
    :return:
        - all_data: Dict of all data
        - batch_dic: Dict of bach/plate with samples/compounds
        - uv_tensor, ms_pos_tensor, ms_neg_tensor: tensors for UV and MS data.
        - sample_date: date for the samples
    :rtype:
        - dict
        - dict
        - dict
        - dict
        - dict
        - str
    """
    all_data = _file_handler(file_list)


    return all_data


if __name__ == "__main__":
    from file_handler import get_file_list
    path = "C:/Users/phch/PycharmProjects/LC_data/HTE_analysis_tool/HTE_analysis_tool/data/P1"
    database = "SCore.db"
    file_list = get_file_list(path)

    test = DataMining()

    all_data, batch_dic, uv_tensor, ms_pos_tensor, ms_neg_tensor = test.dm_controller(path)


import os
import numpy as np
import pandas as pd
import re


class DataMining:
    def __str__(self):
        """
        Gets data out of LC/MS/MS files. UV data in TXT formate and MS data in JPEX formate.
        :return:
        all_data: Dict of all data
        batch_dic: Dict of bach/plate with samples/compounds
        uv_tensor, ms_pos_tensor, ms_neg_tensor: tensors for UV and MS data.
        """

    @staticmethod
    def _uv_date(file, temp_file_name, sample_id, sample_date, batch_id, batch_dic, uv_files):
        """
        grabs UV data based on files ending with ".txt"
        It also uses data in the UV-files for batch name, and sample name for the complete DataFrame.
        Uses the UV-file name for ID-ing what MS-files belongs to witch batch/sample to make sure  that the right data
        are combined in the final DataFrame.
        :param file: raw data file for UV data
        :param temp_file_name: List of file names of the data, to match it against MS data
        :param sample_id: List of compound id per sample
        :param batch_id: list of batch_id / plate_id
        :param batch_dic: a dictionary keys for batch/plate and values a list of samples/compounds
        :param uv_files: A list of the UV data
        :return: temp_file_name: name of the file for comparing with ms data
        sample_id: sample/compound id
        batch_id: batch/plate id
        batch_dic: a dictionary keys for batch/plate and values a list of samples/compounds
        uv_files: the UV data
        sample_date: date and time for the sample
        """

        temp_file = file.split("/")
        temp_uv_file_name = temp_file[-1].removesuffix(".txt")
        temp_uv_name_list = temp_uv_file_name.split("_")
        if temp_uv_name_list[-1].isdigit():
            temp_uv_name_list.pop()
        temp_uv_file_name = "_".join(temp_uv_name_list)
        temp_file_name.append(temp_uv_file_name)

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
                temp_time_date = x[2].split()

            # get sample information
            if x[0] == "[Sample Information]":
                temp_sample_id = x[6].split()
                sample_id.append(temp_sample_id[2])
                sample_date[temp_sample_id[2]] = [temp_time_date[1], temp_time_date[2]]


            # get batch information
            if x[0] == "[Original Files]":
                temp_batch_id = os.path.basename(x[3]).split(".")
                batch_id.append(temp_batch_id[0])
                batch_dic.setdefault(temp_batch_id[0], []).append(temp_sample_id[2])

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
        uv_intensity = pd.DataFrame(UV, columns=UV_wavelengths, index=UV_retention_times)
        uv_files.append(uv_intensity)

        return temp_file_name, sample_id, batch_id, batch_dic, uv_files, sample_date

    @staticmethod
    def _ms_neg(file, temp_file_name, ms_neg_files):
        """
        Grabs negative MS data from "_Seg1Ev2.JDX"
        compares the name with UV-file name to make sure that it is the right data.
        :param file: raw data file for MS data (Negative mode)
        :param temp_file_name: list of file names, to compare with UV, to make sure that the same data is added to the
        same sample/compound
        :param ms_neg_files: the MS data
        :return: temp_ms_neg(infomation for ms_positive to make sure the two type matches), ms_neg_files (MS Data)
        """
        temp_file = file.split("/")
        file_removedsuffix = temp_file[-1].removesuffix("_Seg1Ev2.JDX")
        # for values in self.temp_file_name:

        if file_removedsuffix in temp_file_name:

            with open(file) as f:
                JDXfile = f.read()
            # Split MS_file at '##SCAN_NUMBER'
            MS_file = JDXfile.split('##SCAN_NUMBER')
            # Delete first string in MS_file
            del MS_file[0]

            # used for checking len() of file later, to make sure that all arrays is the same size
            temp_ms_neg = MS_file
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
                # Extract MS- data
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
            # Combine MS- intensities, m/z-values (columns) and retention times (rows) in one dataframe
            df_MS_neg = pd.DataFrame(zero_matrix)
            df_MS_neg.columns = mz_range
            df_MS_neg.index = MS_retention_times
            ms_neg_files.append(df_MS_neg)

            return temp_ms_neg, ms_neg_files

    @staticmethod
    def _ms_post(file, temp_file_name, temp_ms_neg, ms_pos_files):
        """
        Grabs positive MS data from "_Seg1Ev1.JDX"
        compares the name with UV-file name to make sure that it is the rigth data.
        :param file: raw data file for MS data (Positive mode)
        :param temp_file_name: list of file names to make
        :param temp_ms_neg: list of file names, to compare with UV, to make sure that the same data is added to the
        same sample/compound
        :param ms_pos_files: The Data
        :return: ms_pos_files (MS data)
        """
        temp_file = file.split("/")
        file_removedsuffix = temp_file[-1].removesuffix("_Seg1Ev1.JDX")
        if file_removedsuffix in temp_file_name:

            with open(file) as f:
                JDXfile = f.read()

            MS_file = JDXfile.split('##SCAN_NUMBER')
            # Delete first string in MS_file
            # self.ms_pos_file_name.append(MS_file[0].removeprefix("##TITLE= "))
            del MS_file[0]

            # MS+ measurements does not always include the first reading (scan number 1)
            # If the first reading is present it is deleted, to make sure all MS+
            # readings have the same dimensions

            if len(MS_file) == len(temp_ms_neg):
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
            ms_pos_files.append(df_MS_pos)
        return ms_pos_files

    def _file_handler(self, file_list):
        """
        Goes through the full list of files and folders, and sends the right files to the right data handlers
        :param file_list: List of all files in a specific folder
        :return: sample_id, batch_id, batch_dic, temp_file_name, uv_files, ms_neg_files, ms_pos_files, sample_date
        """

        # running each file type seperated, as their names are being checked against each other, to make sure that
        # there are files for each type of data. This could be changed for Threading, But then a different check needs
        # to be put in place
        temp_file_name = []
        sample_id = []
        sample_date = {}
        batch_id = []
        batch_dic = {}
        uv_files = []
        ms_neg_files = []
        ms_pos_files = []

        for file in file_list:
            # uv files
            if file.endswith('.txt'):
                temp_file_name, sample_id, batch_id, batch_dic, uv_files, sample_date = \
                    self._uv_date(file, temp_file_name, sample_id, sample_date, batch_id, batch_dic, uv_files)

        for file in file_list:
            # ms negativ files
            if file.endswith('Ev2.JDX'):
                temp_ms_neg, ms_neg_files = self._ms_neg(file, temp_file_name, ms_neg_files)

        for file in file_list:
            # ms positive files
            if file.endswith('Ev1.JDX'):
                ms_pos_files = self._ms_post(file, temp_file_name, temp_ms_neg, ms_pos_files)

        return sample_id, batch_id, batch_dic, temp_file_name, uv_files, ms_neg_files, ms_pos_files, sample_date

    @staticmethod
    def _write_to_df(batch_id, sample_id, temp_file_name, uv_files, ms_pos_files, ms_neg_files):
        """
        writes all data to a DataFrame
        :param batch_id: List of batches/plates
        :param sample_id: list of samples/compounds
        :param temp_file_name: list of names for the files
        :param uv_files: UV data
        :param ms_pos_files: MS data (positive mode)
        :param ms_neg_files: MS data (negative mode)
        :return: all_data (all data writen together)
        """
        all_data = {}
        for batch in batch_id:
            all_data[batch] = {}

        for k in range(len(sample_id)):
            all_data[batch_id[k]][sample_id[k]] = {"file name": [], "data": [], "UV": [], "MS_pos": [], "MS_neg": []}
            all_data[batch_id[k]][sample_id[k]]["file name"] = temp_file_name[k]
            all_data[batch_id[k]][sample_id[k]]["UV"] = uv_files[k]
            all_data[batch_id[k]][sample_id[k]]["MS_pos"] = ms_pos_files[k]
            all_data[batch_id[k]][sample_id[k]]["MS_neg"] = ms_neg_files[k]


        return all_data

    @staticmethod
    def _tensor(all_data):
        """
        generate tensors out of the data.
        :param all_data: all_data, bach/plate, sample/compound uv, ms pos/neg data in one dict.
        :return: uv_tensor, ms_pos_tensor, ms_neg_tensor
        """

        uv_tensor = {}
        ms_pos_tensor = {}
        ms_neg_tensor = {}

        for batch in all_data:
            for value, samples in enumerate(all_data[batch]):

                uv_tensor[samples] = all_data[batch][samples]["UV"]
                ms_pos_tensor[samples] = all_data[batch][samples]["MS_pos"]
                ms_neg_tensor[samples] = all_data[batch][samples]["MS_neg"]

        return uv_tensor, ms_pos_tensor, ms_neg_tensor

    def dm_controller(self, file_list):
        """
        access point for transforming raw data into a usefull formate
        :param file_list: list of all the UV and MS data files
        :return:
        all_data: Dict of all data
        batch_dic: Dict of bach/plate with samples/compounds
        uv_tensor, ms_pos_tensor, ms_neg_tensor: tensors for UV and MS data.
        """
        sample_id, batch_id, batch_dic, temp_file_name, uv_files, ms_neg_files, ms_pos_files, sample_date = \
            self._file_handler(file_list)
        all_data = self._write_to_df(batch_id, sample_id, temp_file_name, uv_files, ms_pos_files, ms_neg_files)
        uv_tensor, ms_pos_tensor, ms_neg_tensor = self._tensor(all_data)
        return all_data, batch_dic, uv_tensor, ms_pos_tensor, ms_neg_tensor, sample_date


if __name__ == "__main__":
    from file_handler import get_file_list
    path = "C:/Users/phch/PycharmProjects/LC_data/HTE_analysis_tool/HTE_analysis_tool/data/P1"
    database = "SCore.db"
    file_list = get_file_list(path)

    test = DataMining()

    all_data, batch_dic, uv_tensor, ms_pos_tensor, ms_neg_tensor = test.dm_controller(path)


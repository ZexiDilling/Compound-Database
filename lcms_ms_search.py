import numpy as np
import configparser


class MassSearching:
    def __str__(self):
        """
        looks through ms-data in a tensor form. to locate peaks in the data.

        :return: a list of peaks for a specific sample/compound
        """
    @staticmethod
    def aduct_search(ms_mode):
        """
        Finds aduct from the config file, and add them to a list, that is used when going over the masses found.

        :param ms_mode: what mode the data is in. or is being looked at.
        :type ms_mode: str
        :return: A list of all aduct for either positive or negative ion-mode
        """
        config = configparser.ConfigParser()
        ms_aduct = []
        ions = []

        if ms_mode == 'pos':
            config.read("config.txt")
            for sections in config.sections():
                if sections == "Positive ion mode":
                    for ion in config[sections]:
                        ions.append(ion)
                        temp = config[sections][ion].split(",")
                        try:
                            ms_aduct.append([float(temp[0]), float(temp[1])])
                        except ValueError:
                            temp_2 = temp[1].split("/")
                            temp_2 = int(temp_2[0]) / int(temp_2[1])
                            ms_aduct.append([float(temp[0]), float(temp_2)])

        if ms_mode == 'neg':
            config.read("config.txt")
            for sections in config.sections():
                if sections == "Negative ion mode":
                    for ion in config[sections]:
                        ions.append(ion)
                        temp = config[sections][ion].split(",")
                        try:
                            ms_aduct.append([float(temp[0]), float(temp[1])])
                        except ValueError:
                            temp_2 = temp[1].split("/")
                            temp_2 = int(temp_2[0]) / int(temp_2[1])
                            ms_aduct.append([float(temp[0]), float(temp_2)])

        return ms_aduct, ions

    def mass_search(self, batch, sample, mass, delta_mass, ms_mode, peak_information, ms_tensor, mz_threshold, data):
        """
        M/z search function by top n m/z-values in a peak.
        A m/z value is significant if it is between the top n most intense peaks.

        :param batch: Bath/plate for the sample/compound
        :type batch: dict
        :param sample: The id for the sample/compound
        :type sample: str
        :param mass: Mass for the sample/compound
        :type mass: float
        :param delta_mass: +/- range for the mass search field
        :type delta_mass: float
        :param ms_mode: What mode the data is in. positive or negative
        :type ms_mode: str
        :param peak_information: Information from the uv date.
        :type peak_information: dict
        :param ms_tensor: The raw ms-data in tensor form
        :type ms_tensor: dict
        :param mz_threshold: The minimum amount of signal before the data is being recognised as a peak.
        :type mz_threshold: float
        :param data: All the data for all the compounds
        :type data: dict
        :return: A dict of peaks for ms-data
        :rtype: dict
        """

        ms_mz = data[batch][sample]["MS_pos"].columns
        ms_pos_rt = data[batch][sample]["MS_pos"].index
        ms_neg_rt = data[batch][sample]["MS_neg"].index
        peak_hit = {}
        peak_table = peak_information[batch][sample]
        peak_table_t = np.transpose(peak_table)

        for index, _ in enumerate(ms_tensor):
            ms_data_sample = ms_tensor[index]

        # Loop over all peaks in sample s
        for i in peak_table_t:
            # Find UV RT's (converted to seconds)
            uv_peak_start_rt = peak_table_t[i][2]*60
            uv_peak_end_rt = peak_table_t[i][3]*60
            # MS peaks appears later than the corresponding UV peaks in the spectrum
            # Add 12 seconds (0.2 min) to UV_peak_end_RT to correct for the above
            uv_peak_end_rt = uv_peak_end_rt+12

            if ms_mode == "pos":
                ms_peak_start_rt = ms_pos_rt[(np.fabs(ms_pos_rt - uv_peak_start_rt)).argmin(axis=0)]
                ms_peak_end_rt = ms_pos_rt[(np.fabs(ms_pos_rt - uv_peak_end_rt)).argmin(axis=0)]

                ms_peak_start_rt_index = [i for i, x in enumerate(ms_pos_rt == ms_peak_start_rt) if x][0]
                ms_peak_end_rt_index = [i for i, x in enumerate(ms_pos_rt == ms_peak_end_rt) if x][0]
            elif ms_mode == "neg":
                ms_peak_start_rt = ms_neg_rt[(np.fabs(ms_neg_rt - uv_peak_start_rt)).argmin(axis=0)]
                ms_peak_end_rt = ms_neg_rt[(np.fabs(ms_neg_rt - uv_peak_end_rt)).argmin(axis=0)]

                ms_peak_start_rt_index = [i for i, x in enumerate(ms_neg_rt == ms_peak_start_rt) if x][0]
                ms_peak_end_rt_index = [i for i, x in enumerate(ms_neg_rt == ms_peak_end_rt) if x][0]

            x_temp = ms_data_sample[ms_peak_start_rt_index:ms_peak_end_rt_index+1]
            x_sum = np.sum(x_temp, axis=0)
            idx = []
            for index, _ in enumerate(x_sum):
                if x_sum[index] > mz_threshold:
                    idx.append(index)

            mz_max_values = np.array(ms_mz[idx])
            mz_aduct, ions = self.aduct_search(ms_mode)

            for index, _ in enumerate(idx):
                for counter, aduct in enumerate(mz_aduct):
                    temp_mass = (mass * aduct[1]) + aduct[0]
                    if temp_mass-delta_mass < mz_max_values[index] < temp_mass+delta_mass:
                        peak_hit[peak_table_t[i][0]] = {}
                        peak_hit[peak_table_t[i][0]][ions[counter]] = mz_max_values[index]

        return peak_hit


if __name__ == "__main__":
    mz = MassSearching()
    test = mz.aduct_search("pos")
    print(test)


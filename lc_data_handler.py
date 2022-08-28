import numpy as np

from database_handler import DataBaseFunctions
from data_miner import dm_controller
from lcms_uv_integration import Integration
from lcms_ms_search import MassSearching


class LCMSHandler:
    def __init__(self, database="SCore.db"):
        self.dbf = DataBaseFunctions(database)
        self.lc_int = Integration()
        self.lc_ms = MassSearching()

    def __str__(self):
        """
        Finds and analyse data from LC/MS/MS

        :return: compound_info with MS, UV and purity data
        """

    @staticmethod
    def _temp_sample_setup(batch_dic_raw):
        """
        Makes a list of samples/compounds

        :param batch_dic_raw: a dict key: batch/plates value is a list of: samples/compounds
        :type batch_dic_raw: dict
        :return: a list of all samples
        :rtype: list
        """
        temp_sample = []
        for batch in batch_dic_raw:
            for sample in batch_dic_raw[batch]:
                temp_sample.append(sample)
        return temp_sample

    def _compound_info_generator(self, samples, sample_date):
        """
        Generates a dicts with information for each sample and finds the mass listed in the database for each sample

        :param samples: A list of all samples
        :type samples: list
        :return: a dicts with information for each sample, including information from the database.
        :rtype: dict
        """
        compound_info = {}
        for sample in samples:
            compound_info[sample] = {}
            compound_info[sample]["compound_id"] = sample
            compound_info[sample]["experiment"] = int
            compound_info[sample]["result_max"] = float
            compound_info[sample]["result_total"] = list
            compound_info[sample]["mass"] = float
            compound_info[sample]["Peak_Info"] = list
            compound_info[sample]["time_date"] = list
            compound_info[sample]["wavelength"] = float     # if wavelength is added, this can get that info too.
            table = "compound_main"

            item_id_1 = sample
            item_id_2 = sample
            item_header_1 = "compound_id"
            item_header_2 = "compound_id"

            row = self.dbf.find_data(table, item_id_1, item_id_2, item_header_1, item_header_2)
            try:
                compound_info[sample]["mass"] = row[0][3]
            except IndexError:
                print("sample do not exist in the database")
            compound_info[sample]["time_date"] = sample_date[sample]

        return compound_info

    def _integration_operator(self, data, batch_dict, samples, compound_info, uv_tensor, uv_one, uv_same_wavelength,
                             wavelength, uv_threshold, rt_solvent_peak):
        """
        Integrate UV data to get a peaktable out. with peak number, retention times and area.

        :param data: All data for the samples/compounds
        :type data: dict
        :param batch_dict: A dict with keys as batch/plates and values as a list of samples/compounds
        :type batch_dict: dict
        :param samples: A list of samples/compounds
        :type samples: list
        :param compound_info: A dict with information data for each sample/compound
        :type compound_info: dict
        :param uv_tensor: the uv-tensors for all the samples/compounds
        :type uv_tensor: dict
        :param uv_one: if the integration needs to use a single wavelenght to analyse the data or multiple
        :type uv_one: bool
        :param uv_same_wavelength: If it uses a single one, then looks at if it is the same wavelength for all the
            samples/compounds
        :type uv_same_wavelength: bool
        :param wavelength: all wavelengths - not used!!!!
        :type wavelength: float
        :param uv_threshold: minimum threshold for looking at UV-data. anything below will be ignored.
        :type uv_threshold: float
        :param rt_solvent_peak: retention time for the solvent peak
        :type rt_solvent_peak: float
        :return: a dataframe with peak information (retention  time, peak  numbers and area) for all the
            samples/compounds
        :rtype: dict
        """

        temp_wavelength = []

        # setup for running all wavelength
        if not uv_one:
            for _ in samples:
                temp_wavelength.append("all")
        else:
            # setting wavelength for all the sample to the same.
            if uv_same_wavelength:
                for _ in samples:
                    temp_wavelength.append(uv_same_wavelength)
            else:
                for sample in samples:

                    try:
                        temp_wavelength.append(compound_info[sample]["wavelength"])
                    except KeyError:
                        temp_wavelength.append(254)

        # Find integrals for batch P

        uv_peak_information = self.lc_int.calculate_uv_integrals(batch_dict, temp_wavelength, uv_threshold,
                                                                   uv_tensor, data, rt_solvent_peak)

        return uv_peak_information

    def _ms_search(self, data, batch_dict, ms_pos_tensor, ms_neg_tensor, mz_delta, ms_mode, mz_threshold,
                   uv_peak_information, compound_info):
        """
        Calls a function to looked at the ms-data  to find peak for the specific sample/compounds, including aduct.
        Aduct can be found in the config file

        :param data: All data for the samples/compounds
        :type data: dict
        :param batch_dict: A dict with keys as batch/plates values as a list of samples/compounds per batch/plate
        :type batch_dict: dict
        :param ms_pos_tensor: The tensor for ms_data in positive mode
        :type ms_pos_tensor: dict
        :param ms_neg_tensor: The tensor for ms_data in negative mode
        :type ms_neg_tensor: dict
        :param mz_delta: The raw ms-data in tensor form
        :type mz_delta: float
        :param ms_mode: What ms_mode to look at the data
        :type ms_mode: str
        :param mz_threshold: The minimum amount of signal before the data is being recognised as a peak.
        :type mz_threshold: float
        :param uv_peak_information: The uv information for peaks
        :type uv_peak_information: dict
        :param compound_info: All information for each sample/compound
        :type compound_info: dict
        :return: A dict for samples/compounds and what mass was found for each sample/compound
        :rtype: dict
        """

        temp_ms_pos_tensor = []
        temp_ms_neg_tensor = []
        for batch in batch_dict:
            for sample in batch_dict[batch]:
                temp_ms_pos_tensor.append(ms_pos_tensor[sample])
                temp_ms_neg_tensor.append(ms_neg_tensor[sample])
        temp_ms_pos_tensor = np.array(temp_ms_pos_tensor)
        temp_ms_neg_tensor = np.array(temp_ms_neg_tensor)

        if ms_mode:
            temp_ms_tensor = temp_ms_pos_tensor
            temp_ms_mode = "pos"
        else:
            temp_ms_tensor = temp_ms_neg_tensor
            temp_ms_mode = "neg"

        mass_hit = {}
        for batch in batch_dict:
            for sample in batch_dict[batch]:
                peak_hit = self.lc_ms.mass_search(batch, sample, compound_info[sample]["mass"], mz_delta, temp_ms_mode,
                                                  uv_peak_information, temp_ms_tensor, mz_threshold, data)

                if not peak_hit:
                    mass_hit[sample] = "No Hits"
                else:
                    mass_hit[sample] = peak_hit
        return mass_hit

    @staticmethod
    def _purity_mass(batch_dict, uv_peak_information, mass_hit, compound_info):
        """
        Compare the list of peak-information from uv with the peak-information for the ms-data

        :param batch_dict: Batch_dic_raw: a dict key: batch/plates value is a list of: samples/compounds
        :type batch_dict: dict
        :param uv_peak_information: Peak-information from uv-data for samples/compounds
        :type uv_peak_information: dict
        :param mass_hit: Peak-information from ms-data for samples/compounds
        :type mass_hit: dict
        :param compound_info: all information for each sample/compound
        :return: compound_info: information for all the compounds
        :rtype: dict
        """

        for batch in batch_dict:
            for sample in batch_dict[batch]:

                if mass_hit[sample] == "No Hits":
                    pass
                else:
                    for peak in mass_hit[sample]:
                        for index, row in uv_peak_information[batch][sample].iterrows():
                            if row[0] == peak:
                                mass_hit[sample][peak]["purity"] = row[4]

                compound_info[sample]["Peak_Info"] = mass_hit[sample]

        return compound_info

    def lc_controller(self, file_list, uv_one, uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak, mz_delta,
                      ms_mode, mz_threshold):
        """
        The control modul for the LC data, to control the flow of data into the different operations

        :param file_list: A list of files
        :type file_list: list
        :param uv_one: If it uses a single wavelenght or multiple
        :type uv_one: bool
        :param uv_same_wavelength: If it uses a single one, then looks at if it is the same wavelength for all the
            samples/compounds
        :type uv_same_wavelength: bool
        :param wavelength: all wavelengths - not used!!!!
        :type wavelength: float
        :param uv_threshold: minimum threshold for looking at UV-data. anything below will be ignored.
        :type uv_threshold: float
        :param rt_solvent_peak: retention time for the solvent peak
        :type rt_solvent_peak: float
        :param mz_delta: The raw ms-data in tensor form
        :type mz_delta: float
        :param ms_mode: What ms_mode to look at the data
        :type ms_mode: str
        :param mz_threshold: The minimum amount of signal before the data is being recognised as a peak.
        :type mz_threshold: float
        :return: The information for each compound if the mass have been found and the purity of the compound
        :rtype: dict
        """

        data, batch_dict, uv_tensor, ms_pos_tensor, ms_neg_tensor, sample_date = self.dm.dm_controller(file_list)
        samples = self._temp_sample_setup(batch_dict)
        compound_info = self._compound_info_generator(samples, sample_date)

        uv_peak_information = self._integration_operator(data, batch_dict, samples, compound_info, uv_tensor, uv_one,
                                                         uv_same_wavelength, wavelength, uv_threshold, rt_solvent_peak)

        mass_hit = self._ms_search(data, batch_dict, ms_pos_tensor, ms_neg_tensor, mz_delta, ms_mode, mz_threshold,
                                   uv_peak_information, compound_info)

        compound_info = self._purity_mass(batch_dict, uv_peak_information, mass_hit, compound_info)

        return compound_info

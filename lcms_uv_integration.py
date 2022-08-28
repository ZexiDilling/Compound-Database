import numpy as np
import scipy
import pandas as pd
import scipy.stats


class Integration:
    def __str__(self):
        """
        A modul for integrating UV data in tensor form. to find peaks area and height, and based on that, find the
        purity of a sample/compound

        :return: A Datafrom with uv-peak information.
        """
    @staticmethod
    def _integration_uv_wavelength(batch, sample, wavelength, uv_threshold, uv_tensor, data, rt_solvent_peak):
        """
        Calculate the integrals of the UV peaks using the trapezoid integration rule.
        Sum over one specific wavelength and calculate the UV peak integrals based on this.
        slope calculation notes:
            Find out when a peak start/stops based on the slope.
            Positive slope value indicate the begging of a peak and negative slope value indicate the end of a peak.
            Uses scipy.stats.linregress to calculate slope.
            Linregress is utilised to compute the linear least-squares regression for two given one-dimensional
            arrays of the same length.
            The slope thresholds can be changed, see '#OBS: Can change slope threshold here'.

        :param batch: batch/plate the sample is from
        :type batch: dict
        :param sample: sample/compound ID
        :type sample: str
        :param wavelength: what wavelength the integration is working at. can be all (limited to the data)
        :type wavelength: float
        :param uv_threshold: minimum threshold before data is being looked at. everything below is ignored
        :type uv_threshold: float
        :param uv_tensor: a tensor for the uv data for the specific sample
        :type uv_tensor: dict
        :param data: All data for all the samples
        :type data: dict
        :param rt_solvent_peak: retentions time for the solvent peak, to avoid data from that peak.
        :type rt_solvent_peak: float
        :return: df_integrate_overview is a pandas dataframe with peak list, integrals, peak start time and peak end
            time.
        :rtype: pandas.core.frame.DataFrame
        """

        uv_tensor = np.array(uv_tensor)
        uv_threshold = uv_threshold

        # Save both slope values and the corresponding retentions times
        slope = []
        st_slope = []

        # Define UV retention times in seconds and wavelengths
        uv_rt = data[batch][sample]['UV'].index*60
        if wavelength == "all":
            uv_tensor = np.sum(uv_tensor, axis=1)
            wave_indx = None

        else:
            uv_wavelengths = data[batch][sample]['UV'].columns
            # Find index of selected wavelength
            wave_number = uv_wavelengths[(np.fabs(uv_wavelengths-wavelength)).argmin(axis=0)]
            wave_indx = [i for i, x in enumerate(uv_wavelengths == wave_number) if x][0]

        # Calculate the slope based on 5 data points
        for rt in np.arange(0, len(uv_tensor[5:, wave_indx])):
            x = uv_rt.tolist()[(0+rt):(5+rt)]
            if wave_indx:
                y = uv_tensor[(0+rt):(5+rt), wave_indx]
            else:
                y = uv_tensor[(0 + rt):(5 + rt)]
            temp_slope = scipy.stats.linregress(x, y)[0]
            slope.append(temp_slope)
            st_slope.append(uv_rt[5+rt])

        # Find the start and end times based on the slope
        rt_start_peak = []
        rt_end_peak = []
        x = -1  # x makes sure the RT's are order correctly
        for s in np.arange(1, len(slope)-1):
            if slope[s] > uv_threshold < slope[s-1] and x < 0:
                rt_start_peak.append(st_slope[s])
                x = 1
            if slope[s] < -uv_threshold > slope[s+1] and x > 0:
                rt_end_peak.append(st_slope[s])
                x = -1

        # For the last peak it is possible only to detect rt_start_peak
        # If this happens, delete the last observation in rt_start_peak
        if len(rt_start_peak) > len(rt_end_peak):
            del(rt_start_peak[-1])

        rt_start_peak_new = []
        rt_end_peak_new = []

        # Deleting the solvent peak
        for x in np.arange(0, len(rt_start_peak)):
            if rt_start_peak[x]/60 > rt_solvent_peak:
                rt_start_peak_new.append(rt_start_peak[x])
                rt_end_peak_new.append(rt_end_peak[x])

        # Calculate the integrals numerically with trapezoid integration rule
        integrals = []
        for s in np.arange(0, len(rt_start_peak_new)):

            # Find index of start and end times
            indx_start = [i for i, x in enumerate(uv_rt == rt_start_peak_new[s]) if x][0]
            indx_end = [i for i, x in enumerate(uv_rt == rt_end_peak_new[s]) if x][0]

            # Calculate n, a, b and h
            n = len(uv_rt.tolist()[indx_start:indx_end+1])
            a = uv_rt.tolist()[indx_start]
            b = uv_rt.tolist()[indx_end]
            h = (b-a)/n

            # Define x and y values based on the peak time interval
            x = uv_rt.tolist()[indx_start:indx_end+1]
            if wave_indx:
                y = uv_tensor[indx_start:indx_end+1, wave_indx]
            else:
                y = uv_tensor[indx_start:indx_end + 1]

            # Calculate the integrals using the trapezoid integration rule
            int_list = []
            for i in range(len(x)):
                if i == 0 or i == n-1:
                    int_list.append(h/2*y[i])
                else:
                    int_list.append(h*y[i])
            integral = sum(int_list)
            integrals.append(round(integral))

        # Save peak information and collect it in a dataframe
        peak_list = []
        for rt in np.arange(0, len(rt_start_peak_new)):
            rt_start_peak_new[rt] = round(rt_start_peak_new[rt]/60, 3)
            rt_end_peak_new[rt] = round(rt_end_peak_new[rt]/60, 3)
            peak_list.append('Peak {}'.format(rt+1))

        integrals_total = sum(integrals)
        purity = []
        for x in integrals:
            pur = round((x/integrals_total) * 100, 3)
            purity.append(pur)

        # Save in a dataframe
        df = {'Peak list': peak_list, 'Integrals': integrals, 'Peak start time': rt_start_peak_new,
              'Peak end time': rt_end_peak_new, "purity": purity}

        df_integrate_overview = pd.DataFrame(df)
        if df_integrate_overview.empty:
            df = {'Peak list': ["No peaks detected"], 'Integrals': ["No peaks detected"], 'Peak start time':
                        ["No peaks detected"], 'Peak end time': ["No peaks detected"], "purity": ["No peaks detected"]}
            df_integrate_overview = pd.DataFrame(df)

        return df_integrate_overview

    def calculate_uv_integrals(self, batch_dict, wavelength, uv_threshold, uv_tensor, data, solvent_peak):
        """
        Calculate integrals for all samples in a plate and combine them to a list of pandas dataframes.
        One dataframe for each sample.
        A dataframe contains the following information, peak list, integrals, peak start time and peak and time.

        :param batch_dict: A dict with batch/plates and all samples/compounds for that one
        :type batch_dict: dict
        :param wavelength: a list of wavelength that the different samples/compound are going to be integrated at
        :type wavelength: list
        :param uv_threshold: minimum threshold before data is being looked at. everything below is ignored
        :type uv_threshold: float
        :param uv_tensor: a tensor for the uv data for the specific sample
        :type uv_tensor: dict
        :param data: All data for all the samples
        :type data: dict
        :param solvent_peak: retentions time for the solvent peak, to avoid data from that peak.
        :type solvent_peak: float
        :return: df_combined is a list of pandas dataframes.
        :rtype: dict
        """
        peak_information = {}

        # For now only works for all samples. Needs to make a new dict over samples and batches, to run this over,
        # to make it more flexible. It needs to be added to all methods using the module.

        for batch in data:
            peak_information[batch] = {}

        for batch in batch_dict:
            for value, sample in enumerate(batch_dict[batch]):
                temp_data_frame = self._integration_uv_wavelength(batch, sample, wavelength[value], uv_threshold,
                                                                  uv_tensor[sample], data, solvent_peak)

                peak_information[batch][sample] = temp_data_frame

        return peak_information

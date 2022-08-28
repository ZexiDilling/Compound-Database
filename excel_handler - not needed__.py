import pandas as pd


class ExcelReader:
    def __str__(self):
        """
        Reads excel files
        For now used to get plat-layout for DaughterPlates.

        :return: Data from excel file
        """

    # @staticmethod
    # def _plate_layout_import(sheet="384", file="Destination.xlsx"):
    #     """
    #     Import platelayout from a specific excel file. marked with blank(b), samples(s), reference(r)
    #     and export it as a panda-dataframe.
    #
    #     :param sheet: The worksheet for the excel filere where the data is added
    #     :type sheet: str
    #     :param file: Name of excel file
    #     :type file: str
    #     :return: A layout in Dataframe format
    #     :rtype: pandas.core.frame.DataFrame
    #     """
    #     df_plate = pd.read_excel(file, sheet_name=sheet, index_col=1, skiprows=1)
    #     del df_plate["Unnamed: 0"]
    #
    #     return df_plate

    # @staticmethod
    # def _counter(df, subject):
    #     """
    #     counts how many of each type (blank, sample, ref) there are.
    #
    #     :param df: Dataframe with the layout
    #     :type df: pandas.core.frame.DataFrame
    #     :param subject: What sample type that is being counted
    #     :return: A number for how many of b, s, or r sample that are in the plat-layout
    #     """
    #     counter = 0
    #
    #     for row in df.iterrows():
    #         for value in row[1]:
    #             if subject in value:
    #                 counter += 1
    #     return counter
    #
    # @staticmethod
    # def _from_excel_formatting(df):
    #     """
    #     turning the panda-datafrom into a dict.
    #
    #     :param df: Datafram with the plat-Layout
    #     :type df: pandas.core.frame.DataFrame
    #     :return: A dict with what is in each well. blank, sample or ref
    #     :rtype: dict
    #     """
    #     well_dict = {'blank': [], 'sample': [], 'ref': []}
    #     for keys in df:
    #         for key in df[keys]:
    #
    #             if df[keys][key] == "b":
    #                 well_dict["blank"].append(f"{key}{keys}")
    #             elif df[keys][key] == "s":
    #                 well_dict["sample"].append(f"{key}{keys}")
    #             elif df[keys][key] == "r":
    #                 well_dict["ref"].append(f"{key}{keys}")
    #
    #     return well_dict


    def layout_controller(self, data_ditch):
        """
        controls the formatting of the plate-layout

        :param plate_type: What type of plate (96, 384 or 1536)
        :type plate_type: str
        :param file: Excel file with the data
        :type file: str
        :return: A dict over what is in each well. a counter of how many samples
        :rtype: dict, int
        """

        # df_plate = self._plate_layout_import(plate_type, file)

        # counter_samples = self._counter(df_plate, "s")
        # counter_blank = self._counter(df_plate, "b")
        # counter_ref = self._counter(df_plate, "r")
        well_dict = self._formatting(data_ditch)

        # return well_dict, counter_samples, counter_blank, counter_ref

        return well_dict


if __name__ == "__main__":
    # file = "C:/Users/phch/PycharmProjects/plate_formatting/Destination.xlsx"
    # plate_type = "384"
    # er = ExcelReader()
    # er.layout_controller(file, plate_type)
    ...
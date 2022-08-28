import configparser
import types

from bio_data_functions import *


class ConfigWriter:
    def __init__(self, config, configfile="config.ini"):
        self.config = config
        self.config_file = configfile

    def delete_all_info(self, headline):
        for sub_headlines in self.config[headline]:
            self.config.remove_option(headline, sub_headlines)

        # self.config.clear(headline)

    def _setter(self, headline, constant, value):
        if not isinstance(value, types.FunctionType):
            self.config.set(headline, constant, str(value))

    def _bio_final_report(self, setting_dict):
        header = "Settings_bio"
        constant_start_string = "final_report"

        for headline in setting_dict:
            if headline == "calc":
                for sub_headline in setting_dict[headline]:
                    if sub_headline == "z_prime":
                        constant = f"{constant_start_string}_{headline}_{sub_headline}"
                        self._setter(header, constant, setting_dict[headline][sub_headline])
                    else:
                        for sub_sub_headline in setting_dict[headline][sub_headline]:
                            constant = f"{constant_start_string}_{headline}_{sub_headline}_{sub_sub_headline}"
                            self._setter(header, constant, setting_dict[headline][sub_headline][sub_sub_headline])
            elif headline == "pora_threshold" or headline == "data":
                for sub_headline in setting_dict[headline]:
                    for sub_sub_headline in setting_dict[headline][sub_headline]:
                        # for sub_sub_sub_headline in setting_dict[headline][sub_headline]:
                        constant = f"{constant_start_string}_{headline}_{sub_headline}_{sub_sub_headline}"

                        self._setter(header, constant,
                                     setting_dict[headline][sub_headline][sub_sub_headline])
            else:
                for sub_headline in setting_dict[headline]:
                    constant = f"{constant_start_string}_{headline}_{sub_headline}"
                    self._setter(header, constant, setting_dict[headline][sub_headline])

    def _bio_plate_report(self, setting_dict):
        header = "Settings_bio"
        constant_start_string = "plate_report"

        for headline in setting_dict:
            if headline == "calc_dict" or headline == "plate_calc_dict" or \
                    headline == "plate_analysis_dict" or headline == "pora_threshold":
                for sub_headline in setting_dict[headline]:
                    for sub_sub_headline in setting_dict[headline][sub_headline]:
                        if sub_sub_headline == "state" or sub_sub_headline == "calc":
                            for sub_sub_sub_headline in setting_dict[headline][sub_headline][sub_sub_headline]:

                                constant = f"{constant_start_string}_{headline}_{sub_headline}_{sub_sub_headline}_" \
                                           f"{sub_sub_sub_headline}"
                                self._setter(header, constant,
                                             setting_dict[headline][sub_headline][sub_sub_headline][
                                                 sub_sub_sub_headline])
                        else:
                            constant = f"{constant_start_string}_{headline}_{sub_headline}_{sub_sub_headline}"
                            self._setter(header, constant, setting_dict[headline][sub_headline][sub_sub_headline])

            elif headline == "pora_threshold" or headline == "data":
                for sub_headline in setting_dict[headline]:
                    for sub_sub_headline in setting_dict[headline][sub_headline]:
                        for sub_sub_sub_headline in setting_dict[headline][sub_headline]:
                            constant = f"{constant_start_string}_{headline}_{sub_headline}_{sub_sub_headline}_{sub_sub_sub_headline}"
                            self._setter(header, constant,
                                         setting_dict[headline][sub_headline][sub_sub_headline][sub_sub_sub_headline])

            elif headline == "z_prime_calc":
                constant = f"{constant_start_string}_{headline}"
                self._setter(header, constant, setting_dict[headline])

            else:
                for sub_headline in setting_dict[headline]:
                    constant = f"{constant_start_string}_{headline}_{sub_headline}"
                    self._setter(header, constant, setting_dict[headline][sub_headline])

    def _ms_ion_settings(self, setting_dict):
        header = ["Positive ion mode", "Negative ion mode"]

        for headline in setting_dict:
            for ions in setting_dict[headline]["positive"]:
                temp_config = self.config[header[0]][ions].split(",")
                temp_config.pop()
                temp_config = ",".join(value for value in temp_config)
                temp_config += f",{setting_dict[headline]['positive'][ions]}"
                self._setter(header[0], ions, temp_config)

            for ions in setting_dict[headline]["negative"]:
                temp_config = self.config[header[1]][ions].split(",")
                temp_config.pop()
                temp_config = ",".join(value for value in temp_config)
                temp_config += f",{setting_dict[headline]['negative'][ions]}"
                self._setter(header[1], ions, temp_config)

    def _simple_settings_writer(self, setting_dict):

        for headline in setting_dict:
            for sub_headline in setting_dict[headline]:
                print(headline)
                print(sub_headline)
                print(setting_dict[headline][sub_headline])
                self._setter(headline, sub_headline, setting_dict[headline][sub_headline])

    def _writer(self):

        with open(self.config_file, "w") as config_file:
            self.config.write(config_file)

    def run(self, setting_dict, name_setting, delete_all=False):

        if delete_all:
            for headline in setting_dict:
                self.delete_all_info(headline)

        if name_setting == "bio_full_report":
            self._bio_final_report(setting_dict)
        elif name_setting == "bio_plate_report":
            self._bio_plate_report(setting_dict)
        elif name_setting == "ms_ions_settings":
            self._ms_ion_settings(setting_dict)
        elif name_setting == "simple_settings":
            print(setting_dict)
            self._simple_settings_writer(setting_dict)

        self._writer()


if __name__ == "__main__":
    # bio_final_report_setup = {
    #     "methods": {"original": "test",
    #                 "normalised": "test",
    #                 "pora": "test"},
    #     "analyse": {"sample": "test",
    #                 "minimum": "test",
    #                 "max": "test",
    #                 "empty": "test",
    #                 "negative": "test",
    #                 "positive": "test",
    #                 "blank": "test"},
    #     "calc": {"original": {"overview": "test",
    #                           "sample": "test",
    #                           "minimum": "test",
    #                           "max": "test",
    #                           "empty": "test",
    #                           "negative": "test",
    #                           "positive": "test",
    #                           "blank": "test"},
    #              "normalised": {"overview": "test",
    #                             "sample": "test",
    #                             "minimum": "test",
    #                             "max": "test",
    #                             "empty": "test",
    #                             "negative": "test",
    #                             "positive": "test",
    #                             "blank": "test"},
    #              "pora": {"overview": "test",
    #                       "sample": "test",
    #                       "minimum": "test",
    #                       "max": "test",
    #                       "empty": "test",
    #                       "negative": "test",
    #                       "positive": "test",
    #                       "blank": "test"},
    #              "z_prime": "test"},
    #     "pora_threshold": {"low": {"min": "test",
    #                                "max": "test"},
    #                        "mid": {"min": "test",
    #                                "max": "test"},
    #                        "high": {"min": "test",
    #                                 "max": "test"}},
    #     "data": {"sample": {"matrix": "test",
    #                         "list": "test",
    #                         "max_min": "test"},
    #              "minimum": {"matrix": "test",
    #                          "list": "test",
    #                          "max_min": "test"},
    #              "max": {"matrix": "test",
    #                      "list": "test",
    #                      "max_min": "test"},
    #              "empty": {"matrix": "test",
    #                        "list": "test",
    #                        "max_min": "test"},
    #              "negative": {"matrix": "test",
    #                           "list": "test",
    #                           "max_min": "test"},
    #              "positive": {"matrix": "test",
    #                           "list": "test",
    #                           "max_min": "test"},
    #              "blank": {"matrix": "test",
    #                        "list": "test",
    #                        "max_min": "test"},
    #              "z_prime": {"matrix": "test",
    #                          "list": "test",
    #                          "max_min": "test"}}}
    # bio_plate_report_setup = {
    #     "well_states_report_method": {"original": "testing_this_thing",
    #                                   "normalised": "testing_this_thing",
    #                                   "pora": "testing_this_thing",
    #                                   "pora_internal": "testing_this_thing"},
    #     "well_states_report": {'sample': "testing_this_thing",
    #                            'blank': "testing_this_thing",
    #                            'max': "testing_this_thing",
    #                            'minimum': "testing_this_thing",
    #                            'positive': "testing_this_thing"
    #         ,
    #                            'negative': "testing_this_thing"
    #         ,
    #                            'empty': "testing_this_thing"},
    #     "calc_dict": {"original": {"use": "testing_this_thing",
    #                                             "avg": "testing_this_thing",
    #                                             "stdev": "testing_this_thing",
    #                                             "state": {"sample": "testing_this_thing"
    #                                                            "state_sample",
    #                                                       "minimum": "testing_this_thing"
    #                                                                      "state_minimum",
    #                                                       "max": "testing_this_thing"
    #                                                                      "state_max",
    #                                                       "empty": "testing_this_thing"
    #                                                                      "state_empty",
    #                                                       "negative": "testing_this_thing"
    #                                                                      "state_negative",
    #                                                       "positive": "testing_this_thing"
    #                                                                      "state_positive",
    #                                                       "blank": "testing_this_thing"
    #                                                                      "state_blank"}},
    #                                "normalised": {"use": "testing_this_thing",
    #                                               "avg": "testing_this_thing",
    #                                               "stdev": "testing_this_thinglate_report_plate_report_calc_dict_normalised_stdev",
    #                                               "state": {"sample": "testing_this_thing"
    #                                                              "state_sample",
    #                                                         "minimum": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_minimum",
    #                                                         "max": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_max",
    #                                                         "empty": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_empty",
    #                                                         "negative": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_negative",
    #                                                         "positive": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_positive",
    #                                                         "blank": "testing_this_thinglate_report_plate_report_calc_dict_normalised_"
    #                                                             "state_blank"}},
    #                                "pora": {"use": "testing_this_thing",
    #                                         "avg": "testing_this_thing",
    #                                         "stdev": "testing_this_thing",
    #                                         "state": {"sample": "testing_this_thing"
    #                                                        ,
    #                                                   "minimum": "testing_this_thing"
    #                                                                  "minimum",
    #                                                   "max": "testing_this_thinglate_report_plate_report_calc_dict_pora_state_max",
    #                                                   "empty": "testing_this_thinglate_report_plate_report_calc_dict_pora_state_empty"
    #                                             ,
    #                                                   "negative": "testing_this_thing"
    #                                                                  "negative",
    #                                                   "positive": "testing_this_thing"
    #                                                                  "positive",
    #                                                   "blank": "testing_this_thinglate_report_plate_report_calc_dict_pora_state_blank"
    #                                                   }},
    #                                "pora_internal": {"use": "testing_this_thing"
    #                                    ,
    #                                                  "avg": "testing_this_thinglate_report_plate_report_calc_dict_pora_internal_avg"
    #                                    ,
    #                                                  "stdev": "testing_this_thing"
    #                                                                 "stdev",
    #                                                  "state": {"sample": "testing_this_thing"
    #                                                                 "internal_state_sample",
    #                                                            "minimum": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_minimum",
    #                                                            "max": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_max",
    #                                                            "empty": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_empty",
    #                                                            "negative": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_negative",
    #                                                            "positive": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_positive",
    #                                                            "blank": "testing_this_thinglate_report_plate_report_calc_dict_pora_"
    #                                                                "internal_state_blank"}},
    #                                "other": {"use": "testing_this_thing",
    #                                               "calc": {"z_prime": "testing_this_thing"
    #                                                              "z_prime"}}},
    #     "plate_calc_dict": {
    #         "original": {"use": "testing_this_thing",
    #                      "avg": "testing_this_thing",
    #                      "stdev": "testing_this_thing",
    #                      "state": {"sample": "testing_this_thing",
    #                                "minimum": "testing_this_thing",
    #                                "max": "testing_this_thing",
    #                                "empty": "testing_this_thing",
    #                                "negative": "testing_this_thing",
    #                                "positive": "testing_this_thing",
    #                                "blank": "testing_this_thing"}},
    #         "normalised": {"use": "testing_this_thing",
    #                        "avg": "testing_this_thing",
    #                        "stdev": "testing_this_thing",
    #                        "state": {"sample": "testing_this_thing",
    #                                  "minimum": "testing_this_thing",
    #                                  "max": "testing_this_thing",
    #                                  "empty": "testing_this_thing",
    #                                  "negative": "testing_this_thing",
    #                                  "positive": "testing_this_thing",
    #                                  "blank": "testing_this_thing"}},
    #         "pora": {"use": "testing_this_thing",
    #                  "avg": "testing_this_thing",
    #                  "stdev": "testing_this_thing",
    #                  "state": {"sample": "testing_this_thing",
    #                            "minimum": "testing_this_thing",
    #                            "max": "testing_this_thing",
    #                            "empty": "testing_this_thing",
    #                            "negative": "testing_this_thing",
    #                            "positive": "testing_this_thing",
    #                            "blank": "testing_this_thing"}},
    #         "pora_internal": {"use": "testing_this_thing",
    #                           "avg": "testing_this_thing",
    #                           "stdev": "testing_this_thing",
    #                           "state": {"sample": "testing_this_thing",
    #                                     "minimum": "testing_this_thing",
    #                                     "max": "testing_this_thing",
    #                                     "empty": "testing_this_thing",
    #                                     "negative": "testing_this_thing",
    #                                     "positive": "testing_this_thing",
    #                                     "blank": "testing_this_thing"}},
    #     },
    #     "plate_analysis_dict": {"original": {"use": "testing_this_thing",
    #                                          "methode": org,
    #                                          "state_map": "testing_this_thing",
    #                                          "heatmap": "testing_this_thing",
    #                                          "hit_map": "testing_this_thing",
    #                                          "none": "testing_this_thing"},
    #                             "normalised": {"use": "testing_this_thing",
    #                                            "methode": norm,
    #                                            "state_map": "testing_this_thing",
    #                                            "heatmap": "testing_this_thing",
    #                                            "hit_map": "testing_this_thing",
    #                                            "none": "testing_this_thing"},
    #                             "pora": {"use": "testing_this_thing",
    #                                      "methode": pora,
    #                                      "state_map": "testing_this_thing",
    #                                      "heatmap": "testing_this_thing",
    #                                      "hit_map": "testing_this_thing",
    #                                      "none": "testing_this_thing"},
    #                             "pora_internal": {"use": "testing_this_thing",
    #                                               "methode": pora_internal,
    #                                               "state_map": "testing_this_thing",
    #                                               "heatmap": "testing_this_thing",
    #                                               "hit_map": "testing_this_thing",
    #                                               "none": "testing_this_thing"}
    #                             },
    #     "z_prime_calc": "testing_this_thing",
    #     "heatmap_colours": {'start': "testing_this_thing",
    #                                  'mid': "testing_this_thing",
    #                                  'end': "testing_this_thing"},
    #     "pora_threshold": {"low": {"min": "testing_this_thing",
    #                                "max": "testing_this_thing"},
    #                        "mid": {"min": "testing_this_thing",
    #                                "max": "testing_this_thing"},
    #                        "high": {"min": "testing_this_thing",
    #                                 "max": "testing_this_thing"},
    #                        "colour": {"low": "testing_this_thing",
    #                                  "mid": "testing_this_thing",
    #                                  "high": "testing_this_thing"}
    #                        }}
    #

    config = configparser.ConfigParser()
    config.read("config_test.ini")

    ms_settings = {
        "ions": {"positive": {
            "m+3h": bool(config["Positive ion mode"]["m+3h"].split(",")[-1]),
            "m+2h+na": bool(config["Positive ion mode"]["m+2h+na"].split(",")[-1]),
            "m+h+2na": bool(config["Positive ion mode"]["m+h+2na"].split(",")[-1]),
            "m+3na": bool(config["Positive ion mode"]["m+3na"].split(",")[-1]),
            "m+2h": bool(config["Positive ion mode"]["m+2h"].split(",")[-1]),
            "m+h+nh4": bool(config["Positive ion mode"]["m+h+nh4"].split(",")[-1]),
            "m+h+na": bool(config["Positive ion mode"]["m+h+na"].split(",")[-1]),
            "m+h+k": bool(config["Positive ion mode"]["m+h+k"].split(",")[-1]),
            "m+acn+2h": bool(config["Positive ion mode"]["m+acn+2h"].split(",")[-1]),
            "m+2na": bool(config["Positive ion mode"]["m+2na"].split(",")[-1]),
            "m+2acn+2h": bool(config["Positive ion mode"]["m+2acn+2h"].split(",")[-1]),
            "m+3acn+2h": bool(config["Positive ion mode"]["m+3acn+2h"].split(",")[-1]),
            "m+h": bool(config["Positive ion mode"]["m+h"].split(",")[-1]),
            "m+nh4": bool(config["Positive ion mode"]["m+nh4"].split(",")[-1]),
            "m+na": bool(config["Positive ion mode"]["m+na"].split(",")[-1]),
            "m+ch3oh+h": bool(config["Positive ion mode"]["m+ch3oh+h"].split(",")[-1]),
            "m+k": bool(config["Positive ion mode"]["m+k"].split(",")[-1]),
            "m+acn+h": bool(config["Positive ion mode"]["m+acn+h"].split(",")[-1]),
            "m+2na-h": bool(config["Positive ion mode"]["m+2na-h"].split(",")[-1]),
            "m+isoprop+h": bool(config["Positive ion mode"]["m+isoprop+h"].split(",")[-1]),
            "m+acn+na": bool(config["Positive ion mode"]["m+acn+na"].split(",")[-1]),
            "m+2k+h": bool(config["Positive ion mode"]["m+2k+h"].split(",")[-1]),
            "m+dmso+h": bool(config["Positive ion mode"]["m+dmso+h"].split(",")[-1]),
            "m+2acn+h": bool(config["Positive ion mode"]["m+2acn+h"].split(",")[-1]),
            "m+isoprop+na+h": bool(config["Positive ion mode"]["m+isoprop+na+h"].split(",")[-1]),
            "2m+h": bool(config["Positive ion mode"]["2m+h"].split(",")[-1]),
            "2m+nh4": bool(config["Positive ion mode"]["2m+nh4"].split(",")[-1]),
            "2m+na": bool(config["Positive ion mode"]["2m+na"].split(",")[-1]),
            "2m+3h2o+2h": bool(config["Positive ion mode"]["2m+3h2o+2h"].split(",")[-1]),
            "2m+k": bool(config["Positive ion mode"]["2m+k"].split(",")[-1]),
            "2m+acn+h": bool(config["Positive ion mode"]["2m+acn+h"].split(",")[-1]),
            "2m+acn+na": bool(config["Positive ion mode"]["2m+acn+na"].split(",")[-1])
        },
            "negative": {
                "m-3h": bool(config["Negative ion mode"]["m-3h"].split(",")[-1]),
                "m-2h": bool(config["Negative ion mode"]["m-2h"].split(",")[-1]),
                "m-h2o-h": bool(config["Negative ion mode"]["m-h2o-h"].split(",")[-1]),
                "m-h": bool(config["Negative ion mode"]["m-h"].split(",")[-1]),
                "m+na-2h": bool(config["Negative ion mode"]["m+na-2h"].split(",")[-1]),
                "m+cl": bool(config["Negative ion mode"]["m+cl"].split(",")[-1]),
                "m+k-2h": bool(config["Negative ion mode"]["m+k-2h"].split(",")[-1]),
                "m+fa-h": bool(config["Negative ion mode"]["m+fa-h"].split(",")[-1]),
                "m+hac-h": bool(config["Negative ion mode"]["m+hac-h"].split(",")[-1]),
                "m+br": bool(config["Negative ion mode"]["m+br"].split(",")[-1]),
                "m+tfa-h": bool(config["Negative ion mode"]["m+tfa-h"].split(",")[-1]),
                "2m-h": bool(config["Negative ion mode"]["2m-h"].split(",")[-1]),
                "2m+fa-h": bool(config["Negative ion mode"]["2m+fa-h"].split(",")[-1]),
                "2m+hac-h": bool(config["Negative ion mode"]["2m+hac-h"].split(",")[-1]),
                "3m-h": bool(config["Negative ion mode"]["3m-h"].split(",")[-1]),
            }
        }
    }

    name_setting = "ms_ions_settings"

    cw = ConfigWriter(config)

    cw.run(ms_settings, name_setting)
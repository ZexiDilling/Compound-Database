from extra_functions import rgb_to_hex, hex_to_rgb


class Heatmap:
    def __init__(self):
        self.fact_cache = {}

    @staticmethod
    def _color_dict(gradient):
        """ Takes in a list of RGB sub-lists and returns dictionary of
        colors in RGB and hex form for use in a graphing function
        defined later on """
        return {"hex": [rgb_to_hex(rgb) for rgb in gradient],
                "r": [rgb[0] for rgb in gradient],
                "g": [rgb[1] for rgb in gradient],
                "b": [rgb[2] for rgb in gradient]}

    def _linear_gradient(self, start_hex, end_hex="#FFFFFF", colour_amount=1000):
        ''' returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") '''
        # Starting and ending colors in RGB form
        start_colour = hex_to_rgb(start_hex)
        end_colour = hex_to_rgb(end_hex)

        # Initialize a list of the output colors with the starting color
        rgb_list = [start_colour]

        # Calculate a color at each evenly spaced value of t from 1 to n
        for counter in range(1, colour_amount):

            # Interpolate RGB vector for color at the current value of t
            curr_vector = [int(start_colour[column] + (float(counter) / (colour_amount-1)) *
                               (end_colour[column] - start_colour[column])) for column in range(3)]

            # Add it to our list of output colors
            rgb_list.append(curr_vector)

        return self._color_dict(rgb_list)

    def _poly_linear_gradient(self, colors, n):
        ''' returns a list of colors forming linear gradients between
          all sequential pairs of colors. "n" specifies the total
          number of desired output colors '''
        # The number of colors per individual linear gradient
        n_out = int(float(n) / (len(colors) - 1))
        # returns dictionary defined by color_dict()
        gradient_dict = self._linear_gradient(colors[0], colors[1], n_out)

        if len(colors) > 1:
            for col in range(1, len(colors) - 1):
                next = self._linear_gradient(colors[col], colors[col+1], n_out)
                for k in ("hex", "r", "g", "b"):
                    # Exclude first point to avoid duplicates
                    gradient_dict[k] += next[k][1:]

        return gradient_dict

    @staticmethod
    def _convert_percentiles(well_dict, percentiles):

        well_values = [value for wells, value in well_dict.items() if value != "nan"]
        max_values = max(well_values)
        min_values = min(well_values)

        percentile_dict = {"high": {"max": max_values, "min": "", "mid": ""},
                           "low": {"max": "", "min": min_values, "mid": ""}}

        if percentiles["low"] != 0:
            percentile_dict["low"]["max"] = (max_values / 100) * percentiles["low"]
        else:
            percentile_dict["low"]["max"] = min_values

        if percentiles["high"] != 100:
            percentile_dict["high"]["min"] = (max_values / 100) * percentiles["high"]
        else:
            percentile_dict["high"]["min"] = max_values

        if percentiles["mid"]:
            percentile_dict["high"]["mid"] = (((max_values - min_values) / 100) * percentiles["mid"]) + min_values
            percentile_dict["low"]["mid"] = (((max_values - min_values)/ 100) * percentiles["mid"]) + min_values

        print(percentile_dict)
        return percentile_dict, max_values, min_values

    @staticmethod
    def _samples_per_percentile(well_dict, percentile_dict, colour_amount):

        wells_percentile_dict = {}

        for well in well_dict:
            wells_percentile_dict[well] = {}

            if well_dict[well] >= percentile_dict["high"]["mid"]:
                wells_percentile_dict[well]["percentile"] = "high"
                if percentile_dict["high"]["max"] >= well_dict[well] >= percentile_dict["high"]["min"]:
                    wells_percentile_dict[well]["colour_value"] = colour_amount
                else:
                    percent_of_range = 100 / (percentile_dict["high"]["min"] - percentile_dict["high"]["mid"]) * \
                                           (well_dict[well] - percentile_dict["high"]["mid"])

                    colour_value = colour_amount/100 * percent_of_range
                    wells_percentile_dict[well]["colour_value"] = colour_value

            elif percentile_dict["high"]["mid"] > well_dict[well] >= percentile_dict["low"]["min"]:
                wells_percentile_dict[well]["percentile"] = "low"
                if percentile_dict["low"]["max"] >= well_dict[well] >= percentile_dict["low"]["min"]:
                    wells_percentile_dict[well]["colour_value"] = 0
                else:
                    percent_of_range = 100 / (percentile_dict["low"]["mid"] - percentile_dict["low"]["max"]) * \
                                           (well_dict[well] - percentile_dict["low"]["max"])

                    colour_value = colour_amount/100 * percent_of_range

                    wells_percentile_dict[well]["colour_value"] = colour_value
                #
                # if well_dict[well] >= percentile_dict[percentile]:
                #     try:
                #         if wells_percentile_dict[well]["lower_bound"] < percentile_dict[percentile]:
                #             wells_percentile_dict[well]["lower_bound"] = percentile
                #     except KeyError:
                #         wells_percentile_dict[well]["lower_bound"] = percentile
                #
                # if well_dict[well] <= percentile_dict[percentile]:
                #     try:
                #         if wells_percentile_dict[well]["upper_bound"] > percentile_dict[percentile]:
                #             wells_percentile_dict[well]["upper_bound"] = percentile_dict[percentile]
                #     except KeyError:
                #         wells_percentile_dict[well]["upper_bound"] = percentile_dict[percentile]

        return wells_percentile_dict

    @staticmethod
    def dict_convert(well_dict, state_dict, states):
        heatmap_dict = {}
        for well in well_dict:
            if state_dict[well]["state"] in states:
                heatmap_dict[well] = well_dict[well]

        return heatmap_dict

    @staticmethod
    def get_well_colour(colour_dict, wells_percentile_dict, well_dict, well):

        # temp_well_value = round(well_dict[well] / well_percentile_dict[well]["upper_bound"] * 1000)
        # well_percentile = well_percentile_dict[well]["lower_bound"]
        try:
            colour_bound = wells_percentile_dict[well]["percentile"]
        except KeyError:
            return "white"
        well_colour_value = round(wells_percentile_dict[well]["colour_value"])
        try:
            well_colour = colour_dict[colour_bound]["hex"][well_colour_value]
        except IndexError:
            well_colour = colour_dict[colour_bound]["hex"][-1]
        return well_colour

    def heatmap_colours(self, well_dict, percentile, colours):

        percentile_dict, max_values, min_values = self._convert_percentiles(well_dict, percentile)

        colour_amount = 1000
        colour_dict = {}
        for percentile in percentile_dict:
            colour_dict[percentile] = self._poly_linear_gradient(colours[percentile], colour_amount)

        well_percentile_dict = self._samples_per_percentile(well_dict, percentile_dict, colour_amount)

        return colour_dict, well_percentile_dict, max_values, min_values


if __name__ == "__main__":
    start_hex = "#5cb347"
    end_hex = "#5cb347"
    mid_2 = "#5cb347"
    mid_3 = "#5cb347"
    mid_hex = [2, 1]

    colour_list = [start_hex, mid_2, mid_2, mid_3, mid_3, end_hex]
    hm = Heatmap()
    print(hm.bezier_gradient(colour_list, 5))
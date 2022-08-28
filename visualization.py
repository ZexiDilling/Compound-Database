import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def uv_chromatogram(data, canvas, samples):
    """uv chromatogram of different sample(s) in the same plate.
    Summed over all wavelength and plots intensity as a function of retention time.
    Samples is a vector with the sample number(s) of intrest.
    P is the plate number.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor. When calling the function it is only necessary to define plate number (P).
    Data is the main dictionary containing all data."""
    # Define uv retention times
    uv_tensor = []
    for index, sample in enumerate(samples):
        if index == 0:
            uv_rt = data[sample]["uv"].index
        uv_tensor.append(data[sample]["uv"])

    uv_tensor = np.array(uv_tensor)

    # Sum over all wavelengths
    uv_tensor_sum_wavelengths = np.sum(uv_tensor, axis=2)
    # Plot figure
    fig, ax = plt.subplots()
    for index, sample in enumerate(samples):
        plt.plot(uv_tensor_sum_wavelengths[index, :], label=sample)
    plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
    ax.set_xticks(list(range(0, len(uv_rt), 75)))
    ax.set_xticklabels([str(x) for x in uv_rt[::75]])
    ax.set_xlabel(r'Retention time [min]')
    ax.set_ylabel(r'Intensity [a.u.]')
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def MS_chromatogram(samples, plates, ms_mode, ms_tensor, data, canvas):
    """MS(+ or -) chromatogram for one or several sample(s).
    Plots intensity as a function of retention time.
    Samples is a vector with the sample number(s) of intrest.
    P is the plate number.
    MS_mode can only take 'positive' or 'negative' as input.
    MS_tensor is the tensor of intrest, e.g. P4_MS_pos_tensor.
    data is the main dictionary containing all data."""
    # Positive MS mode
    if ms_mode == 'pos':
        # Find MS retention times and convert to minutes from seconds

        ms_rt = np.round(data[plates[0]][samples[0]]['MS_pos'].index/60, 2)
        graph_name = 'MS+ chromatogram'
    else:
        ms_rt = np.round(data[plates[0]][samples[0]]['MS_pos'].index / 60, 2)
        graph_name = 'MS- chromatogram'

    # Sum over all mz-values

    ms_tensor_sum_mz = np.sum(ms_tensor, axis=2)
    # Plot figure
    fig, ax = plt.subplots()

    for value, sample in enumerate([value - 1 for value, sample in enumerate(samples)]):
        plt.plot(ms_tensor_sum_mz[value, :], label=samples[value])
    plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
    ax.set_xticks(list(range(0, len(ms_rt), 5)))
    ax.set_xticklabels([str(x) for x in ms_rt[::5]])
    ax.set_xlabel(r'Retention time [s]')
    ax.set_ylabel(r'Intensity [a.u.]')
    plt.xticks(rotation=90)
    plt.title(graph_name)

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def MS_spectrum(samples, plates, rt_mz, ms_mode, ms_tensor, data, canvas):
    """MS(+ or -) spectrum of one or several sample(s) at one retention time.
    Plots intensity as a function of m/z-values.
    samples is a vector with the sample number(s) of intrest.
    P is the plate number.
    RT_mz is the retention time of interest.
    MS_mode can only take 'positive' or 'negative' as input.
    MS_tensor is the tensor of intrest, e.g. P4_MS_pos_tensor.
    data is the main dictionary containing all data."""
    #Convert to seconds
    rt_mz = rt_mz*60
    # Positive MS mode
    if ms_mode == 'pos':
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_pos'].columns
        ms_RT = (data[plates[0]][samples[0]]['MS_pos'].index)
        graph_name = 'MS+'
    else:
        ms_mz = data[plates[0]][samples[0]]['MS_pos'].columns
        ms_RT = (data[plates[0]][samples[0]]['MS_pos'].index)
        graph_name = 'MS-'

    # Find index for selected retention time
    rt_closest_value = ms_RT[(np.fabs(ms_RT-rt_mz)).argmin(axis=0)]
    rt_indx = [i for i, x in enumerate(ms_RT == rt_closest_value) if x][0]
    # Plot figure
    fig, ax = plt.subplots()
    #for sample in [sample - 1 for sample in samples]:
    for value, sample in enumerate([value - 1 for value, sample in enumerate(samples)]):
        plt.plot(ms_tensor[value, rt_indx, :], label=samples[value])
    plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
    ax.set_xticks(list(range(0, len(ms_mz), 500)))
    ax.set_xticklabels([str(x) for x in ms_mz[::500]])
    ax.set_xlabel(r'm/z')
    ax.set_ylabel(r'Intensity [a.u.]')
    plt.xticks(rotation=90)
    plt.title(graph_name + ' plot at {} minutes'.format(round(ms_RT[rt_indx]/60, 1)))

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

### Heat maps
def heatmap_uv_sample(samples, plates, uv_tensor, data, canvas):
    """uv heatmap for one specific sample.
    sample is the sample number of interest.
    P is the plate number.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Define uv wavelengtjs and retention times
    uv_wavelengths = np.round(data[plates[0]][samples[0]]['UV'].columns, 1)
    uv_rt = data[plates[0]][samples[0]]['UV'].index
    #Plot figure
    fig, ax = plt.subplots()
    for value, sample in enumerate(samples):
        sns.heatmap(uv_tensor[value-1, :, :], ax=ax, center=0)
    ax.set_xticks(list(range(0, len(uv_wavelengths), 25)))
    ax.set_xticklabels([str(x) for x in uv_wavelengths[::25]])
    ax.set_yticks(list(range(0, len(uv_rt), 50)))
    ax.set_yticklabels([str(x) for x in uv_rt[::50]])
    ax.set_xlabel(r'Wavelength [nm]')
    ax.set_ylabel(r'Retention time [min]')
    plt.title("UV/Vis heat map for plate {} sample {}".format(plates, samples))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def heatmap_uv_rt(samples, plates, rt_value, uv_tensor, data, canvas):
    """uv heatmap for one specific retention time.
    RT_value is the rention time of interest.
    P is the plate number.
    samples is a vector with the sample number(s) of intrest.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Extract uv data for the given samples
    uv_tensor_samples = []
    for value, sample in enumerate(samples):
        uv_tensor_samples.append(uv_tensor[value-1])
    uv_tensor_samples = np.array(uv_tensor_samples)
    # Define uv wavelengths and retention times
    uv_wavelengths = data[plates[0]][samples[0]]['UV'].columns
    uv_rt = data[plates[0]][samples[0]]['UV'].index
    # Find index for selected retention time
    rt_closest_value = uv_rt[(np.fabs(uv_rt-rt_value)).argmin(axis=0)]
    rt_indx = [i for i, x in enumerate(uv_rt == rt_closest_value) if x][0]
    #Plot figure
    fig, ax = plt.subplots()
    sns.heatmap(uv_tensor_samples[:, rt_indx, :], ax=ax, center=0)
    ax.set_xticks(list(range(0, len(uv_wavelengths), 25)))
    ax.set_xticklabels([str(x) for x in uv_wavelengths[::25]])
    ax.set_yticklabels(samples)
    ax.set_xlabel(r'Wavelength [nm]')
    ax.set_ylabel(r'Sample number')
    plt.title("UV/Vis heat map at {} min".format(uv_rt[rt_indx]))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def heatmap_uv_wavelength(samples, plates, wavelength, uv_tensor, data, canvas):
    """uv heatmap for one specific wavelength.
    RT_value is the rention time of interest.
    P is the plate number.
    samples is a vector with the sample number(s) of intrest.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Extract uv data for the given samples
    uv_tensor_samples = []
    for value, sample in enumerate(samples):
        uv_tensor_samples.append(uv_tensor[value-1])
    uv_tensor_samples = np.array(uv_tensor_samples)
    # Define uv wavelengths and retention times
    uv_wavelengths = data[plates[0]][samples[0]]['UV'].columns
    uv_rt = data[plates[0]][samples[0]]['UV'].index
    # Find index for selected wavelength
    wave_number = uv_wavelengths[(np.fabs(uv_wavelengths-wavelength)).argmin(axis=0)]
    wave_indx = [i for i, x in enumerate(uv_wavelengths == wave_number) if x][0]
    #Plot figure
    fig, ax = plt.subplots()
    sns.heatmap(uv_tensor_samples[:, :, wave_indx], ax=ax, center=0)
    sns.color_palette("vlag", as_cmap=True)
    ax.set_xticks(list(range(0, len(uv_rt), 50)))
    ax.set_xticklabels([str(x) for x in uv_rt[::50]])
    ax.set_yticklabels(samples)
    ax.set_xlabel(r'Retention time [min]')
    ax.set_ylabel(r'Sample number')
    plt.title("UV/Vis heat map at wavelength {} nm".format(uv_wavelengths[wave_indx]))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def heatmap_MS_sample_binned(samples, plates, bin_numbers, ms_mode, ms_tensor, data, canvas):
    """MS heatmap for one specific sample with binned m/z-values.
    sample is the sample number of interest.
    P is the plate number.
    MS_mode is either 'pos' or 'neg'.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Positive MS mode
    if ms_mode == 'pos':
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_pos'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_pos'].index
        graph_name = "MS(+)"
    else:
        ms_mz = data[plates[0]][samples[0]]['MS_neg'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_neg'].index
        graph_name = "MS(-)"

    for value, sample in enumerate(samples):
        temp_value = value
    ms_rt = np.round(ms_rt / 60, 1)
    # Bin m/z-values accoridng to the number of bins defined
    ms = []
    ms_columns = []
    bin_size = round(len(ms_mz)/bin_numbers)
    for i in range(0, bin_numbers):
        if i == 0:
            ms.append(np.sum(ms_tensor[temp_value-1, :, 0:bin_size+bin_size], axis=1))
            ms_columns.append(ms_mz[round(bin_size/2)])
        else:
            ms.append(np.sum(ms_tensor[temp_value-1, :, i*bin_size:i*bin_size+bin_size], axis=1))
            ms_columns.append(ms_mz[(bin_size*i)+round(bin_size/2)])
    ms = pd.DataFrame(ms)
    ms.index = ms_columns
    # Plot figure
    fig, ax = plt.subplots()
    sns.heatmap(ms, ax=ax, center=0)
    ax.set_xticks(list(range(0, len(ms_rt), 5)))
    ax.set_xticklabels([str(x) for x in ms_rt[::5]])
    ax.set_ylabel(r'm/z-values (binned)')
    ax.set_xlabel(r'Retention time [min]')
    plt.title(graph_name + " heat map for plate {} sample {}".format(plates, samples))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def heatmap_MS_RT_binned(samples, plates, bin_numbers, ms_mode, rt_value, ms_tensor, data, canvas):
    """MS heatmap for one specific retention time with binned m/z-values.
    RT_value is the rention time of interest.
    P is the plate number.
    samples is a vector with the sample number(s) of intrest.
    MS_mode is either 'pos' or 'neg'.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Positive MS mode
    if ms_mode == 'pos':
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_pos'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_pos'].index
    else:
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_neg'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_neg'].index

    # Extract MS data for the given samples
    ms_tensor_samples = []
    for value, samples in enumerate(samples):
        ms_tensor_samples.append(ms_tensor[value - 1])
    ms_tensor_samples = np.array(ms_tensor_samples)
    ms_rt = np.round(ms_rt/60, 1)
    # Find index for selected retention time
    rt_closest_value = ms_rt[(np.fabs(ms_rt-rt_value)).argmin(axis=0)]
    rt_indx = [i for i, x in enumerate(ms_rt == rt_closest_value) if x][0]
    # Bin m/z-values accoridng to the number of bins defined
    ms = []
    ms_columns = []
    bin_size = round(len(ms_mz)/bin_numbers)
    for i in range(0, bin_numbers):
        if i == 0:
            ms.append(np.sum(ms_tensor_samples[:, rt_indx, 0:bin_size+bin_size], axis=1))
            ms_columns.append(ms_mz[round(bin_size/2)])
        else:
            ms.append(np.sum(ms_tensor_samples[:, rt_indx, i*bin_size:i*bin_size+bin_size], axis=1))
            ms_columns.append(ms_mz[(bin_size*i)+round(bin_size/2)])
    ms = pd.DataFrame(ms)
    ms.index = ms_columns
    # Plot figure
    fig, ax = plt.subplots()
    sns.heatmap(ms, ax=ax, center=0)
    ax.set_xticklabels(samples)
    ax.set_xlabel(r'Sample number')
    ax.set_ylabel(r'm/z-values (binned)')
    plt.title("MS(+) heatmap for plate {} at {} minutes".format(plates, ms_rt[rt_indx]))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg

def heatmap_MS_mz(samples, plates, ms_mode, mz_value, ms_tensor, data, canvas):
    """MS heatmap for one specific m/z-value.
    mz_value is the m/z-value of intrest.
    P is the plate number.
    samples is a vector with the sample number(s) of intrest.
    MS_mode is either 'pos' or 'neg'.
    uv_tensor is the tensor of intrest, e.g. P1_uv_tensor.
    data is the main dictionary containing all data."""
    # Positive MS mode
    if ms_mode == 'pos':
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_pos'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_pos'].index
    else:
        # Define m/z-values and retention times
        ms_mz = data[plates[0]][samples[0]]['MS_neg'].columns
        ms_rt = data[plates[0]][samples[0]]['MS_neg'].index

    # Extract MS data for the given samples
    ms_tensor_samples = []
    for value, samples in enumerate(samples):
        ms_tensor_samples.append(ms_tensor[value-1])
    ms_pos_tensor_samples = np.array(ms_tensor_samples)

    ms_rt = np.round(ms_rt/60, 1)
    # Find index for selected m/z-value
    mz_closest_value = ms_mz[(np.fabs(ms_mz-mz_value)).argmin(axis=0)]
    mz_indx = [i for i, x in enumerate(ms_mz == mz_closest_value) if x][0]
    # Plot figure
    fig, ax = plt.subplots()
    sns.heatmap(ms_pos_tensor_samples[:, :, mz_indx], ax=ax, center=0)
    ax.set_xticks(list(range(0, len(ms_rt), 5)))
    ax.set_xticklabels([str(x) for x in ms_rt[::5]])
    ax.set_ylabel(r'Sample number')
    ax.set_xlabel(r'Retention time [min]')
    plt.title("MS(+) heatmap for plate {} at {}".format(plates, ms_mz[mz_indx]))
    fig.tight_layout()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas.TKCanvas)

    return figure_canvas_agg


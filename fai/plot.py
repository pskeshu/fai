from fai import stats, files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use("seaborn-colorblind")
matplotlib.rc('savefig', dpi=300, bbox="tight", pad_inches=0)
matplotlib.rc('font', size=20)


def data_for_all_plots(list_of_dataclass):
    n_mean = []
    n_delta_mean = []
    n_norm_mean = []

    n_ks = []
    n_std = []

    for dataclass in list_of_dataclass:
        if len(dataclass.mean) != 27:
            continue
        n_mean.append(dataclass.mean)
        n_delta_mean.append(dataclass.mean_delta)
        n_norm_mean.append(dataclass.mean_norm)

        amaps = dataclass.anisotropy_round_median

        ks_ = []
        std_ = []
        for amap in amaps:
            ks_.append(stats.ks(amaps[0], amap)[0])
            std_.append(stats.std(amap))
        n_ks.append(ks_)
        n_std.append(std_)

    data = {
        "mean": ["Mean Anisotropy", n_mean],
        "delta": [r"$\Delta$ Anisotropy", n_delta_mean],
        "norm": [r"$r_t/r_0$", n_norm_mean],
        "ks": ["KS (0, t)", n_ks],
        "sd": ["SD Anisotropy", n_std],
    }

    return data


class PlotLines:
    def __init__(self, list_of_means, ylabel):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel(ylabel)
        self.ax.set_xticks([0, 60, 120])
        self.list_of_means = list_of_means
        self.time = np.arange(27) * 5

    def scatter_plot(self):
        starting_num = self.list_of_means[0][0]
        if starting_num in [0, 1]:
            self.ax.axhline(starting_num, c="k", linewidth=1, linestyle="--")
        for mean in self.list_of_means:
            self.ax.plot(self.time, mean)
            self.ax.scatter(self.time, mean, s=5)
        return self.ax

    def average_plot(self):
        mean_value = stats.mean(self.list_of_means, without_zero=False, axis=0)
        error_value = stats.sem(self.list_of_means, without_zero=False, axis=0)
        self.ax.errorbar(self.time, mean_value, yerr=error_value, capthick=2)
        self.ax.axhline(mean_value[0], c="k", linewidth=1, linestyle="--")
        return self.ax

    def save(self, savename):
        plt.tight_layout()
        plt.savefig(savename)
        plt.close()


def plot_all(list_of_dataclass, treatment, plotdir="./plots"):
    data = data_for_all_plots(list_of_dataclass)
    files.mkdir(plotdir)

    for savename in data:
        ylabel, ydata = data[savename]
        average = PlotLines(ydata, ylabel)
        ax = average.average_plot()
        average.save(f"{plotdir}/{savename}_average")

        scatter = PlotLines(ydata, ylabel)
        ax = scatter.scatter_plot()
        scatter.save(f"{plotdir}/{savename}")

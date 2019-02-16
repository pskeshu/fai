import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use("seaborn-colorblind")
matplotlib.rc('savefig', dpi=300, bbox="tight", pad_inches=0)
matplotlib.rc('font', size=20)


def scatter_plot(ax, list_of_means):
    time = np.arange(len(list_of_means[0])) * 5
    ax.set_xlabel("Time")
    ax.set_xticks([0, 60, 120])

    for mean in list_of_means:
        ax.plot(time, mean)
        ax.scatter(time, mean, s=5)

    return ax


def error_plot(ax, list_of_means):
    time = np.arange(len(list_of_means[0])) * 5
    ax.set_xlabel("Time")

    mean_value = np.mean(list_of_means, axis=0)
    error_value = stats.sem(list_of_means)

    ax.errorbar(time, mean_value, yerr=error_value, capthick=2)
    ax.set_xticks([0, 60, 120])

    return ax


def delta_mean_anisotropy(all_mean_delta, treatment, savename, error=False):
    fig, ax = plt.subplots()
    num = len(all_mean_delta)

    ax.set(ylabel=r"$\Delta$ Anisotropy",
           title=f"{treatment} N : {num}")

    ax.axhline(0, c="k", linewidth=1, linestyle="--")

    if error:
        ax = error_plot(ax, all_mean_delta)
        savename += "_error"
    else:
        ax = scatter_plot(ax, all_mean_delta)

    plt.savefig(f"{savename}")
    plt.close()


def mean_anisotropy(all_mean, treatment, savename, error=False):
    fig, ax = plt.subplots()
    num = len(all_mean)

    ax.set(ylabel="Mean Anisotropy",
           title=f"{treatment} N : {num}")

    if error:
        ax = error_plot(ax, all_mean)
        savename += "_error"
    else:
        ax = scatter_plot(ax, all_mean)

    plt.savefig(f"{savename}")
    plt.close()


def norm_mean_anisotropy(all_mean_norm, treatment, savename, error=False):
    fig, ax = plt.subplots()
    num = len(all_mean_norm)

    ax.set(ylabel=r"$r_t/r_0$",
           title=f"{treatment} N : {num}")

    ax.axhline(1, c="k", linewidth=1, linestyle="--")

    if error:
        ax = error_plot(ax, all_mean_norm)
        savename += "_error"
    else:
        ax = scatter_plot(ax, all_mean_norm)

    plt.savefig(f"{savename}")
    plt.close()

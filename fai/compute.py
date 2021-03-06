# Note: compare the results for:
#   1. round() vs np.around()
#   2. np.float() vs float()

import numpy as np
from fai import process, stats, util
import warnings


def anisotropy(dataclass, g_factor, bg):
    """Calculate anisotropy, given an image.

    Parameters
    ----------
    dataclass : AnisotropyData dataclass
        `parallel_roi_cropped` and `perpendicular_roi_reg_cropped` attributes
        are used for the anisotropy calculation.

    g_factor : float
        The correction factor for the bias in polarization.

    bg : float
        The constant background value to be subtracted from the image before
        calculating anisotropy. This is usually the baseline of the sensor.
        This value is generally 100.0 in the case of Andor Zyla 4.2 sCMOS
        camera.


    Returns
    -------
    dataclass : AnisotropyData dataclass
        The anisotropy map, rounded off to the 3rd decimal value is stored in
        the `anisotropy_raw` attribute in the dataclass.

    """

    if bg is not 100:
        warnings.warn("Background value should be 100")

    # read the raw data
    parallel = dataclass.parallel_roi_cropped
    perpendicular = dataclass.perpendicular_roi_reg_cropped

    # mask for cells
    mask = dataclass.mask_roi_cropped

    # calculate anisotropy for the given raw data
    anisotropy_map = _calculate_anisotropy(mask,
                                           parallel, perpendicular,
                                           g_factor, bg)
    # discretize anisotropy maps
    rounded_anisotropy = np.round(anisotropy_map, 3)

    # discretized median filtered anisotropy map
    median_filtered = process.median(rounded_anisotropy, size=3)

    # store the computed anisotropy values
    dataclass.anisotropy_raw = anisotropy_map
    dataclass.anisotropy_round = rounded_anisotropy
    dataclass.anisotropy_round_median = median_filtered

    # calculate different statistics for a given time series and
    # store it in dataclass
    _update_stats(dataclass, dataclass.anisotropy_round_median)

    metadata = dataclass.metadata
    metadata.update({"bg": bg, "g_factor": g_factor})

    return dataclass


def _calculate_anisotropy(mask, parallel, perpendicular, g_factor, bg):
    """Subtract bg, and calculate anisotropy"""

    # bg is also subtracted from regions outside the nucleus, which makes it
    # -100, resulting in incorrect anisotropy
    parallel = parallel - bg
    perpendicular = perpendicular - bg

    # To fix the above problem:
    # multiplied with nuclear RoI mask to set the outside nuclear region to 0.
    parallel = parallel * mask
    perpendicular = perpendicular * mask

    amap = calculate_r(parallel, perpendicular, g_factor)
    return amap


def calculate_r(parallel, perpendicular, g_factor):
    """
    Parameters
    ----------
    parallel : ndarray
        Parallel channel

    perpendicular : ndarray
        Perpendicular channel

    g_factor : float
        Correction factor to remove bias in detection

    Returns
    -------
    anisotropy_map : ndarray
        Anisotropy image
    """
    numerator = (parallel - (g_factor * perpendicular))
    denominator = (parallel + (2 * g_factor * perpendicular))

    with np.errstate(divide='ignore', invalid='ignore'):
        anisotropy_map = np.true_divide(numerator, denominator)
        anisotropy_map[~ np.isfinite(anisotropy_map)] = 0

    anisotropy_map[anisotropy_map >= 1] = 0
    anisotropy_map[anisotropy_map <= 0] = 0

    return anisotropy_map


def _update_stats(dataclass, anisotropy_timedata):
    """Helper function to calculate stats from an anisotropy timeseries and
    update to dataclass"""
    dataclass.mean = util.iterate(
        stats.mean, anisotropy_timedata, without_zero=True)
    dataclass.median = util.iterate(
        stats.median, anisotropy_timedata, without_zero=True)

    dataclass.mean_norm = stats.normalize(dataclass.mean)
    dataclass.median_norm = stats.normalize(dataclass.median)

    dataclass.mean_delta = stats.delta(dataclass.mean)
    dataclass.median_delta = stats.delta(dataclass.median)

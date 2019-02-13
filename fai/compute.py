# Note: compare the results for:
#   1. round() vs np.around()
#   2. np.float() vs float()

import numpy as np
from fai import process


def anisotropy(dataclass, g_factor, bg):
    """Calculate anisotropy, given an image.

    Parameters
    ----------
    dataclass : AnisotropyData dataclass
        `parallel_roi_cropped` and `perpendicular_roi_reg_cropped` attributes are
        used for the anisotropy calculation.

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
        the `anisotropy` attribute in the dataclass.

    """
    parallel = dataclass.parallel_roi_cropped - bg
    perpendicular = dataclass.perpendicular_roi_reg_cropped - bg

    numerator = (parallel - (g_factor * perpendicular))
    denominator = (parallel + (2 * g_factor * perpendicular))

    with np.errstate(divide='ignore', invalid='ignore'):
        anisotropy_map = np.true_divide(numerator, denominator)
        anisotropy_map[~ np.isfinite(anisotropy_map)] = 0

    anisotropy_map[anisotropy_map >= 1] = 0
    anisotropy_map[anisotropy_map <= 0] = 0

    rounded_anisotropy = np.round(anisotropy_map, 3)
    median_filtered = process.median(rounded_anisotropy, size=3)

    dataclass.anisotropy_raw = anisotropy_map
    dataclass.anisotropy_round = rounded_anisotropy
    dataclass.anisotropy_round_median = median_filtered

    metadata = dataclass.metadata
    metadata.update({"bg": bg, "g_factor": g_factor})

    return dataclass
